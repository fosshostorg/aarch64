package main

import (
	"context"
	"encoding/json"
	"flag"
	"io/ioutil"
	"log"
	"net"
	"os"
	"os/signal"
	"strconv"
	"strings"
	"syscall"
	"time"

	"github.com/bwmarrin/snowflake"
	"github.com/digitalocean/go-libvirt"
	"github.com/nsqio/go-nsq"
)

const (
	ControlEventChangeStateShutdown = iota
	ControlEventChangeStateStartup
	ControlEventChangeStateReset
	ControlEventChangeStateReboot
)

type ControlMessageData struct {
	Name   string `json:"name"`
	Source string `json:"source"`
	Event  int    `json:"event"`
	State  int    `json:"state"`
}

type ErrorMessage struct {
	Error     string `json:"error"`
	Text      string `json:"text"`
	Host      string `json:"host"`
	NSQMsg    string `json:"nsq_msg"`
	MachineID int64  `json:"machine_id"`
}

type ControlMessage struct {
	ID     int64              `json:"id"`
	Action string             `json:"action"`
	Data   ControlMessageData `json:"data"`
}

type processMessage struct{}

// HandleMessage implements the Handler interface.
func (h *processMessage) HandleMessage(m *nsq.Message) error {
	if len(m.Body) == 0 {
		// Returning nil will automatically send a FIN command to NSQ to mark the message as processed.
		return nil
	}

	var msg ControlMessage
	if err := json.Unmarshal(m.Body, &msg); err != nil {
		reportError(err, "Invalid NSQ Message", m)
		return nil
		// No point in even returning an error if we can't unmarshal the message as we don't want that requeued.
	}

	// NSQ does not guarantee messages are not duplicated. We'll check
	if seenIDs[msg.ID] {
		log.Printf("Dropped duplicate message, ID %d \n", msg.ID) // No need to send this to the error logger, it's natural
		return nil
	}
	seenIDs[msg.ID] = true

	var vm libvirt.Domain

	// If there is a VMName lets get the vm
	if msg.Data.Name != "" {
		tvm, err := lbvt.DomainLookupByName(msg.Data.Name)
		if err != nil {
			reportError(err, "VM could not be found", m)
			return nil
		}
		vm = tvm
	}

	switch msg.Action {
	case "changeState":
		if msg.Data.Name == "" {
			// We should have a producer output to a logs place for this kind of stuff
			return nil
		}
		// Change the state of the VM
		switch msg.Data.Event {
		case ControlEventChangeStateShutdown:
			lbvt.DomainShutdown(vm)
		case ControlEventChangeStateReboot:
			lbvt.DomainReboot(vm, libvirt.DomainRebootDefault)
		case ControlEventChangeStateReset:
			lbvt.DomainReset(vm, 0)
		case ControlEventChangeStateStartup:
			lbvt.DomainCreate(vm)
		default:
			// We should have a producer output to a logs place for this kind of stuff
			log.Printf("Unknown state %d provided to changeState \n", msg.Data.Event)
			reportError(nil, "Unknown state provided to changeState", m)
		}
	}

	return nil
}

func producerSendStruct(structToSend interface{}, title string, producer *nsq.Producer) {
	encoded_msg, err := json.Marshal(structToSend)
	if err != nil {
		reportFatalError(err, "Could not marshal struct for sending to Publisher", nil)
	}
	producer.PublishAsync(title, encoded_msg, nil)
}

func reportError(err error, text string, message *nsq.Message) {
	log.Println(text, err)
	msg := ErrorMessage{
		Error:     err.Error(),
		Text:      text,
		Host:      hostname,
		NSQMsg:    string(message.Body),
		MachineID: mid,
	}

	producerSendStruct(msg, "aarch64-error", apiProducer)
}

func reportFatalError(err error, text string, msg *nsq.Message) {
	reportError(err, text, msg)
	os.Exit(1)
}

func monitorVMStatus(ctx context.Context, snow *snowflake.Node) {
	events, _ := lbvt.LifecycleEvents(ctx)
	for event := range events {
		switch libvirt.DomainEventType(event.Event) {
		case libvirt.DomainEventStarted:
			msg := ControlMessage{
				ID:     int64(snow.Generate()),
				Action: "NewVMState",
				Data: ControlMessageData{
					Name:  event.Dom.Name,
					State: 1,
				},
			}
			producerSendStruct(msg, "aarch64-api", apiProducer)
		case libvirt.DomainEventStopped:
			msg := ControlMessage{
				ID:     int64(snow.Generate()),
				Action: "NewVMState",
				Data: ControlMessageData{
					Name:  event.Dom.Name,
					State: 5,
				},
			}
			producerSendStruct(msg, "aarch64-api", apiProducer)
		}
	}
}

func getMachineID() int64 {
	content, err := ioutil.ReadFile("/etc/mid")

	if err != nil {
		reportFatalError(err, "Could not read /etc/mid", nil)
	}
	midRaw, err := strconv.Atoi(strings.TrimSuffix(string(content), "\n"))
	mid := int64(midRaw)
	if err != nil {
		reportFatalError(err, "Machine does not have an MID or MID is stored incorrectly (/etc/mid)", nil)
	}

	log.Printf("Detected Machine ID of %d", mid)
	return mid
}

func connectToLibVirt() *libvirt.Libvirt {
	// Lets handle the libvirt stuff first
	c, err := net.DialTimeout("unix", "/var/run/libvirt/libvirt-sock", 2*time.Second)
	if err != nil {
		reportFatalError(err, "Could not connect to libvirt socket", nil)
	}

	l := libvirt.New(c)
	if err := l.Connect(); err != nil {
		reportFatalError(err, "Could not connect to libvirt", nil)
	}

	log.Printf("Connected to libvirt\n")
	return l
}

func getHostname() string {
	host, err := os.Hostname()
	if err != nil {
		reportFatalError(err, "Could not get hostname", nil)
	}

	return host
}

func createNSQConsumer(topic string, channel string) *nsq.Consumer {
	consumer, err := nsq.NewConsumer(topic, channel, nsq.NewConfig())
	if err != nil {
		reportFatalError(err, "Could not create NSQ consumer", nil)
	}
	consumer.AddHandler(&processMessage{})
	err = consumer.ConnectToNSQD(nsqConnectString)
	if err != nil {
		reportFatalError(err, "Could not connect to NSQ", nil)
	}
	return consumer
}

// Let's define our variables needed through the program
var (
	lbvt             *libvirt.Libvirt
	seenIDs          = make(map[int64]bool)
	nsqConnectString = *flag.String("nsq-connect-uri", "[fd0d:944c:1337:aa64:1::]:4150", "The URI for NSQ producers & consumers to connect to")
	hostname         string
	mid              int64
	apiProducer      *nsq.Producer
)

func main() {
	flag.Parse()
	lbvt = connectToLibVirt()
	defer lbvt.Disconnect()
	hostname := getHostname()
	mid = getMachineID()
	snow, _ := snowflake.NewNode(mid)

	// Set seenID to true so that packets without an ID get dropped
	seenIDs[0] = true

	// Create the apiProducer
	var err error
	apiProducer, err = nsq.NewProducer(nsqConnectString, nsq.NewConfig())
	if err != nil {
		reportFatalError(err, "Could not create NSQ producer", nil)
	}
	defer apiProducer.Stop()

	// Time for NSQ
	hostControlConsumer := createNSQConsumer("aarch64-"+hostname, "main")
	defer hostControlConsumer.Stop()
	clusterControlConsumer := createNSQConsumer("aarch64-cluster", hostname)
	defer clusterControlConsumer.Stop()

	// Let's allow our queues to drain properly during shutdown.
	// We'll create a channel to listen for SIGINT (Ctrl+C) to signal
	// to our application to gracefully shutdown.
	shutdown := make(chan os.Signal, 2)
	signal.Notify(shutdown, syscall.SIGINT)

	// This is our main loop. It will continue to read off of our nsq
	// channel until either the consumer dies or our application is signaled
	// to stop.
	monitorCTX := context.Background()
	go monitorVMStatus(monitorCTX, snow)
	defer monitorCTX.Done()

	for {
		select {
		case <-hostControlConsumer.StopChan:
			return
		case <-clusterControlConsumer.StopChan:
			return
		case <-shutdown:
			return
		}
	}
}

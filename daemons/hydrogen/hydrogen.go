package main

import (
	"context"
	"encoding/json"
	"flag"
	"log"
	"net"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/bwmarrin/snowflake"
	"github.com/digitalocean/go-libvirt"
	"github.com/fosshostorg/aarch64/daemons/internal/commons"
	"github.com/fosshostorg/aarch64/daemons/internal/message"
	"github.com/nsqio/go-nsq"
)

func handleMessage(m *nsq.Message) error {
	if len(m.Body) == 0 {
		// Returning nil will automatically send a FIN command to NSQ to mark the message as processed.
		return nil
	}

	var msg message.ControlMessage
	if err := json.Unmarshal(m.Body, &msg); err != nil {
		log.Printf("Invalid NSQ Message: %s\n", m.Body)
		return nil
		// No point in even returning an error if we can't unmarshal the message as we don't want that requeued.
	}

	// NSQ does not guarantee messages are not duplicated. We'll check
	if seenIDs[msg.ID] {
		log.Printf("Dropped duplicate message, ID %d\n", msg.ID) // No need to send this to the error logger, it's natural
		return nil
	}
	seenIDs[msg.ID] = true

	var vm libvirt.Domain

	// If there is a VMName lets get the vm
	if msg.Data.Name != "" {
		tvm, err := lbvt.DomainLookupByName(msg.Data.Name)
		if err != nil {
			log.Printf("%s\n", err) // This error already says everything to be said
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
		case message.ControlEventChangeStateShutdown:
			lbvt.DomainShutdown(vm)
		case message.ControlEventChangeStateReboot:
			lbvt.DomainReboot(vm, libvirt.DomainRebootDefault)
		case message.ControlEventChangeStateReset:
			lbvt.DomainReset(vm, 0)
		case message.ControlEventChangeStateStartup:
			lbvt.DomainCreate(vm)
		default:
			// We should have a producer output to a logs place for this kind of stuff
			log.Printf("Unknown state %d provided to changeState\n", msg.Data.Event)
		}
	}

	return nil
}

func monitorVMStatus(ctx context.Context, snow *snowflake.Node) {
	events, _ := lbvt.LifecycleEvents(ctx)
	for event := range events {
		switch libvirt.DomainEventType(event.Event) {
		case libvirt.DomainEventStarted:
			msg := message.ControlMessage{
				ID:     int64(snow.Generate()),
				Action: "NewVMState",
				Data: message.ControlMessageData{
					Name:  event.Dom.Name,
					State: 1,
				},
			}
			commons.ProducerSendStruct(msg, "aarch64-api", apiProducer)
		case libvirt.DomainEventStopped:
			msg := message.ControlMessage{
				ID:     int64(snow.Generate()),
				Action: "NewVMState",
				Data: message.ControlMessageData{
					Name:  event.Dom.Name,
					State: 5,
				},
			}
			commons.ProducerSendStruct(msg, "aarch64-api", apiProducer)
		}
	}
}

func connectToLibVirt() *libvirt.Libvirt {
	// Lets handle the libvirt stuff first
	c, err := net.DialTimeout("unix", "/var/run/libvirt/libvirt-sock", 2*time.Second)
	if err != nil {
		log.Printf("Could not connect to libvirt socket: %s\n", err)
	}

	l := libvirt.New(c)
	if err := l.Connect(); err != nil {
		log.Printf("Could not connect to libvirt: %s\n", err)
	}

	log.Printf("Connected to libvirt\n")
	return l
}

// Let's define our variables needed through the program
var (
	lbvt        *libvirt.Libvirt
	seenIDs     = make(map[int64]bool)
	hostname    string
	apiProducer *nsq.Producer
)

func main() {
	flag.Parse()
	lbvt = connectToLibVirt()
	defer lbvt.Disconnect()
	hostname := commons.GetHostname()
	snow := commons.GetSnow()

	// Set seenID to true so that packets without an ID get dropped
	seenIDs[0] = true

	// Create the apiProducer
	var err error
	apiProducer, err = nsq.NewProducer(commons.NSQCoreUrl, nsq.NewConfig())
	if err != nil {
		log.Printf("Could not connect to NSQ: %s\n", err)
	}
	defer apiProducer.Stop()

	// Time for NSQ
	hostControlConsumer := commons.CreateNSQConsumer(commons.NSQCoreUrl, "aarch64-"+hostname, "main", nsq.HandlerFunc(handleMessage))
	defer hostControlConsumer.Stop()
	clusterControlConsumer := commons.CreateNSQConsumer(commons.NSQCoreUrl, "aarch64-cluster", hostname, nsq.HandlerFunc(handleMessage))
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

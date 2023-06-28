package commons

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"os"
	"strconv"
	"strings"

	"github.com/bwmarrin/snowflake"
	"github.com/nsqio/go-nsq"
)

//var NSQCoreUrl = "[fd0d:944c:1337:aa64:1::]:4150"
var NSQCoreUrl = "[fd2f:376d:8703:aa64:1::]:4150"
var ProxyConfigPath = "/usr/local/openresty/nginx/conf/nginx.conf"
var ProxyCachePath = "/etc/berrylium.json"

func GetMachineID() int64 {
	content, err := ioutil.ReadFile("/etc/mid")

	if err != nil {
		log.Printf("Error reading machine ID: %s \n", err)
	}
	midRaw, err := strconv.Atoi(strings.TrimSuffix(string(content), "\n"))
	mid := int64(midRaw)
	if err != nil {
		log.Printf("Error parsing machine ID: %s", err)
	}

	log.Printf("Detected Machine ID of %d \n", mid)
	return mid
}

func GetHostname() string {
	host, err := os.Hostname()
	if err != nil {
		log.Printf("Error getting hostname: %s \n", err)
	}

	return host
}

func CreateNSQConsumer(uri string, topic string, channel string, handler nsq.Handler) *nsq.Consumer {
	consumer, err := nsq.NewConsumer(topic, channel, nsq.NewConfig())
	if err != nil {
		log.Printf("Error creating NSQ consumer: %s \n", err)
	}
	consumer.AddHandler(handler)
	err = consumer.ConnectToNSQD(uri)
	if err != nil {
		log.Printf("Error connecting to NSQD: %s \n", err)
	}
	return consumer
}

func GetSnow() *snowflake.Node {
	mid := GetMachineID()
	snow, _ := snowflake.NewNode(mid)
	return snow
}

func ProducerSendStruct(structToSend interface{}, title string, producer *nsq.Producer) {
	encoded_msg, err := json.Marshal(structToSend)
	if err != nil {
		log.Printf("Could not marshal struct for sending to Publisher: %s\n", err)
	}
	producer.PublishAsync(title, encoded_msg, nil)
}

package main

import (
	"encoding/json"
	"flag"

	"github.com/fosshostorg/aarch64/daemons/internal/commons"
	"github.com/fosshostorg/aarch64/daemons/internal/message"
	"github.com/nsqio/go-nsq"
	"go.uber.org/zap"
)

func NewNSQHandler(l *zap.Logger) *NSQHandler {
	return &NSQHandler{l}
}

type NSQHandler struct {
	l *zap.Logger
}

func (h *NSQHandler) HandleMessage(m *nsq.Message) error {
	// Message Body Should Not be Empty
	if m.Body != nil || len(m.Body) <= 0 {
		h.l.Error("message body is empty")
		return nil
	}

	// Decode Message Body
	var data message.ProxyUpdateMessage
	if err := json.Unmarshal(m.Body, &data); err != nil {
		h.l.Error("failed to unmarshal message", zap.Error(err))
		return nil
	}

	return nil
}

func main() {
	l, _ := zap.NewDevelopment()

	var (
		nsqConnectURI   string
		proxyConfigPath string
	)

	// Parse Flags
	flag.StringVar(&nsqConnectURI, "nsq-connect-uri", commons.NSQCoreUrl, "The URI for NSQ producers & consumers to connect to")
	flag.StringVar(&proxyConfigPath, "proxy-config-path", "", "The path to the proxy configuration file")
	flag.Parse()
	if proxyConfigPath == "" {
		l.Fatal("proxy-config-path is required")
	}

	// Connect to NSQ
	hostname := commons.GetHostname()

}

package message

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

const (
	ControlEventChangeStateShutdown = iota
	ControlEventChangeStateStartup
	ControlEventChangeStateReset
	ControlEventChangeStateReboot
)

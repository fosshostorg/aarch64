package message

type MessageData struct {
	Name   string      `json:"name"`
	Source string      `json:"source"`
	Event  ActionEvent `json:"event"`
	Num    int         `json:"state"`
}

type ErrorMessage struct {
	Error     string `json:"error"`
	Text      string `json:"text"`
	Host      string `json:"host"`
	NSQMsg    string `json:"nsq_msg"`
	MachineID int64  `json:"machine_id"`
}

type Message struct {
	ID     int64       `json:"id"`
	Action Action      `json:"action"`
	Data   MessageData `json:"data"`
}

type Action int64

const (
	ChangeState Action = iota
	NewVMState
)

type ActionEvent int64

const (
	StateShutdown ActionEvent = iota
	StateStartup
	StateReset
	StateReboot
	StateStop
)

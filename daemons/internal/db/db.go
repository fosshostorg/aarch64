package db

type VM struct {
	ID          string `bson:"_id"`
	Hostname    string `bson:"hostname"`
	Pop         string `bson:"pop"`
	Project     string `bson:"project"`
	Os          string `bson:"os"`
	Vcpus       int    `bson:"vcpus"`
	Memory      int    `bson:"memory"`
	Ssd         int    `bson:"ssd"`
	Host        int    `bson:"host"`
	Password    int    `bson:"password"`
	Phoned_home bool   `bson:"phoned_home"`
	Created     struct {
		By string  `bson:"by"`
		At float64 `bson:"at"` // unix timestamp
	} `bson:"created"`
	Index   int    `bson:"index"`
	Prefix  string `bson:"prefix"`
	Gateway string `bson:"gateway"`
	Address string `bson:"address"`
	State   int    `bson:"state"`
}

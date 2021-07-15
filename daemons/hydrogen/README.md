# Hydrogen
Hydrogen is a NSQ Consumer/Producer living on the aarch64 hypervisor. It takes in jobs from the central api server and translates those to local libvirt calls, haproxy config changes, and more.
It is highly specialized for the setup of fosshost so would require extensive customization to use elsewhere. 

## NSQ Layout
Each hypervisor creates a topic for itself called `aarch64-hostname` and creates a channel with it's hostname on the topic `aarch64-cluster`. Control Messages for a single hypervisor should be sent to `aarch64-hostname`, while messages for the cluster should be sent to `aarch64-cluster`
Hydrogen is also an NSQ producer outputting to `aarch64-errors` to report runtime errors it enounters and `aarch64-api` to report VM state changes to the API server

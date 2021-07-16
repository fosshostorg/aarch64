# Meet the rest of the class

## Hydrogen 
Hydrogen is a NSQ Consumer/Producer living on the aarch64 hypervisor. It takes in jobs from the central api server and translates those to local libvirt calls, haproxy config changes, and more.
It is highly specialized for the setup of fosshost so would require extensive customization to use elsewhere. It listens on `aarch64-[hostname]#main` & `aarch64-cluster#[hostname]` for jobs. It also keeps track of local VM Power States and outputs those to `aarch64-api`. 
### Commonly found in
* `aarch64-[hostname]#main`
* `aarch64-cluster#[hostname]`
### Known to harass
* `Helium`

## Helium
Helium is an NSQ Consumer with the role of taking in VM Power State changes from hypervisors and updating the central mongodb server with the new state.

### Commonly found in
* `aarch64-api#helium`
### Known to harass
* Nobody, Helium is quite scared of others

## Lithium
Lithium is a very bossy NSQ Consumer & Producer. Filled with importance it controls the cluster sending out control messages. It sends out messages to the hypervisors to update their libvirt configs, haproxy configs, and more. Clusterwide messages are sent to `aarch64-cluster` while messages to individual machines are sent to `aarch64-[hostname]`. 
### Commonly found in
* `aarch64-api#lithium`
### Known to harass
* `Hydrogen`

# NSQ Layout
Each hypervisor creates a topic for itself called `aarch64-[hostname]` and creates a channel with it's hostname on the topic `aarch64-cluster`. Control Messages for a single hypervisor should be sent to `aarch64-hostname`, while messages for the cluster should be sent to `aarch64-cluster`. Messages to the API server are sent to `aarch64-api`.
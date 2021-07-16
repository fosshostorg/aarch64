# Meet the rest of the class

## Hydrogen 
Hydrogen is a NSQ Consumer/Producer living on the aarch64 hypervisor. It takes in jobs specifically related to libvirt vms on the hypervisor, listening on `aarch64-libvirt-[hostname]#main` for jobs. It also keeps track of local VM Power States and outputs those to `aarch64-power`. 
### Commonly found in
* `aarch64-libvirt-[hostname]#main`
### Known to harass
* `Helium`

## Helium
Helium is an NSQ Consumer with the role of taking in VM Power State changes from hypervisors and updating the central mongodb server with the new state.

### Commonly found in
* `aarch64-power#helium`
### Known to harass
* Nobody, Helium is quite scared of others

## Lithium
Lithium is a very bossy NSQ Consumer & Producer. Filled with importance it controls the cluster sending out control messages. It sends out messages to the hypervisors to update their libvirt configs, haproxy configs, and more. Libvirt control messages are sent to individual machines at `aarch64-libvirt-[hostname]`, while haproxy configuration changes are sent to the entire cluster via `aarch64-haproxy` 
### Commonly found in
* `aarch64-api#lithium`
### Known to harass
* `Hydrogen`

## Beryllium
Beryllium is an NSQ Consumer residing on the hypervisors. It listens on `aarch64-haproxy#[hostname]` and updates the local HAProxy configuration in accordance with the received messages.
### Commonly found in
* `aarch64-haproxy#[hostname]`
### Known to harass
* Nobody, Beryllium enjoys being alone on friday nights


# NSQ Layout TL;DR
* `aarch64-libvirt-[hostname]#main` 
    * Consumer: Hydrogen
    * Producer: Lithium
    * Role: Libvirt Control Commands
* `aarch64-power#helium`
    * Consumer: Helium
    * Producer: Hydrogen
    * Role: VM Power State Updates
* `aarch64-haproxy#[hostname]`
    * Consumer: Beryllium
    * Producer: Lithium
    * Role: HAProxy Configuration
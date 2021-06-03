import libvirt
from api import db, to_object_id, prefix_to_wireguard

hypervisors = []
for pop in db["pops"].find():
    if pop.get("hosts"):
        for idx, host in enumerate(pop.get("hosts")):
            hypervisors.append(prefix_to_wireguard(host["prefix"]))

for hypervisor in hypervisors:
    try:
        conn = libvirt.open(f'qemu+tcp://root@[{hypervisor}]:16509/system')
    except libvirt.libvirtError as e:
        print(e, file=sys.stderr)
    vms = conn.listAllDomains(0)
    for vm in vms:
        result = db["vms"].update_one(
            {"_id": to_object_id(vm.name())},
            {
                "$set": {"state": vm.info()[0]}
            }
        )
    conn.close()
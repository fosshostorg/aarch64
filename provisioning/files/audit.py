import os


def destroy(vm):
    print("Destroying " + vm)
    os.system(f"virsh destroy {vm}")
    os.system(f"virsh undefine --nvram {vm}")
    os.system(f"rm -rf /opt/aarch64/vms/{vm}*")


auth_vms = []
with open("/tmp/authorized-vms.txt", "r") as auth_vms_file:
    for vm in auth_vms_file:
        auth_vms.append(vm.strip())

auth_ifaces = []
with open("/tmp/authorized-ifaces.txt", "r") as auth_ifaces_file:
    for iface in auth_ifaces_file:
        auth_ifaces.append(iface.strip())

auth_ok = True
for vm in os.popen("virsh list --all | tail -n +3").read().strip().split("\n"):
    vm = vm.split(" ")
    while "" in vm:
        vm.remove("")

    if len(vm) > 0:
        if vm[1] not in auth_vms:
            auth_ok = False
            destroy(vm[1])

# Audit network interfaces
ifaces_ok = True
for iface in os.listdir("/sys/class/net/"):
    if iface.startswith("vbr"):  # If VM bridge
        if iface not in auth_ifaces:
            os.system(f"ip link del {iface}")  # TODO: Netlink instead of calling ip
            ifaces_ok = False

if not (auth_ok and ifaces_ok):
    exit(2)

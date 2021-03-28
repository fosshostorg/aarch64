import os

auth_vms = []
with open("/tmp/authorized-vms.txt", "r") as auth_vms_file:
    for vm in auth_vms_file:
        auth_vms.append(vm)

auth_ok = True
for vm in os.popen("virsh list --all | tail -n +3").read().strip().split("\n"):
    parts = vm.replace("  ", "").split(" ")

    while "" in parts:
        parts.remove("")

    if len(parts) > 2:
        if parts[1] not in auth_vms:
            auth_ok = False
            print(f"VM {parts[1]} is not defined, destroying")
            os.system(f"virsh destroy {parts[1]}")
            os.system(f"virsh undefine --nvram {parts[1]}")
            os.system(f"rm -rf /opt/aarch64/vms/{parts[1]}*")

if not auth_ok:
    exit(1)

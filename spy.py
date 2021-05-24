import libvirt
import sys
import json
import resp from api.py
from flask import Flask, request, Response, makeresponse

try:
    conn = libvirt.open()
except libvirt.libvirtError:
    print('Failed to open connection to the hypervisor')
    sys.exit(1)

app = Flask(__name__)

class JSONResponseEncoder(json.JSONEncoder):
    """
    BSON ObjectId-safe JSON response encoder
    """

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def domainToDict(vm):
        vm_info = vm.info()
        return {'name': vm.name(), 'state': vm_info[0], 'maxMemory': vm_info[1], 'vCPUs': vm_info[3]}


@app.route("/vms")
def listVMs():
    try:  # getting a list of all domains (by ID) on the host
        domains = conn.listAllDomains(0)
    except:
        raise Exception('Failed to find any domains')

    vms = []
    for vm in domains:
        vms.append(domainToDict(vm))

    return resp(True, "Virtual Machines", data=vms)

@app.route("/vm/<name>/start")
def startVM(name):
    vm = conn.lookupByName(name)
    try:
        vm.create()
        return resp(True, "Started VM")
    except Exception as e:
        return resp(False, str(e))

@app.route("/vm/<name>/stop")
def stopVM(name):
    vm = conn.lookupByName(name)
    try:
        vm.shutdown()
        return resp(True, "Stopped VM")
    except Exception as e:
        return resp(False, str(e))

# Lets only listen on the wireguard interface
with open("/etc/wireguard/wg0.conf") as f:
    content = f.readlines()
    # Get the address in the wireguard config file
    app.run(host=content[1].split(" = ")[1].split("/")[0])
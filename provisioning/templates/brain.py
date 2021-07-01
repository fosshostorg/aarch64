import libvirt
import socket
import json
import os
import uuid
from threading import Timer
import threading
from socketserver import BaseRequestHandler, ThreadingTCPServer

def setInterval(timer, task):
    isStop = task()
    if not isStop:
        Timer(timer, setInterval, [timer, task]).start()

try:
    virt = libvirt.open()
except libvirt.libvirtError:
    print('Failed to open connection to the hypervisor')
    sys.exit(1)

def getState():
    try:  # getting a list of all domains (by ID) on the host
        domains = virt.listAllDomains(0)
    except:
        raise Exception('Failed to find any domains')
    state = {}
    for vm in domains:
        vm_info = vm.info()
        state[vm.name()] = {'name': vm.name(), 'state': vm_info[0], 'maxMemory': vm_info[1], 'vCPUs': vm_info[3]}
    return state;

def sendDictPacket(conn, dict):
    conn.request.send(bytes(json.dumps(dict)+"\n", 'utf-8'))

global_state = getState()
connections = {}

ip_acl = ["fd0d:944c:1337:aa64:1::", "fd0d:944c:1337:b:6:1::"]
# password="testing-password-if-this-prod-somebody-messed-up"
# if "PASSWORD" in os.environ:
#     password = os.environ["PASSWORD"]

def syncNewConnection(conn):
    for i in global_state:
        sendDictPacket(conn, {"type": "state", "id": i, "state": global_state[i]["state"]})

def collectNewState():
    new_state = getState()
    for i in new_state:
        vm = new_state[i]
        if (i in global_state):
            if (vm["state"] != global_state[i]["state"]):
                for conn_i in connections:
                    conn = connections[conn_i]
                    if (conn["data"]["auth"]):
                        sendDictPacket(conn["handler"], {"type": "state", "id": i, "state": vm["state"]})
        global_state[i] = new_state[i]

class TCPServerV6(ThreadingTCPServer):
    address_family = socket.AF_INET6
    allow_reuse_address = True

def keyCheckPacket(conn, packet, keys):
    for key in keys:
        if not key in packet:
            sendDictPacket(conn["handler"], {"type": "InvalidPacket", "msg": f'Missing {key} in {packet["type"]}'})
            return False
    return True


class EchoHandler(BaseRequestHandler):
    def handle(self):
        print('connection from:', self.client_address)
        if not self.client_address[0] in ip_acl:
            print(f'{self.client_address[0]} is not in the IP ACL')
            return
        sock_id = uuid.uuid1()
        conn = {
            "data": {
                "auth": True,
                "id": sock_id
            },
            "handler": self
        }
        connections[sock_id] = conn
        syncNewConnection(self)
        while True:
            msg = self.request.recv(8192)
            try:
                msg_decoded = json.loads(msg)
            except:
                try:
                    sendDictPacket(self, {"type": "InvalidPacket", "msg": "Invalid JSON"})
                except:
                    # The pipe has broken, so lets just remove it and break out
                    connections.pop(sock_id)
                    break
                continue
            if (not "type" in msg_decoded):
                sendDictPacket(self, {"type": "InvalidPacket", "msg": "Missing type"})
                continue
            msg_type = msg_decoded["type"]
            # if (msg_type == "auth"):
            #     if not keyCheckPacket(conn, msg_decoded, ["pass"]):
            #         continue
            #     if (msg_decoded["pass"] == password):
            #         conn["data"]["auth"] = True
            #         sendDictPacket(self, {"type": "authsuccess"})
            #         syncNewConnection(self);
            #     else:
            #         sendDictPacket(self, {"type": "authfail"})
            #     continue;

            # All commands past here require auth
            if (not conn["data"]["auth"]):
                continue;
            
            if (msg_type == "changestate"):
                if not keyCheckPacket(conn, msg_decoded, ["state", "id"]):
                    continue
                    
                try:    
                    vm = virt.lookupByName(msg_decoded["id"])
                except:
                    sendDictPacket(self, {"type": "vmnotfound", "id": msg_decoded["id"]})
                    continue;   
                state = msg_decoded["state"]
                try: 
                    if (state == "stop"):
                        vm.shutdown()
                        continue
                    if (state == "start"):
                        vm.create()
                        continue
                except Exception as e:
                    sendDictPacket(self, {"type": "statechangeerror", "id": msg_decoded["id"], "err": str(e)})



# get wireguard IP & only listen on that
with open("/etc/wireguard/wg0.conf") as f:
    content = f.readlines()
    wgip = content[1].split(" = ")[1].split("/")[0]
    print(wgip)
    server = TCPServerV6((wgip, 5000), EchoHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

setInterval(1.0, collectNewState) 
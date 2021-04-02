import datetime
import ipaddress
import json
import re
import time
from email.mime.text import MIMEText
from functools import wraps
from os import environ
from secrets import token_hex
from smtplib import SMTP_SSL as SMTP

# noinspection PyPackageRequirements
from argon2 import PasswordHasher
# noinspection PyPackageRequirements
from argon2.exceptions import VerifyMismatchError
from bson import ObjectId
from flask import Flask, request, Response, make_response
from pymongo import ASCENDING, MongoClient
from pymongo.errors import DuplicateKeyError, InvalidId
from rich.console import Console

VERSION = "0.0.1"
DEBUG = environ.get("AARCH64_DEBUG")

console = Console()
argon = PasswordHasher()

app = Flask(__name__)
db = MongoClient("mongodb://localhost:27017")["aarch64"]
db["users"].create_index([("email", ASCENDING)], background=True, unique=True)
db["pops"].create_index([("name", ASCENDING)], background=True, unique=True)
db["proxies"].create_index([("label", ASCENDING)], background=True, unique=True)

# Check for config doc
config_doc = db["config"].find_one()
if not config_doc:
    console.log("Config doc doesn't exist")
    exit(1)

# Validate config prefix
try:
    ipaddress.ip_network(config_doc.get("prefix"), False)
except ValueError as e:
    console.log(f"Invalid prefix {config_doc.get('prefix')} ({e})")
    exit(1)

if (not config_doc.get("oses")) or (len(config_doc.get("oses")) < 1):
    console.log("Config must have at least one OS defined")
    exit(1)

if (not config_doc.get("plans")) or (len(config_doc.get("plans")) < 1):
    console.log("Config must have at least one plan defined")
    exit(1)

if not DEBUG and not config_doc.get("email"):
    console.log("Config must have an email account set up")
    exit(1)


def valid_label(label) -> bool:
    # Validates a DNS zone label
    return label and (re.match(r"^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,63}(?<!-)$", label) is None) and (not label.startswith(".")) and (" " not in label)


def send_email(to: str, subject: str, body: str):
    if not DEBUG:
        # Update config doc
        # noinspection PyShadowingNames
        config_doc = db["config"].find_one()

        # Build the MIME email
        msg = MIMEText(body, "plain")
        msg["Subject"] = subject
        msg["To"] = to
        msg["From"] = config_doc["email"]["address"]

        # Connect and send the email
        server = SMTP(config_doc["email"]["server"])
        server.login(config_doc["email"]["address"], config_doc["email"]["password"])
        server.sendmail(config_doc["email"]["address"], [to], msg.as_string())
        server.quit()
    else:
        print(f"Debug mode set, would send email to {to} subject {subject}")


def to_object_id(object_id: str):
    """
    Cast object_id:str to ObjectId
    """

    try:
        return ObjectId(object_id)
    except InvalidId:
        return ""


def get_project(user_doc: dict, project_id):
    if not user_doc.get("admin"):
        return db["projects"].find_one({
            "_id": to_object_id(project_id),
            "users": {
                "$in": [user_doc["_id"]]
            }
        })
    else:  # If admin
        return db["projects"].find_one({"_id": to_object_id(project_id)})


class JSONResponseEncoder(json.JSONEncoder):
    """
    BSON ObjectId-safe JSON response encoder
    """

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def _resp(success: bool, message: str, data: object = None):
    """
    Return a JSON API response
    :param success: did the request succeed?
    :param message: what happened?
    :param data: any application specific data
    """

    return Response(JSONResponseEncoder().encode({
        "meta": {
            "success": success,
            "message": message
        },
        "data": data
    }), mimetype="application/json")


def with_json(*outer_args):
    """
    Get JSON API request body
    :param outer_args: *args (str) of JSON keys
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _json_body = {}
            for arg in outer_args:
                if not request.json:
                    return _resp(False, "JSON body must not be empty")
                val = request.json.get(arg)
                if val is not None and val is not "":
                    _json_body[arg] = val
                else:
                    return _resp(False, "Required argument " + arg + " is not defined.")
            return func(*args, **kwargs, json_body=_json_body)

        return wrapper

    return decorator


def with_authentication(admin: bool):
    """
    Require a user to be authenticated and pass user_doc to function
    :param admin: Does the user have to be an administrator?
    :return:
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get API key from header (default) or cookie (fallback)
            api_key = request.headers.get("Authorization")
            if not api_key:
                api_key = request.cookies.get("key")
            if not api_key:
                return _resp(False, "Not authenticated"), 403

            user_doc = db["users"].find_one({"key": api_key})
            if not user_doc:
                return _resp(False, "Not authenticated"), 403
            if admin and not user_doc.get("admin"):
                return _resp(False, "Unauthorized"), 403

            return func(*args, **kwargs, user_doc=user_doc)

        return wrapper

    return decorator


@app.route("/auth/signup", methods=["POST"])
@with_json("email", "password")
def signup(json_body: dict) -> Response:
    if not json_body.get("email"):
        return _resp(False, "Account email must exist")

    if not json_body.get("password"):
        return _resp(False, "Account password must exist")

    # TODO: Real email validation
    if not ("@" in json_body["email"] and "." in json_body["email"]):
        return _resp(False, "Invalid email address")

    try:
        db["users"].insert_one({
            "email": json_body["email"],
            "password": argon.hash(json_body["password"]),
            "key": token_hex(24)
        })
    except DuplicateKeyError:
        return _resp(False, "User with this email already exists")

    return _resp(True, "User created")


@app.route("/auth/login", methods=["POST"])
@with_json("email", "password")
def user_login(json_body: dict) -> Response:
    """
    Verify credentials and log a user in
    :param json_body: supplied by decorator
    """

    user = db["users"].find_one({"email": json_body["email"]})
    if not user:
        return _resp(False, "Invalid username or password")

    try:
        valid = argon.verify(user["password"], json_body["password"])
        if not valid:
            raise VerifyMismatchError
        else:
            rsp = make_response(_resp(True, "Authentication successful"))
            # Set the API key cookie with a 90 day expiration date
            rsp.set_cookie("key", user["key"], httponly=True, secure=True, expires=datetime.datetime.now() + datetime.timedelta(days=90))
            return rsp
    except VerifyMismatchError:
        return _resp(False, "Invalid username or password")


@app.route("/auth/logout", methods=["POST"])
def user_logout() -> Response:
    """
    Log a user out by removing key cookie
    """

    resp = make_response(_resp(True, "Logged out"))
    # Overwrite and expire the key cookie immediately
    resp.set_cookie("key", "", expires=0, httponly=True, secure=True)
    return resp


@app.route("/auth/user", methods=["GET"])
@with_authentication(admin=False)
def user_info(user_doc: dict) -> Response:
    """
    Get user info doc
    """

    del user_doc["password"]
    return _resp(True, "Retrieved user info", data=user_doc)


@app.route("/project", methods=["POST"])
@with_authentication(admin=False)
@with_json("name")
def create_project(json_body: dict, user_doc: dict) -> Response:
    # Begin beta tmp code
    if not user_doc.get("admin"):
        return _resp(False, "During the AARCH64 beta, only administrators can create projects. Please let your contact at Fosshost know your email address to continue.")
    # End beta tmp code

    if not json_body.get("name"):
        return _resp(False, "Project name must exist")

    project = db["projects"].insert_one({
        "name": json_body["name"],
        "users": [user_doc["_id"]]
    })

    return _resp(True, "Project created", str(project.inserted_id))


@app.route("/projects", methods=["GET"])
@with_authentication(admin=False)
def projects_list(user_doc: dict) -> Response:
    """
    Get all projects that a user is part of
    """

    if not user_doc.get("admin"):
        projects = list(db["projects"].find({
            "users": {
                "$in": [user_doc["_id"]]
            }
        }))
    else:  # Get all projects if admin
        projects = list(db["projects"].find({}))

    for project in projects:
        if not project.get("vms"):
            project["vms"] = []
        for vm in db["vms"].find({"project": project["_id"]}):
            vm_creator = db["users"].find_one({"_id": vm["created"]["by"]})
            vm["creator"] = vm_creator["email"]
            project["vms"].append(vm)

        # Convert user IDs to email addresses
        project_users = []
        for user in project["users"]:
            project_user_doc = db["users"].find_one({"_id": user})
            if project_user_doc:
                project_users.append(project_user_doc["email"])
        project["users"] = project_users

    return _resp(True, "Retrieved project list", data=projects)


@app.route("/vms/create", methods=["POST"])
@with_authentication(admin=False)
@with_json("hostname", "plan", "pop", "project", "os")
def create_vm(json_body: dict, user_doc: dict) -> Response:
    pop_doc = db["pops"].find_one({"name": json_body["pop"]})
    if not pop_doc:
        return _resp(False, "PoP doesn't exist")

    # Update config doc
    # noinspection PyShadowingNames
    config_doc = db["config"].find_one()

    if json_body["plan"] not in config_doc["plans"].keys():
        return _resp(False, "Plan doesn't exist")

    json_body["vcpus"] = config_doc["plans"][json_body["plan"]]["vcpus"]
    json_body["memory"] = config_doc["plans"][json_body["plan"]]["memory"]
    json_body["ssd"] = config_doc["plans"][json_body["plan"]]["ssd"]
    del json_body["plan"]

    if json_body["os"] not in config_doc["oses"].keys():
        return _resp(False, "OS doesn't exist")

    if not user_doc.get("admin"):
        project_doc = db["projects"].find_one({
            "_id": to_object_id(json_body["project"]),
            "users": {
                "$in": [user_doc["_id"]]
            }
        })
    else:  # Get project if admin
        project_doc = db["projects"].find_one({"_id": to_object_id(json_body["project"])})
    if not project_doc:
        return _resp(False, "Project doesn't exist or unauthorized")
    json_body["project"] = to_object_id(json_body["project"])

    # Calculate host usage for pop
    _host_usage = {}
    for idx, host in enumerate(pop_doc["hosts"]):
        if idx not in _host_usage:
            _host_usage[idx] = 0

        for host_vm in db["vms"].find({"pop": json_body["pop"], "host": idx}):
            _host_usage[idx] += (host_vm["vcpus"] + host_vm["memory"])

    # Sort host usage dict by value (ordered from least used to greatest)
    _host_usage = {k: v for k, v in sorted(_host_usage.items(), key=lambda item: item[1])}

    # Find the least utilized host by taking the first element (call next on iter)
    json_body["host"] = next(iter(_host_usage))

    # Set temporary password
    json_body["password"] = token_hex(16)

    json_body["phoned_home"] = False
    json_body["created"] = {
        "by": user_doc["_id"],
        "at": time.time()
    }

    # Find taken prefixes
    taken_prefixes = []
    taken_indices = []
    for vm in db["vms"].find({"pop": json_body["pop"]}):
        taken_prefixes.append(vm["prefix"])
        taken_indices.append(vm["index"])

    # Set unique VM index
    for index in range(0, 65535):
        if index not in taken_indices:
            json_body["index"] = index

    if not json_body.get("index"):
        return _resp(False, "Unable to assign VM index")

    # Iterate over the selected host's prefix
    host_prefix = pop_doc["hosts"][json_body["host"]]["prefix"]
    for prefix in list(ipaddress.ip_network(host_prefix).subnets(new_prefix=64)):
        if str(prefix) not in taken_prefixes:
            json_body["prefix"] = str(prefix)
            json_body["gateway"] = str(prefix[1])
            json_body["address"] = str(prefix[2]) + "/" + str(str(prefix.prefixlen))
    if not json_body.get("prefix"):
        raise _resp(False, "Unable to assign VM prefix")

    new_vm = db["vms"].insert_one(json_body)
    if new_vm.inserted_id:
        return _resp(True, "VM created", data=json_body)

    raise _resp(False, "Unable to create VM")


@app.route("/project/adduser", methods=["POST"])
@with_authentication(admin=False)
@with_json("project", "email")
def project_add_user(json_body: dict, user_doc: dict) -> Response:
    project_doc = get_project(user_doc, json_body["project"])
    if not project_doc:
        return _resp(False, "Project doesn't exist or unauthorized")

    user_doc = db["users"].find_one({"email": json_body["email"]})
    if not user_doc:
        return _resp(False, "User doesn't exist")

    if user_doc["_id"] in project_doc["users"]:
        return _resp(True, "User is already a member of that project")

    project_update = db["projects"].update_one({"_id": to_object_id(json_body["project"])}, {"$push": {"users": user_doc["_id"]}})
    if project_update.modified_count == 1:
        return _resp(True, "User added to project")
    return _resp(False, "Unable to add user to project")


@app.route("/project", methods=["DELETE"])
@with_authentication(admin=False)
@with_json("project")
def delete_project(json_body: dict, user_doc: dict) -> Response:
    project_doc = get_project(user_doc, json_body["project"])
    if not project_doc:
        return _resp(False, "Project doesn't exist or unauthorized")

    for vm in db["vms"].find({"project": project_doc["_id"]}):
        db["vms"].delete_one({"_id": vm["_id"]})

    deleted_project = db["projects"].delete_one({"_id": project_doc["_id"]})
    if deleted_project.deleted_count == 1:
        return _resp(True, "Project deleted")
    return _resp(False, "Unable to delete project")


@app.route("/vms/delete", methods=["DELETE"])
@with_authentication(admin=False)
@with_json("vm")
def delete_vm(json_body: dict, user_doc: dict) -> Response:
    vm_doc = db["vms"].find_one({"_id": to_object_id(json_body["vm"])})
    if not vm_doc:
        return _resp(False, "VM doesn't exist")

    project_doc = get_project(user_doc, vm_doc["project"])
    if not project_doc:
        return _resp(False, "Project doesn't exist or unauthorized")

    deleted_vm = db["vms"].delete_one({"_id": to_object_id(json_body["vm"])})
    if deleted_vm.deleted_count == 1:
        return _resp(True, "VM deleted")
    return _resp(False, "Unable to delete VM")


@app.route("/proxy", methods=["POST"])
@with_authentication(admin=False)
@with_json("label", "vm")
def add_proxy(json_body: dict, user_doc: dict) -> Response:
    vm_doc = db["vms"].find_one({"_id": to_object_id(json_body["vm"])})
    if not vm_doc:
        return _resp(False, "VM doesn't exist")

    project_doc = get_project(user_doc, vm_doc["project"])
    if not project_doc:
        return _resp(False, "Project doesn't exist or unauthorized")

    # Validate DNS zone label
    if not valid_label(json_body["label"]):
        return _resp(False, "Invalid label")

    try:
        new_proxy = db["proxies"].insert_one({
            "project": project_doc["_id"],
            "label": json_body["label"],
            "vm": vm_doc["_id"]
        })
    except DuplicateKeyError:
        return _resp(False, "Proxy already exists")

    if new_proxy.inserted_id:
        return _resp(True, "Added proxy")
    else:
        return _resp(False, "Unable to add proxy")


@app.route("/proxy", methods=["GET"])
@with_authentication(admin=False)
@with_json("project")
def get_proxies(json_body: dict, user_doc: dict) -> Response:
    project_doc = db["projects"].find_one({"_id": json_body["project"], "users": {"$in": [user_doc["_id"]]}})
    if not project_doc:
        return _resp(False, "Project doesn't exist or unauthorized")

    return _resp(True, "Retrieved proxies", list(db["proxies"].find({"project": project_doc["_id"]})))


@app.route("/system", methods=["GET"])
@with_authentication(admin=False)
def get_system(user_doc: dict):
    # Update config doc
    config_doc = db["config"].find_one()

    # Get PoPs
    pops = []
    for idx, pop in enumerate(db["pops"].find()):
        if not user_doc.get("admin"):
            del pop["hosts"]
            del pop["_id"]
        pops.append(pop)

    return _resp(True, "Retrieved PoPs", data={
        "pops": pops,
        "plans": config_doc["plans"],
        "oses": config_doc["oses"]
    })


@app.route("/admin/pop", methods=["POST"])
@with_authentication(admin=True)
@with_json("name", "provider", "peeringdb_id")
def add_pop(json_body: dict, user_doc: dict) -> Response:
    try:
        new_pop = db["pops"].insert_one({
            "name": json_body["name"],
            "provider": json_body["provider"],
            "peeringdb_id": json_body["peeringdb_id"],
        })
    except DuplicateKeyError:
        return _resp(False, "PoP already exists")
    if new_pop.inserted_id:
        return _resp(True, f"PoP {json_body['name']} added")
    raise _resp(False, "Unable to create PoP")


@app.route("/admin/host", methods=["POST"])
@with_authentication(admin=True)
@with_json("ip", "pop")
def add_host(json_body: dict, user_doc: dict) -> Response:
    try:
        ipaddress.ip_address(json_body["ip"])
    except ValueError:
        return _resp(False, "Invalid IP address")

    pop_doc = db["pops"].find_one({"name": json_body["pop"]})
    if not pop_doc:
        return _resp(False, "PoP doesn't exist")

    if pop_doc.get("hosts"):
        for host in pop_doc.get("hosts"):
            if host["ip"] == json_body["ip"]:
                return _resp(False, f"Host with IP {json_body['ip']} already exists")

    host = {"ip": json_body["ip"]}

    # Get taken prefixes
    taken_prefixes = []
    for pop in db["pops"].find():
        if pop.get("hosts"):
            for host in pop.get("hosts"):
                taken_prefixes.append(host["prefix"])

    # Find next available prefix
    config_doc = db["config"].find_one()
    parent_prefix = ipaddress.ip_network(config_doc["prefix"], False)
    for slash48 in list(parent_prefix.subnets(new_prefix=48)):
        slash48 = str(slash48)
        if slash48 not in taken_prefixes:
            host["prefix"] = slash48
    if not host.get("prefix"):
        raise _resp(False, "No available prefixes to assign")

    new_host = db["pops"].update_one({"_id": pop_doc["_id"]}, {"$push": {"hosts": host}})
    if new_host.modified_count == 1:
        return _resp(True, "Host added")
    else:
        return _resp(False, "Unable to add host")


@app.route("/admin/bgp", methods=["POST"])
@with_authentication(admin=True)
@with_json("ip", "name", "asn", "neighbor")
def add_bgp_session(json_body: dict, user_doc: dict) -> Response:
    for pop in db["pops"].find():
        if pop.get("hosts"):
            for host_index, host in enumerate(pop.get("hosts")):
                if host["ip"] == json_body["ip"]:
                    print("Found host")
                    if not host.get("peers"):
                        host["peers"] = {}

                    host["peers"][json_body["name"]] = {
                        "asn": json_body["asn"],
                        "type": "import-valid",
                        "neighbors": [json_body["neighbor"]]
                    }

                    update = db["pops"].update_one({"_id": pop["_id"]}, {"$set": {"hosts." + str(host_index): host}})
                    if update.modified_count == 1:
                        return _resp(True, "Added BGP session")
                    else:
                        return _resp(False, "Unable to add BGP session")

    return _resp(False, "Unable to find host with provided IP")


@app.route("/admin/ansible", methods=["GET"])
@with_authentication(admin=True)
def get_ansible_hosts(user_doc: dict):
    # Update config doc
    config_doc = db["config"].find_one()

    proxies = []
    for proxy in db["proxies"].find():
        vm_doc = db["vms"].find_one(proxy["vm"])
        if vm_doc:
            proxies.append({
                "label": proxy["label"],
                "address": vm_doc["address"][:-3]
            })
        else:  # If proxy doesn't have a VM anymore, delete it
            db["proxies"].delete_one({"_id": proxy["_id"]})

    _config = {
        "all": {
            "vars": {
                "ansible_user": config_doc["user"],
                "ansible_port": config_doc["port"],
                "ansible_ssh_private_key_file": config_doc["key"],
                "oses": config_doc["oses"],
                "proxies": proxies,
                "parent_prefix": config_doc["prefix"]
            },
            "children": {
                "hypervisors": {"hosts": {}},
                "proxies": {"hosts": {}}
            }
        }
    }

    for pop in db["pops"].find():
        if pop.get("hosts"):
            for idx, host in enumerate(pop.get("hosts")):
                _config["all"]["children"]["hypervisors"]["hosts"][pop["name"] + str(idx)] = {
                    "ansible_host": host["ip"],
                    "bcg": {
                        "asn": config_doc["asn"],
                        "prefixes": [host["prefix"]],
                    },
                    "vms": list(db["vms"].find({"pop": pop["name"], "host": idx}))
                }

                if host.get("peers"):
                    _config["all"]["children"]["hypervisors"]["hosts"][pop["name"] + str(idx)]["bcg"]["peers"] = host.get("peers")

    for proxy in config_doc["proxies"]:
        _config["all"]["children"]["proxies"]["hosts"]["proxy." + proxy["pop"]] = {
            "ansible_port": 22,
            "ansible_host": proxy["ip"],
        }

    return _resp(True, "Retrieved ansible config", data=_config)


@app.route("/intra/phonehome", methods=["GET"])
def phone_home():
    client_ip = request.headers.get("X-Forwarded-For")
    if not client_ip:
        return _resp(False, "No header defined")

    vm_doc = db["vms"].find_one({"address": client_ip + "/64"})
    if not vm_doc:
        return _resp(False, "Unable to find VM")

    if not vm_doc.get("phoned_home"):
        db["vms"].update_one({"address": client_ip + "/64"}, {"$set": {"phoned_home": True}})
        user_doc = db["users"].find_one({"_id": vm_doc["created"]["by"]})
        send_email(user_doc["email"], "AARCH64: VM Created", f"""Hello,

Your AARCH64 VM is ready to go!

Address: {vm_doc["address"][:-3]}
Password: {vm_doc["password"]}

SSH is enabled on port 22 with root access, please secure your VM accordingly.

If you don't have IPv6 you can use our dualstack jumpbox:
ssh -J jump@proxy.dfw.aarch64.com root@{vm_doc["address"][:-3]}

Remote "Out of Band" SSH console:
ssh -p 2222 {vm_doc["_id"]}@{vm_doc["pop"]}{vm_doc["host"]}.aarch64.com

If you have any questions, please reach out via one of our contact methods at https://fosshost.org as this is a no-reply email address.

Best,
Fosshost Team
""")
    return _resp(True, "Phone home complete")


if DEBUG:
    print("Running API server in debug mode...")
    app.run(debug=True)

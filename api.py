import datetime
import ipaddress
import json
from functools import wraps
from os import environ
from secrets import token_hex

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

console = Console()
argon = PasswordHasher()

app = Flask(__name__)
db = MongoClient("mongodb://localhost:27017")["aarch64"]
db["users"].create_index([("email", ASCENDING)], background=True, unique=True)
db["pops"].create_index([("name", ASCENDING)], background=True, unique=True)

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


def to_object_id(object_id: str):
    """
    Cast object_id:str to ObjectId
    """

    try:
        return ObjectId(object_id)
    except InvalidId:
        return ""


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

    projects = list(db["projects"].find({
        "users": {
            "$in": [user_doc["_id"]]
        }
    }, {  # Ignore these keys
        "users": 0
    }))

    for project in projects:
        if not project.get("vms"):
            project["vms"] = []
        for vm in db["vms"].find({"project": project["_id"]}):
            project["vms"].append(vm)

    return _resp(True, "Retrieved project list", data=projects)


@app.route("/vms/create", methods=["POST"])
@with_authentication(admin=False)
@with_json("hostname", "plan", "pop", "project", "os")
def create_vm(json_body: dict, user_doc: dict) -> Response:
    pop_doc = db["pops"].find_one({"name": json_body["pop"]})
    if not pop_doc:
        return _resp(False, "PoP doesn't exist")

    # Update config doc
    config_doc = db["config"].find_one()

    if json_body["plan"] not in config_doc["plans"].keys():
        return _resp(False, "Plan doesn't exist")

    json_body["vcpus"] = config_doc["plans"][json_body["plan"]]["vcpus"]
    json_body["memory"] = config_doc["plans"][json_body["plan"]]["memory"]
    json_body["disk"] = config_doc["plans"][json_body["plan"]]["disk"]
    del json_body["plan"]

    if json_body["os"] not in config_doc["oses"].keys():
        return _resp(False, "OS doesn't exist")

    project_doc = db["projects"].find_one({
        "_id": to_object_id(json_body["project"]),
        "users": {
            "$in": [user_doc["_id"]]
        }
    })
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


@app.route("/vms/delete", methods=["DELETE"])
@with_authentication(admin=False)
@with_json("vm")
def delete_vm(json_body: dict, user_doc: dict) -> Response:
    vm_doc = db["vms"].find_one({"_id": to_object_id(json_body["vm"])})
    if not vm_doc:
        return _resp(False, "VM doesn't exist")

    project_doc = db["projects"].find_one({
        "_id": vm_doc["project"],
        "users": {
            "$in": [user_doc["_id"]]
        }
    })
    if not project_doc:
        return _resp(False, "Project doesn't exist or unauthorized")

    deleted_vm = db["vms"].delete_one({"_id": to_object_id(json_body["vm"])})
    if deleted_vm.deleted_count == 1:
        return _resp(True, "VM deleted")
    return _resp(False, "Unable to delete VM")


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
        "oses": list(config_doc["oses"].keys())
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

    _config = {
        "all": {
            "vars": {
                "ansible_user": config_doc["user"],
                "ansible_port": config_doc["port"],
                "ansible_ssh_private_key_file": config_doc["key"],
                "oses": config_doc["oses"]
            },
            "hosts": {}
        }
    }

    for pop in db["pops"].find():
        if pop.get("hosts"):
            for idx, host in enumerate(pop.get("hosts")):
                _config["all"]["hosts"][pop["name"] + str(idx)] = {
                    "ansible_host": host["ip"],
                    "bcg": {
                        "asn": config_doc["asn"],
                        "prefixes": [host["prefix"]],
                    },
                    "vms": list(db["vms"].find({"pop": pop["name"], "host": idx}))
                }

                if host.get("peers"):
                    _config["all"]["hosts"][pop["name"] + str(idx)]["bcg"]["peers"] = host.get("peers")

    return _resp(True, "Retrieved ansible config", data=_config)


@app.route("/intra/info", methods=["GET"])
def intra_info():
    for pop in db["pops"].find():
        if pop.get("hosts"):
            for host in pop.get("hosts"):
                if host["ip"] == request.headers.get("X-Forwarded-For"):
                    return _resp(True, "Retrieved host config", data=host)

    return _resp(False, "Unauthorized"), 403


if environ.get("AARCH64_DEBUG"):
    app.run(debug=True)

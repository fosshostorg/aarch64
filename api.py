import datetime
import ipaddress
import json
from functools import wraps
from secrets import token_hex
from typing import Optional

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from bson import ObjectId
from flask import Flask, request, Response, make_response
from pymongo import ASCENDING, MongoClient
from pymongo.errors import DuplicateKeyError, InvalidId
from rich.console import Console
from rich.traceback import install

install()  # Install rich traceback handler

VERSION = "0.0.1"

console = Console()
argon = PasswordHasher()

app = Flask(__name__)
db = MongoClient("mongodb://localhost:27017")["aarch64"]
db["users"].create_index([("email", ASCENDING)], background=True, unique=True)
db["pops"].create_index([("name", ASCENDING)], background=True, unique=True)


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


def with_authentication(func):
    """
    Require a user to be authenticated and pass user_doc to function
    :param func:
    :return:
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Get API key from header (default) or cookie (fallback)
        api_key = request.headers.get("Authorization")
        if not api_key:
            api_key = request.cookies.get("key")
        if not api_key:
            return _resp(False, "Not authenticated"), 403

        user_doc = db["users"].find_one({"key": api_key})
        if not user_doc:
            return _resp(False, "Not authenticated"), 403

        return func(*args, **kwargs, user_doc=user_doc)

    return decorated_function


@app.route("/auth/signup", methods=["POST"])
@with_json("email", "password")
async def signup(json_body: dict) -> Response:
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
            "name": json_body["name"],
            "role": json_body["role"],
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
            rsp = make_response(_resp(True, "Authentication successful", {
                "role": user["role"],
                "name": user["name"]
            }))
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


@app.route("/project", methods=["POST"])
@with_authentication
@with_json("name")
def create_project(json_body: dict, user_doc: dict) -> Response:
    if not json_body.get("name"):
        return _resp(False, "Project name must exist")

    project = db["projects"].insert_one({
        "name": json_body["name"],
        "users": user_doc["_id"]
    })

    return _resp(True, "Project created", str(project.inserted_id))


@app.route("/projects", methods=["GET"])
@with_authentication
def projects_list(user_doc: dict) -> Response:
    """
    Get all projects that a user is part of
    """

    projects = list(db["projects"].find({
        "users": {
            "$in": [str(user_doc["_id"])]
        }
    }, {  # Ignore these keys
        "users": 0
    }))

    return _resp(True, "Retrieved project list", data=projects)


@app.post("/vms/create", response_model=VMResponse)
async def create_vm(vm: VM, x_token: Optional[str] = Header(None), api_key: Optional[str] = Cookie(None)):
    user_doc = await db["users"].find_one({"api_key": x_token if x_token else api_key})
    if not user_doc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't exist")

    project_doc = await db["projects"].find_one({"_id": database.to_object_id(vm.project)})
    if not project_doc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project not found")

    if not str(user_doc["_id"]) in project_doc["users"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized for project")

    _vm = vm.dict()

    pop_doc = await db["pops"].find_one({"name": _vm["pop"]})
    if not pop_doc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PoP doesn't exist")

    # Calculate host usage for pop
    _host_usage = {}
    for idx, host in enumerate(pop_doc["hosts"]):
        if idx not in _host_usage:
            _host_usage[idx] = 0

        # async for host_vm in db["vms"].find({"pop": _vm["pop"], "host": idx}):
        #     vm_plan_spec = plans[host_vm["plan"]]
        #     _host_usage[idx] += (vm_plan_spec["vcpus"] + vm_plan_spec["memory"])

    # Sort host usage dict by value (ordered from least used to greatest)
    _host_usage = {k: v for k, v in sorted(_host_usage.items(), key=lambda item: item[1])}

    # Find the least utilized host by taking the first element (call next on iter)
    _vm["host"] = next(iter(_host_usage))

    # Find taken prefixes
    taken_prefixes = []
    async for vm in db["vms"].find({"pop": _vm["pop"]}):
        taken_prefixes.append(vm["prefix"])

    # Iterate over the selected host's prefix
    host_prefix = pop_doc["hosts"][_vm["host"]]["prefix"]
    for prefix in list(ipaddress.ip_network(host_prefix).subnets(new_prefix=64)):
        prefix = str(prefix)
        if prefix not in taken_prefixes:
            _vm["prefix"] = prefix
    if not _vm.get("prefix"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to assign VM prefix")

    new_vm = await db["vms"].insert_one(_vm)
    if new_vm.inserted_id:
        return Response(status_code=status.HTTP_200_OK, content=VMResponse(**_vm))  # TODO: Make this fit the fields

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to create VM")

# @app.get("/pops")
# async def get_pops(x_token: Optional[str] = Header(None), api_key: Optional[str] = Cookie(None)):
#     user_doc = await db["users"].find_one({"api_key": x_token if x_token else api_key})
#     if not user_doc:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
#
#     pops = []
#     async for pop in db["pops"].find():
#         if user_doc.get("admin"):
#             pops.append(pop)
#         else:
#             del pop["hosts"]
#             del pop["_id"]
#             pops.append(pop)
#
#     return Response(status_code=status.HTTP_200_OK, content=pops)

#
# @app.post("/admin/pop")
# async def add_pop(pop: PoP, x_token: Optional[str] = Header(None), api_key: Optional[str] = Cookie(None)):
#     user_doc = await db["users"].find_one({"api_key": x_token if x_token else api_key, "admin": True})
#     if not user_doc:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
#
#     try:
#         new_pop = await db["pops"].insert_one(pop.dict())
#     except DuplicateKeyError:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="PoP with this name already exists")
#     if new_pop.inserted_id:
#         return Response(status_code=status.HTTP_200_OK, content={"detail": f"PoP {pop.name} added"})
#     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to create pop")
#
#
# @app.post("/admin/host")
# async def add_host(host: Host, x_token: Optional[str] = Header(None), api_key: Optional[str] = Cookie(None)):
#     user_doc = await db["users"].find_one({"api_key": x_token if x_token else api_key, "admin": True})
#     if not user_doc:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
#
#     # Cast IP types to string
#     _host = host.dict()
#     _host["ip"] = str(_host["ip"])
#
#     # Get taken prefixes
#     taken_prefixes = []
#     async for pop in db["pops"].find():
#         if pop.get("hosts"):
#             for host in pop.get("hosts"):
#                 taken_prefixes.append(host["prefix"])
#
#     # Find next available prefix
#     config_doc = await db["config"].find_one()
#     parent_prefix = ipaddress.ip_network(config_doc["prefix"])
#     for slash48 in list(parent_prefix.subnets(new_prefix=48)):
#         slash48 = str(slash48)
#         if slash48 not in taken_prefixes:
#             _host["prefix"] = slash48
#     if not _host.get("prefix"):
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No available prefixes to assign")
#
#     new_host = await db["pops"].update_one({"name": _host["pop"]}, {"$push": {"hosts": _host}})
#
#     if new_host.matched_count == 1:
#         return Response(status_code=status.HTTP_200_OK, content={"detail": f"Host added"})
#     else:
#         raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"PoP {host.pop} doesn't exist")
#
#
# @app.get("/admin/ansible")
# async def get_ansible_hosts(x_token: Optional[str] = Header(None), api_key: Optional[str] = Cookie(None)):
#     user_doc = await db["users"].find_one({"api_key": x_token if x_token else api_key, "admin": True})
#     if not user_doc:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
#
#     config_doc = await db["config"].find_one()
#     _config = {
#         "all": {
#             "vars": {
#                 "ansible_user": config_doc["user"],
#                 "ansible_port": config_doc["port"],
#                 "ansible_ssh_private_key_file": config_doc["key_file"]
#             },
#             "hosts": {}
#         }
#     }
#
#     async for pop in db["pops"].find():
#         if pop.get("hosts"):
#             for idx, host in enumerate(pop.get("hosts")):
#                 _config["all"]["hosts"][pop["name"] + str(idx)] = {
#                     "ansible_host": host["ip"]
#                 }
#
#     return Response(status_code=status.HTTP_200_OK, content=_config)

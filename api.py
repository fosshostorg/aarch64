import ipaddress
from json import JSONEncoder, dumps
from secrets import token_hex
from typing import Optional

from argon2 import PasswordHasher
from bson import json_util
from fastapi import FastAPI, status, HTTPException, Header, Cookie
from pydantic import typing
from pymongo import ASCENDING
from pymongo.errors import DuplicateKeyError
from rich.console import Console
from rich.traceback import install
from starlette.responses import Response as StarletteResponse, RedirectResponse

import database
from models.admin import PoP, Host
from models.user import User, Project
from models.vm import plans, VMRequest

install()  # Install rich traceback handler

VERSION = "0.0.1"

console = Console()
argon = PasswordHasher()

app = FastAPI(title="aarch64", version=VERSION)
db = database.get()
db["users"].create_index([("email", ASCENDING)], background=True, unique=True)
db["pops"].create_index([("name", ASCENDING)], background=True, unique=True)


class SafeJSONEncoder(JSONEncoder):
    """
    BSON-safe JSON response encoder
    """

    def default(self, obj):
        return json_util.default(obj)


class Response(StarletteResponse):
    """
    Response implements a starlette.responses.Response to encode BSON-safe JSON with SafeJSONEncoder
    """

    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            cls=SafeJSONEncoder,
        ).encode("utf-8")


@app.on_event("shutdown")
async def shutdown():
    db.close()


@app.get("/")
async def index():
    return RedirectResponse(url="/docs")


@app.post("/auth/signup")
async def signup(user: User):
    _user = user.dict()
    _user["api_key"] = str(token_hex(32))
    _user["password"] = argon.hash(_user["password"])
    try:
        new_user = await db["users"].insert_one(_user)
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")
    if new_user.inserted_id:
        return Response(status_code=status.HTTP_200_OK, content={"detail": "User created"})
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to create user")


@app.post("/auth/login")
async def login(user: User):
    user_doc = await db["users"].find_one({"email": user.email})
    if not user_doc or not argon.verify(user_doc["password"], user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    response = Response(status_code=status.HTTP_200_OK, content=user_doc["api_key"])
    response.set_cookie("api_key", user_doc["api_key"], httponly=True, secure=True, max_age=2628000)  # 1 month expiration
    return response


@app.post("/auth/logout")
async def logout():
    response = Response(status_code=status.HTTP_200_OK, content="")
    response.set_cookie("api_key", "", httponly=True, secure=True, max_age=0)  # Immediate expiration
    return response


@app.post("/project")
async def create_project(project: Project, x_token: Optional[str] = Header(None), api_key: Optional[str] = Cookie(None)):
    user_doc = await db["users"].find_one({"api_key": x_token if x_token else api_key})
    if not user_doc:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't exist")

    _project = project.dict()
    _project["users"] = [str(user_doc["_id"])]

    new_project = await db["projects"].insert_one(_project)
    if new_project.inserted_id:
        return Response(status_code=status.HTTP_200_OK, content={"detail": f"Projected created"})

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to create project")


@app.get("/projects")
async def get_projects(x_token: Optional[str] = Header(None), api_key: Optional[str] = Cookie(None)):
    user_doc = await db["users"].find_one({"api_key": x_token if x_token else api_key})
    if not user_doc:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't exist")

    projects = []
    async for project in db["projects"].find({
        "users": {
            "$in": [str(user_doc["_id"])]
        }
    }, {  # Ignore these keys
        "users": 0
    }):
        projects.append(project)

    return Response(status_code=status.HTTP_200_OK, content=projects)


@app.post("/vms/create")
async def create_vm(vm: VMRequest, x_token: Optional[str] = Header(None), api_key: Optional[str] = Cookie(None)):
    user_doc = await db["users"].find_one({"api_key": x_token if x_token else api_key})
    if not user_doc:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't exist")

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

        async for host_vm in db["vms"].find({"pop": _vm["pop"], "host": idx}):
            vm_plan_spec = plans[host_vm["plan"]]
            _host_usage[idx] += (vm_plan_spec["vcpus"] + vm_plan_spec["memory"])

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
        return Response(status_code=status.HTTP_200_OK, content={"detail": f"VM added"})

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to create VM")


@app.post("/admin/pop")
async def add_pop(pop: PoP, x_token: Optional[str] = Header(None), api_key: Optional[str] = Cookie(None)):
    user_doc = await db["users"].find_one({"api_key": x_token if x_token else api_key, "admin": True})
    if not user_doc:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    try:
        new_pop = await db["pops"].insert_one(pop.dict())
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="PoP with this name already exists")
    if new_pop.inserted_id:
        return Response(status_code=status.HTTP_200_OK, content={"detail": f"PoP {pop.name} added"})
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to create pop")


@app.post("/admin/host")
async def add_host(host: Host, x_token: Optional[str] = Header(None), api_key: Optional[str] = Cookie(None)):
    user_doc = await db["users"].find_one({"api_key": x_token if x_token else api_key, "admin": True})
    if not user_doc:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    # Cast IP types to string
    _host = host.dict()
    _host["ip"] = str(_host["ip"])

    # Get taken prefixes
    taken_prefixes = []
    async for pop in db["pops"].find():
        if pop.get("hosts"):
            for host in pop.get("hosts"):
                taken_prefixes.append(host["prefix"])

    # Find next available prefix
    config_doc = await db["config"].find_one()
    parent_prefix = ipaddress.ip_network(config_doc["prefix"])
    for slash48 in list(parent_prefix.subnets(new_prefix=48))[::-1]:
        slash48 = str(slash48)
        if slash48 not in taken_prefixes:
            _host["prefix"] = slash48
    if not _host.get("prefix"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No available prefixes to assign")

    new_host = await db["pops"].update_one({"name": _host["pop"]}, {"$push": {"hosts": _host}})

    if new_host.matched_count == 1:
        return Response(status_code=status.HTTP_200_OK, content={"detail": f"Host added"})
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"PoP {host.pop} doesn't exist")


@app.get("/admin/ansible")
async def get_ansible_hosts(x_token: Optional[str] = Header(None), api_key: Optional[str] = Cookie(None)):
    user_doc = await db["users"].find_one({"api_key": x_token if x_token else api_key, "admin": True})
    if not user_doc:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    config_doc = await db["config"].find_one()
    _config = {
        "all": {
            "vars": {
                "ansible_user": config_doc["user"],
                "ansible_port": config_doc["port"],
                "ansible_ssh_private_key_file": config_doc["key_file"]
            },
            "hosts": {}
        }
    }

    async for pop in db["pops"].find():
        if pop.get("hosts"):
            for idx, host in enumerate(pop.get("hosts")):
                _config["all"]["hosts"][pop["name"] + str(idx)] = {
                    "ansible_host": host["ip"]
                }

    return Response(status_code=status.HTTP_200_OK, content=_config)

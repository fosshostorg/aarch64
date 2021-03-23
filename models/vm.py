from pydantic import BaseModel, validator

plans = {
    "v1.small.arm": {
        "vcpus": 1,
        "memory": 1,
        "disk": 5
    },
    "v1.medium.arm": {
        "vcpus": 2,
        "memory": 4,
        "disk": 15
    },
    "v1.large.arm": {
        "vcpus": 4,
        "memory": 8,
        "disk": 20
    },
    "v1.xlarge.arm": {
        "vcpus": 8,
        "memory": 16,
        "disk": 50
    }
}

_oses = ["debian", "ubuntu"]


class VMRequest(BaseModel):
    hostname: str
    plan: str
    os: str
    pop: str

    class Config:
        schema_extra = {
            "example": {
                "hostname": "db1.example.com",
                "plan": "v1.small.arm",
                "os": "debian",
                "pop": "dfw"
            }
        }

    @validator("plan")
    def plan_validator(v):
        if not plans.get(v):
            raise ValueError(f"Plan {v} doesn't exist")
        return v

    @validator("os")
    def os_validator(v):
        if v not in _oses:
            raise ValueError(f"OS {v} doesn't exist")
        return v

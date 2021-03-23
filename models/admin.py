from ipaddress import IPv6Network

from pydantic import BaseModel, IPvAnyAddress, validator


class PoP(BaseModel):
    name: str
    provider: str
    location: str
    peeringdb_id: int

    class Config:
        schema_extra = {
            "example": {
                "name": "dfw",
                "provider": "Equinix Metal",
                "location": "Dallas, TX",
                "peeringdb_id": 4
            }
        }


class Host(BaseModel):
    pop: str
    ip: IPvAnyAddress
    prefix: IPv6Network

    class Config:
        schema_extra = {
            "example": {
                "pop": "dfw",
                "ip": "192.0.2.1",
                "prefix": "2001:db8::/48"
            }
        }

    @validator("prefix")
    def prefix_validator(v):
        if v.prefixlen > 48:
            raise ValueError("Prefix length must be <= 48")
        return v

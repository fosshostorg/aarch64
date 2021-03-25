from pymongo import MongoClient

db = MongoClient("mongodb://localhost:27017")["aarch64"]

db["config"].update_one({}, {"$set": {
    "prefix": "2001:db8::/42",
    "plans": {
        "v1.xsmall.aarch64": {
            "vcpus": 1,
            "memory": 1,
            "disk": 4
        },
        "v1.small.aarch64": {
            "vcpus": 2,
            "memory": 4,
            "disk": 8
        },
        "v1.medium.aarch64": {
            "vcpus": 4,
            "memory": 8,
            "disk": 16
        },
        "v1.large.aarch64": {
            "vcpus": 8,
            "memory": 16,
            "disk": 32
        },
        "v1.xlarge.aarch64": {
            "vcpus": 16,
            "memory": 32,
            "disk": 64
        }
    },
    "oses": {
        "debian": "https://cdimage.debian.org/cdimage/openstack/current/debian-10-openstack-arm64.qcow2",
        "ubuntu": "https://cloud-images.ubuntu.com/groovy/current/groovy-server-cloudimg-arm64.img"
    }
}})

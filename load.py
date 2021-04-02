from pymongo import MongoClient

db = MongoClient("mongodb://localhost:27017")["aarch64"]

db["config"].update_one({}, {"$set": {
    "prefix": "2001:db8::/42",
    "plans": {
        "v1.xsmall": {
            "vcpus": 1,
            "memory": 1,
            "ssd": 4
        },
        "v1.small": {
            "vcpus": 2,
            "memory": 4,
            "ssd": 8
        },
        "v1.medium": {
            "vcpus": 4,
            "memory": 8,
            "ssd": 16
        },
        "v1.large": {
            "vcpus": 8,
            "memory": 16,
            "ssd": 32
        },
        "v1.xlarge": {
            "vcpus": 16,
            "memory": 32,
            "ssd": 64
        }
    },
    "oses": {
        "debian": {
            "version": "10.8",
            "url": "https://cdimage.debian.org/cdimage/openstack/current/debian-10-openstack-arm64.qcow2"
        },
        "ubuntu": {
            "version": "20.10",
            "url": "https://cloud-images.ubuntu.com/groovy/current/groovy-server-cloudimg-arm64.img"
        }
    }
}})

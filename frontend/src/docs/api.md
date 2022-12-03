---
id: api
---

# API

AARCH64.com has a public RESTful API for automating the use of the platform.

Native clients are also available:

| Language | Client                                                                      |
| :------- | :-------------------------------------------------------------------------- |
| Python   | [aarch64-client-python](https://github.com/natesales/aarch64-client-python) |
| Go       | [aarch64-client-go](https://github.com/natesales/aarch64-client-go)         |

## API Reference

All routes return a JSON object with `meta` and `data` keys. `meta` will always contain a `success` boolean and a `message` string, and `data` optionally contains additional data specific to individual API routes.

```json
{
	"meta": {
		"success": true,
		"message": "A short description of what went wrong or right"
	},
	"data": {}
}
```

### Authentication

POST `/auth/signup`

Request body:

```json
{
	"email": "user@example.com",
	"password": "OCfF23Jg0g0us0LQmg0us0LQm2SkD"
}
```

POST `/auth/login`

Request body:

```json
{
	"email": "user@example.com",
	"password": "OCfF23Jg0g0us0LQmg0us0LQm2SkD"
}
```

Response body:

```json
{
    "meta": {
        "success": true,
        "message": "Authentication successful"
    },
    "data": {
        "key": "cfea63484ccfea63484bfe78ed72d2cbfe78eea63484bfe78e"
    }
}
```

POST `/auth/logout`

Request body: `None`

GET `/auth/user`

Request body: `None`

Response body:

```json
{
	"meta": {
		"success": true,
		"message": "Retrieved user info"
	},
	"data": {
		"_id": "605d72d2ccfea63484bfe78e",
		"email": "user@example.com",
		"key": "cfea63484ccfea63484bfe78ed72d2cbfe78eea63484bfe78e"
	}
}
```

### Project

POST `/project`

Authentication required

Request body:

```json
{
	"name": "My Project Name",
	"budget": 4
}
```

Response body:

```json
{
	"meta": {
		"success": true,
		"message": "Project created"
	},
	"data": "605d72d2ccfea63484bfe78e"
}
```

DELETE `/project`

Authentication required

Request body:

```json
{
	"project": "605fdf474177beeb253eed4a"
}
```

GET `/projects`

Authentication required

Request body: `None`

Response body:

```json
{
	"meta": {
		"success": true,
		"message": "Retrieved project list"
	},
	"data": [
		{
			"_id": "605d1fbc361f9e55eec97986",
			"name": "Test Project",
			"users": ["user1@example.com", "user2@example.com"],
			"budget": 6,
			"budget_used": 4,
			"vms": [
				{
					"hostname": "testvm1",
					"vcpus": 4,
					"memory": 8,
					"ssd": 16,
					"pop": "dfw",
					"project": "605d1fbc361f9e55eec97986",
					"host": 0,
					"index": 0,
					"prefix": "2001:db8:ffff::/64",
					"gateway": "2001:db8:ffff::1",
					"address": "2001:db8:ffff::2/64",
					"os": "debian",
					"_id": "605d1fea3c05da2790ea3dbb",
					"password": "3c05da2790ea3d3c05da2790ea3d3c05da2790ea3d",
					"phoned_home": true
				}
			]
		}
	]
}
```

POST `/project/adduser`

Authentication required

Request body:

```json
{
	"project": "605fdf474177ba62253eed4a",
	"email": "user2@example.com"
}
```

DELETE `/project/removeuserself`

Authentication required

Request body:

```json
{
      "project": "605fdf474177ba62253eed4a",
      "email": "user2@example.com"
}
```

POST `/project/changeuser`

Authentication required

Request body:

```json
{
	"project": "605fdf474177ba62253eed4a",
	"budget": 28
}
```

### VMs

POST `/vms/create`

Authentication required

Request body:

```json
{
	"hostname": "testvm1",
	"pop": "dfw",
	"project": "605d1fbc361f9e55eec97986",
	"plan": "v1.medium.aarch64",
	"os": "debian"
}
```

Response body:

```json
{
	"meta": {
		"success": true,
		"message": "VM created"
	},
	"data": {
		"hostname": "testvm1",
		"vcpus": 4,
		"memory": 8,
		"ssd": 16,
		"pop": "dfw",
		"project": "605d1fbc361f9e55eec97986",
		"host": 0,
		"index": 0,
		"os": "debian",
		"prefix": "2001:db8:ffff::/64",
		"gateway": "2001:db8:ffff::1",
		"address": "2001:db8:ffff::2/64",
		"_id": "605d1fea3c05da2790ea3dbb",
		"password": "3c05da2790ea3d3c05da2790ea3d3c05da2790ea3d",
		"phoned_home": false
	}
}
```

DELETE `/vms/delete`

Authentication required

Request body:

```json
{
	"vm": "605fdf4e4177beeb253eed4b"
}
```

Response body:

```json
{
	"meta": {
		"success": true,
		"message": "VM deleted"
	},
	"data": null
}
```

POST `/vms/start`

Authentication required

Request body:

```json
{
	"vm": "605fdf4e4177beeb253eed4b"
}
```

Response body:

```json
{
	"meta": {
		"success": true,
		"message": "VM has been started"
	},
	"data": null
}
```

POST `/vms/shutdown`

Authentication required

Request body:

```json
{
	"vm": "605fdf4e4177beeb253eed4b"
}
```

Response body:

```json
{
	"meta": {
		"success": true,
		"message": "VM has been shutdown"
	},
	"data": null
}
```

POST `/vms/reboot`

Authentication required

Request body:

```json
{
	"vm": "605fdf4e4177beeb253eed4b"
}
```

Response body:

```json
{
	"meta": {
		"success": true,
		"message": "VM has been rebooted"
	},
	"data": null
}
```

POST `/vms/stop`

Authentication required

Request body:

```json
{
	"vm": "605fdf4e4177beeb253eed4b"
}
```

Response body:

```json
{
	"meta": {
		"success": true,
		"message": "VM has been stopped"
	},
	"data": null
}
```

POST `/vms/reset`

Authentication required

Request body:

```json
{
	"vm": "605fdf4e4177beeb253eed4b"
}
```

Response body:

```json
{
	"meta": {
		"success": true,
		"message": "VM has been reset"
	},
	"data": null
}
```

### System

GET `/system`

Authentication required

Request body: `None`

Response body:

```json
{
	"meta": {
		"success": true,
		"message": "Retrieved PoPs"
	},
	"data": {
		"pops": [
			{
				"_id": "605a8ee1cdf6bb6559de1cb7",
				"name": "dfw",
				"provider": "Equinix Metal",
				"location": "Dallas, TX",
				"peeringdb_id": 4
			}
		],
		"plans": {
			"v1.xsmall.aarch64": {
				"vcpus": 1,
				"memory": 1,
				"ssd": 4
			},
			"v1.small.aarch64": {
				"vcpus": 2,
				"memory": 4,
				"ssd": 8
			},
			"v1.medium.aarch64": {
				"vcpus": 4,
				"memory": 8,
				"ssd": 16
			},
			"v1.large.aarch64": {
				"vcpus": 8,
				"memory": 16,
				"ssd": 32
			},
			"v1.xlarge.aarch64": {
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
	}
}
```

### Proxy

POST `/proxy`

Authentication required

Request body:

```json
{
	"vm": "60641b57f50d8e43cfc9dfb7",
	"label": "test.example.com"
}
```

GET `/proxies/<project_id>`

Authentication required

Response body:

```json
{
	"meta": {
		"success": true,
		"message": "Retrieved proxies"
	},
	"data": [
		{
			"_id": "f9e55eec9605d1fbd1fbc361",
			"project": "605d1fbc361f9e55eec97986",
			"label": "example.com",
			"vm": "d1fbc361f9e5e55361f9e5e55e"
		}
	]
}
```

DELETE `/proxy`

Authentication required

Request body:

```json
{
	"proxy": "f9e55eec9605d1fbd1fbc361"
}
```

GET `/project/<project_id>/audit`

Authentication required

Request body: None

Response: List of audit entries

```json
{
	"meta": {
		"success": true,
		"message": "Retrieved audit log"
	},
	"data": [
		{
			"_id": "M9GLKcDhV0cKVM67wG8G5UGQW",
			"time": 1621724859.4778383,
			"title": "project.create",
			"user_id": "QGVfv/UlkuIGTQXkNLSzkBM",
			"user_name": "nate@fosshost.org",
			"project_id": "JefGMbQDMsK9pAEn6CBhhVyO8L0F6",
			"project_name": "Fosshost"
		},
		{
			"_id": "6ilwo3pufTwFtkK/Ws32tdje880OWQ5",
			"time": 1621454880.3627973,
			"title": "vm.delete",
			"vm_id": "BZhCT8qLco759IT2BcqCWcXsB6Z",
			"vm_name": "test.example.com",
			"project_id": "JefGMbQDMsK9pAEn6CBhhVyO8L0F6",
			"project_name": "Fosshost",
			"user_id": "QGVfv/UlkuIGTQXkNLSzkBM",
			"user_name": "nate@fosshost.org"
		}
	]
}
```

### Admin

POST `/admin/pop`

Admin authentication required

Request body:

```json
{
	"name": "dfw",
	"provider": "Equinix Metal",
	"location": "Dallas, TX",
	"peeringdb_id": 4
}
```

POST `/admin/host`

Admin authentication required

Request body:

```json
{
	"pop": "dfw",
	"ip": "192.0.2.1"
}
```

GET `/admin/ansible`

Admin authentication required

Request body: Ansible config in JSON format

POST `/admin/bgp`

Admin authentication required

Request body:

```json
{
	"ip": "192.0.2.3",
	"name": "Transit",
	"asn": 65530,
	"neighbor": "192.0.2.100"
}
```

GET `/admin/audit`

Admin authentication required

Request body: None

Response: List of audit entries

```json
{
	"meta": {
		"success": true,
		"message": "Retrieved audit log"
	},
	"data": [
		{
			"_id": "M9GLKcDhV0cKVM67wG8G5UGQW",
			"time": 1621724859.4778383,
			"title": "project.create",
			"user_id": "QGVfv/UlkuIGTQXkNLSzkBM",
			"user_name": "nate@fosshost.org",
			"project_id": "JefGMbQDMsK9pAEn6CBhhVyO8L0F6",
			"project_name": "Fosshost"
		},
		{
			"_id": "6ilwo3pufTwFtkK/Ws32tdje880OWQ5",
			"time": 1621454880.3627973,
			"title": "vm.delete",
			"vm_id": "BZhCT8qLco759IT2BcqCWcXsB6Z",
			"vm_name": "test.example.com",
			"project_id": "JefGMbQDMsK9pAEn6CBhhVyO8L0F6",
			"project_name": "Fosshost",
			"user_id": "QGVfv/UlkuIGTQXkNLSzkBM",
			"user_name": "nate@fosshost.org"
		}
	]
}
```

### Internal

GET `/intra/phonehome`

Request body: `None`

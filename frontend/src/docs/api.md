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
	"name": "My Project Name"
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
			"vms": [
				{
					"hostname": "testvm1",
					"vcpus": 4,
					"memory": 8,
					"disk": 16,
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
		"disk": 16,
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

### Internal

GET `/intra/phonehome`

Request body: `None`

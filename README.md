# aarch64 Control Plane

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

### Project

POST `/project`

Authentication required

Request body:
```json
{
    "name": "My Project Name"
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
            "vms": [
                {
                "_id": "605d1fea3c05da2790ea3dbb",
                "hostname": "testvm1",
                "plan": "v1.medium.aarch64",
                "pop": "dfw",
                "project": "605d1fbc361f9e55eec97986",
                "host": 0,
                "prefix": "2001:db8:ffff::/64"
                }
            ]
        }
    ]
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
    "plan": "v1.medium.aarch64"
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
        "plan": "v1.medium.aarch64",
        "pop": "dfw",
        "project": "605d1fbc361f9e55eec97986",
        "host": 0,
        "prefix": "2001:db8:ffff::/64",
        "_id": "605d1fea3c05da2790ea3dbb"
    }
}
```

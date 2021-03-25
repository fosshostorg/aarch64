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

Request body:
```json
{
  "name": "My Project Name"
}
```

GET `/projects`

Request body: `None`

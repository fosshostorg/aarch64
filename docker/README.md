# Setting up a dev environment!

If this is your first time using it, add AARCH64_DEV_CONFIG_DATABASE: "true" to the docker-compose for the `backend` service.

`docker-compose up -d --build`

Make an account using the webui (port 8080), use mongo-express (port 8081) to make your account admin.

Run the following 2 fetch requests once logged in as admin.

This creates the test POP
```
fetch('/api/admin/pop', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
        name: "test",
        provider: "test",
        location: "Test, World",
        peeringdb_id: 30
    }),
})
```

This adds a host to the POP.

```
fetch('/api/admin/host', {
  method: 'POST', // or 'PUT'
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
        "pop": "test",
        "ip": "192.0.2.1"
    }),
})
```
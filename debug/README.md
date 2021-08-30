# Debugging / development instructions

## Frontend debugging/development instructions 

Here we assume that you have npm, nodejs, docker and docker-compose available.

1. Run `docker-compose build && docker-compose up` to build & run the development CORS-bypass proxy 
   
   (use `docker-compose up -d` to run in the background).

2. cd into the frontend directory.
3. run `npm install`
4. run `npm run dev` to start the development server.

## Notes
### Backend debugging/development
The CORS-bypass proxy is not needed here, since the proxy queries https://console.aarch64.com/api .
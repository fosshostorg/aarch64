FROM golang:1.18.3-alpine3.15

WORKDIR /usr/src/app

COPY ./api ./
RUN go mod init && go build

CMD [ "./api" ]

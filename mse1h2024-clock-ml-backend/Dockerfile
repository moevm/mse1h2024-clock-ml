FROM golang:1.22-alpine AS builder

WORKDIR /build

ADD go.mod .
ADD go.sum .
RUN go mod download

COPY . .

RUN go build -o main cmd/main/main.go

FROM alpine

WORKDIR /build

COPY --from=builder /build/main /build/main

ADD config/config.yaml config.yaml
ENV CFG_PATH /build/config.yaml

EXPOSE 746

CMD ["./main"]

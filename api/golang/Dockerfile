FROM golang:latest as builder

WORKDIR /app

COPY go.mod ./

RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o myapp .

FROM alpine:latest

WORKDIR /app

COPY --from=builder /app/myapp .

EXPOSE 8000

CMD ["./myapp"]
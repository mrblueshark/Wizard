# 1. Build Stage
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copy go.mod and go.sum to cache dependencies
COPY go.mod .
# COPY go.sum . # Not necessary if go.mod is sufficient for go get

# Download dependencies
# We need to install the gRPC and protobuf packages
RUN go get -d ./...

# Copy all source code
COPY . .

# Build the application
# CGO_ENABLED=0 builds a static executable
RUN go build -ldflags "-s -w" -o /collector ./main.go

# 2. Production Stage
FROM alpine:latest

WORKDIR /root/

# Copy the static binary from the builder stage
COPY --from=builder /collector .

# The entrypoint runs the compiled Go application
CMD ["/collector"]
# --- STAGE 1: Builder Stage ---

# Use a full Go image for building
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copy dependency files
COPY go.mod .
COPY go.sum .

# Download and tidy up Go modules
RUN go mod download
RUN go mod tidy

# Copy application source code
COPY cmd cmd
COPY collector collector
COPY pkg pkg

# FIX: Explicitly install the missing 'github.com/google/uuid' dependency
# This resolves the 'no required module provides package' error.
RUN go get github.com/google/uuid

# Build the Go application, statically linked
# Using '-mod=readonly' now that all dependencies are accounted for.
RUN CGO_ENABLED=0 go build -mod=readonly -o /usr/local/bin/collector ./cmd/wizard


# --- STAGE 2: Final Runtime Stage ---

# Use a minimal Alpine image for the final container (smaller footprint)
FROM alpine:latest

# Install ca-certificates required for HTTPS communication (Go Kafka library needs this)
RUN apk --no-cache add ca-certificates

WORKDIR /app

# Copy the built binary from the builder stage
COPY --from=builder /usr/local/bin/collector /usr/local/bin/collector

# Command to run the application
CMD ["/usr/local/bin/collector"]

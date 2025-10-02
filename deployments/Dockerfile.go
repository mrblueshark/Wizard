# File: Dockerfile.go

# --- STAGE 1: Build Stage ---
# Use a full Go image for building (contains compiler, tools, etc.)
FROM golang:1.21-alpine AS builder

# Set necessary environment variables
ENV CGO_ENABLED=0 \
    GOOS=linux

# Set the working directory inside the container
WORKDIR /app/go

# Copy go.mod and go.sum files first to cache dependencies
COPY go/go.mod .
COPY go/go.sum .

# Download dependencies
RUN go mod download

# Copy the rest of the Go source code
COPY go/ .

# Build the Go application, generating a static binary named 'wizard-collector'
# The '-a' flag forces rebuilding packages, '-installsuffix cgo' ensures CGO is disabled
RUN go build -ldflags "-s -w" -o /usr/local/bin/wizard-collector ./cmd/wizard/main.go

# --- STAGE 2: Final (Minimal) Stage ---
# Use a super-minimal, secure base image (no shell, minimal attack surface)
FROM scratch

# Set the Timezone database for accurate time operations (optional but recommended)
COPY --from=builder /usr/share/zoneinfo/Etc/UTC /etc/localtime

# Copy the static binary from the build stage
COPY --from=builder /usr/local/bin/wizard-collector /usr/local/bin/wizard-collector

# Expose the service port (assuming the Go app listens here)
EXPOSE 8080

# Run the compiled binary
ENTRYPOINT ["/usr/local/bin/wizard-collector"]
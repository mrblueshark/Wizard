package app

// CollectorConfig holds configuration details for the collector service.
type CollectorConfig struct {
	// Address of the gRPC storage service (Matches the service name in docker-compose)
	StorageServiceAddr string
}

// LoadConfig simulates loading configuration (e.g., from environment variables or a file).
func LoadConfig() CollectorConfig {
	return CollectorConfig{
		// Note: The Docker Compose file sets this environment variable.
		StorageServiceAddr: "storage:50051", 
	}
}

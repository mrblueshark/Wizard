package app

import (
	"os"
	"log"
	"time"
	"strconv"
)

// CollectorConfig holds configuration details for the collector service.
type CollectorConfig struct {
	// Address of the gRPC storage service
	StorageServiceAddr string
	// Interval between simulated packet dispatches
	CollectionInterval time.Duration
}

// LoadConfig loads configuration from environment variables.
func LoadConfig() CollectorConfig {
	// 1. Get Storage Address
	storageAddr := os.Getenv("STORAGE_SERVICE_ADDRESS")
	storagePort := os.Getenv("STORAGE_SERVICE_PORT")
	
	if storageAddr == "" || storagePort == "" {
		// Log.Fatal is robust error handling as per Phase 3 requirements
		log.Fatal("FATAL: STORAGE_SERVICE_ADDRESS and STORAGE_SERVICE_PORT must be set in the environment.")
	}
	
	// 2. Get Collection Interval
	intervalSecsStr := os.Getenv("COLLECTOR_INTERVAL_SECONDS")
	
	intervalSecs := 2 // Default to 2 seconds
	if intervalSecsStr != "" {
		var err error
		// Using strconv.Atoi to safely parse the environment variable
		intervalSecs, err = strconv.Atoi(intervalSecsStr)
		if err != nil {
			log.Printf("Warning: Invalid COLLECTOR_INTERVAL_SECONDS '%s'. Defaulting to 2 seconds. Error: %v", intervalSecsStr, err)
			intervalSecs = 2
		}
	}
	
	return CollectorConfig{
		StorageServiceAddr: storageAddr + ":" + storagePort, 
		CollectionInterval: time.Duration(intervalSecs) * time.Second,
	}
}

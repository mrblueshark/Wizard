// Package app provides the main application logic and configuration loading for the collector service.
package app

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

// Config struct holds the application configuration loaded from environment variables.
type Config struct {
	KafkaBroker string
	KafkaTopic  string
	RunInterval time.Duration
}

// LoadConfig reads configuration from environment variables and returns a Config struct.
func LoadConfig() *Config {
	// Kafka Broker (e.g., "kafka:9093" in Docker Compose)
	kafkaBroker := os.Getenv("KAFKA_BROKER")
	if kafkaBroker == "" {
		fmt.Println("FATAL: KAFKA_BROKER environment variable not set. Defaulting to 'localhost:9092'")
		kafkaBroker = "localhost:9092"
	}

	// Kafka Topic (e.g., "events")
	kafkaTopic := os.Getenv("KAFKA_TOPIC")
	if kafkaTopic == "" {
		fmt.Println("FATAL: KAFKA_TOPIC environment variable not set. Defaulting to 'events'")
		kafkaTopic = "events"
	}

	// Run Interval (e.g., "1000" milliseconds)
	runIntervalStr := os.Getenv("RUN_INTERVAL_MS")
	if runIntervalStr == "" {
		fmt.Println("INFO: RUN_INTERVAL_MS not set. Defaulting to 1000ms")
		runIntervalStr = "1000" // Default to 1 second
	}

	runIntervalMs, err := strconv.Atoi(runIntervalStr)
	if err != nil || runIntervalMs <= 0 {
		fmt.Printf("WARN: Invalid RUN_INTERVAL_MS (%s). Using default 1000ms.\n", runIntervalStr)
		runIntervalMs = 1000
	}

	return &Config{
		KafkaBroker: kafkaBroker,
		KafkaTopic:  kafkaTopic,
		// Convert milliseconds to time.Duration
		RunInterval: time.Duration(runIntervalMs) * time.Millisecond,
	}
}

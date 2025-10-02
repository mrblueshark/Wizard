// Package app provides the main application logic for the collector service.
package app

import (
	"fmt"
	"os"
)

// Main function serves as the entry point for the application.
func Main() {
	// Load configuration from environment variables
	config := LoadConfig()

	// Initialize the Collector instance with loaded config
	collector := NewCollector(
		config.KafkaBroker,
		config.KafkaTopic,
		config.RunInterval,
	)

	// Check if the collector initialization was successful (producer is created)
	if collector == nil {
		fmt.Println("FATAL: Collector initialization failed. Exiting.")
    

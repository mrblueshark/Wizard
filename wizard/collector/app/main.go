package app

import (
	"log"
	"os"
	"os/signal"
	"syscall"
)

// Run is the main entrypoint function for the collector application logic.
func Run() {
	log.Println("Starting Collector service...")

	// 1. Load Configuration (from config.go)
	cfg := LoadConfig()

	// 2. Initialize Dispatcher (gRPC client, from dispatcher.go)
	dispatcher, err := NewDispatcher(cfg.StorageServiceAddr)
	if err != nil {
		log.Fatalf("FATAL: Failed to connect to storage service at %s: %v", cfg.StorageServiceAddr, err)
	}
	defer dispatcher.Close()
	log.Printf("Successfully initialized dispatcher to %s", cfg.StorageServiceAddr)

	// 3. Initialize and Start Capture Engine (from engine.go)
	engine := NewCaptureEngine(dispatcher)
	go engine.Start() // Run the engine in a separate goroutine

	// 4. Graceful Shutdown Handler
	quit := make(chan os.Signal, 1)
	// Trap signals: INT (Ctrl+C) and TERM (kill)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	
	// Wait for an interrupt signal
	<-quit
	
	log.Println("Received shutdown signal. Starting cleanup...")

	// Stop the engine and wait for dispatching to finish
	engine.Stop() 
	
	log.Println("Collector service gracefully stopped.")
}

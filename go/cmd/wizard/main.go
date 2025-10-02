package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"
	"time"

	"wizard/collector/app" 
)

func main() {
	kafkaBrokers := os.Getenv("KAFKA_BROKERS")
	kafkaTopic := os.Getenv("KAFKA_OUTPUT_TOPIC")
	
	if kafkaBrokers == "" || kafkaTopic == "" {
		log.Fatal("FATAL: Missing KAFKA_BROKERS or KAFKA_OUTPUT_TOPIC environment variables. Exiting.")
	}

	fmt.Println("WIZARD Collector Service starting up...")
	
	engine := app.NewEngine()
	
	dispatcher, err := app.NewDispatcher(kafkaBrokers, kafkaTopic)
	if err != nil {
		log.Fatalf("FATAL: Could not initialize Kafka Dispatcher: %v", err)
	}
	defer dispatcher.Close() 

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

	fmt.Println("Service running. Listening for events (simulated loop)...")

	// --- Simulation: Event Ingestion Loop ---
	go func() {
		ticker := time.NewTicker(5 * time.Second)
		defer ticker.Stop()
		
		for {
			select {
			case <-ticker.C:
				rawEventData := []byte(`{"type": "TELEMETRY", "user_id": "u-mock-007", "payload": {"status": "ok", "latency_ms": 15}}`)
				
				event, pErr := engine.ProcessEvent(ctx, rawEventData)
				if pErr != nil {
					log.Printf("ERROR: Failed to process incoming event: %v", pErr)
					continue
				}
				
				dErr := dispatcher.DispatchEvent(ctx, event)
				if dErr != nil {
					log.Printf("ERROR: Failed to dispatch event %s to Kafka: %v", event.ID, dErr)
				} else {
					fmt.Printf("[%s] Event %s Dispatched (Type: %s)\n", time.Now().Format("15:04:05"), event.ID, event.Type)
				}
				
			case <-ctx.Done():
				return
			}
		}
	}()

	// --- Wait for Shutdown Signal ---
	sig := <-sigCh
	fmt.Printf("\nReceived signal (%v). Starting graceful shutdown...\n", sig)

	cancel()
	time.Sleep(2 * time.Second)
	fmt.Println("WIZARD Collector Service shutdown complete.")
	os.Exit(0)
}

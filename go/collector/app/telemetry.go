// Package app provides application logic including telemetry setup.
package app

import (
	"fmt"
	"net/http"
	"time"
)

// Telemetry holds any metrics or monitoring components.
type Telemetry struct {
	// We can add Prometheus registry, Jaeger tracer, etc., here later.
}

// NewTelemetry creates and initializes telemetry components.
func NewTelemetry() *Telemetry {
	// NOTE: For a complete solution, this would initialize a Prometheus register
	// or an OpenTelemetry/Jaeger tracer.
	return &Telemetry{}
}

// StartMetricsServer starts a simple HTTP server to expose metrics or health checks.
func (t *Telemetry) StartMetricsServer() {
	mux := http.NewServeMux()

	// Simple health check endpoint
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, "OK: Collector is running at %s", time.Now().Format(time.RFC3339))
	})

	// Placeholder for /metrics endpoint
	mux.HandleFunc("/metrics", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, "# Placeholder for Prometheus metrics output.\n")
		fmt.Fprintf(w, "collector_events_produced_total 0\n")
	})

	// Start server asynchronously
	go func() {
		port := ":8080"
		fmt.Printf("INFO: Telemetry server starting on http://localhost%s\n", port)
		if err := http.ListenAndServe(port, mux); err != nil && err != http.ErrServerClosed {
			fmt.Printf("ERROR: Telemetry server failed to start: %v\n", err)
		}
	}()
}

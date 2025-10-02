package app

import (
	"log"
)

// Telemetry provides a standardized interface for logging, metrics, and tracing.
type Telemetry struct {
	// In a production environment, this would hold references to Prometheus, Jaeger, etc.
}

// NewTelemetry initializes the telemetry system.
func NewTelemetry(serviceName string) *Telemetry {
	log.Printf("[TELEMETRY] Initialized telemetry for service: %s", serviceName)
	// Add setup for real metrics/tracing here
	return &Telemetry{}
}

// LogError handles standardized error logging.
func (t *Telemetry) LogError(message string, err error) {
	log.Printf("[ERROR] %s: %v", message, err)
}

// LogInfo handles standardized informational logging.
func (t *Telemetry) LogInfo(message string) {
	log.Printf("[INFO] %s", message)
}

// RecordMetric simulates recording a metric (e.g., packet dispatch rate).
func (t *Telemetry) RecordMetric(name string, value float64) {
	// In production, push to Prometheus/Datadog here
	log.Printf("[METRIC] %s: %.2f", name, value)
}

// Close gracefully shuts down telemetry resources (e.g., flushing logs).
func (t *Telemetry) Close() {
	log.Println("[TELEMETRY] Shutting down.")
}

// We should update collector/app/main.go to use this:
/*
// Inside collector/app/main.go Run()
telemetry := NewTelemetry("collector")
defer telemetry.Close()
// Replace log.Printf with telemetry.LogInfo/LogError where applicable
*/

package tests

import (
	"context"
	"testing"

	"wizard/collector/app" // Import the application logic to be tested
	"wizard/pkg/models"  // Import shared data models
)

// TestProcessEvent_ValidData ensures that a correctly formatted event is processed
// and converted into the standardized CollectorEvent model.
func TestProcessEvent_ValidData(t *testing.T) {
	// 1. Setup the test environment
	engine := app.NewEngine()
	ctx := context.Background()

	// 2. Define a valid raw JSON event payload (as bytes)
	validRawData := []byte(`{
		"type": "LOGIN",
		"user_id": "user-42",
		"payload": {
			"ip_address": "192.168.1.1",
			"success": true
		}
	}`)

	// 3. Execute the function being tested
	event, err := engine.ProcessEvent(ctx, validRawData)

	// 4. Assert the results
	if err != nil {
		t.Fatalf("ProcessEvent failed with an unexpected error: %v", err)
	}
	
	if event.Type != models.EventLogin {
		t.Errorf("Expected event type %s, got %s", models.EventLogin, event.Type)
	}
	
	if event.UserID != "user-42" {
		t.Errorf("Expected UserID 'user-42', got %s", event.UserID)
	}

	// Check if the flexible Data payload was parsed correctly
	if ip, ok := event.Data["ip_address"].(string); !ok || ip != "192.168.1.1" {
		t.Errorf("Expected ip_address to be '192.168.1.1', got %v", event.Data["ip_address"])
	}
}

// TestProcessEvent_MissingUserID ensures validation logic correctly rejects bad data.
func TestProcessEvent_MissingUserID(t *testing.T) {
	// 1. Setup the test environment
	engine := app.NewEngine()
	ctx := context.Background()

	// 2. Define an invalid raw JSON event payload (missing user_id)
	invalidRawData := []byte(`{
		"type": "PURCHASE",
		"payload": {
			"value": 99.99
		}
	}`)

	// 3. Execute the function being tested
	_, err := engine.ProcessEvent(ctx, invalidRawData)

	// 4. Assert the error
	if err == nil {
		t.Fatal("Expected an error due to missing user_id, but got none.")
	}
	
	expectedErrorSubstring := "missing user_id"
	if err != nil && !contains(err.Error(), expectedErrorSubstring) {
		t.Errorf("Expected error message to contain '%s', but got: %v", expectedErrorSubstring, err)
	}
}

// Helper function to check if a string contains a substring
func contains(s, substr string) bool {
	for i := 0; i < len(s)-len(substr)+1; i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}

package app

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"time"

	"wizard/pkg/models" 
	"wizard/pkg/utils" 
)

type Engine struct {}

func NewEngine() *Engine {
	return &Engine{}
}

type RawEvent struct {
	Type string `json:"type"`
	UserID string `json:"user_id"`
	Payload json.RawMessage `json:"payload"`
}

func (e *Engine) ProcessEvent(ctx context.Context, data []byte) (*models.CollectorEvent, error) {
	var raw RawEvent
	
	if err := json.Unmarshal(data, &raw); err != nil {
		return nil, fmt.Errorf("failed to unmarshal raw event: %w", err)
	}

	if raw.UserID == "" {
		return nil, errors.New("event validation failed: missing user_id")
	}
	
	eventType := models.EventType(raw.Type)
	if eventType == "" {
		return nil, errors.New("event validation failed: missing event type")
	}
	
	var eventData map[string]interface{}
	if err := json.Unmarshal(raw.Payload, &eventData); err != nil {
		// Accept empty payload
	}

	event := &models.CollectorEvent{
		ID:            utils.GenerateUUID(), 
		Timestamp:     time.Now().UTC(),
		Type:          eventType,
		UserID:        raw.UserID,
		SourceService: "collector-v1",
		Data:          eventData,
	}
	
	return event, nil
}

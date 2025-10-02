package models

import (
	"time"
)

type EventType string

const (
	EventLogin     EventType = "LOGIN"
	EventPurchase  EventType = "PURCHASE"
	EventClick     EventType = "CLICK"
	EventTelemetry EventType = "TELEMETRY"
)

type CollectorEvent struct {
	ID string `json:"id" bson:"_id"` 
	Timestamp time.Time `json:"timestamp" bson:"timestamp"`
	Type EventType `json:"type" bson:"type"`
	UserID string `json:"user_id" bson:"user_id"`
	SourceService string `json:"source_service" bson:"source_service"`
	Data map[string]interface{} `json:"data" bson:"data"`
}

type AnalysisResult struct {
	EventID string `json:"event_id" bson:"event_id"`
	Score float64 `json:"score" bson:"score"` 
	Labels []string `json:"labels" bson:"labels"`
	DetailMessage string `json:"detail_message" bson:"detail_message"`
	ProcessedAt time.Time `json:"processed_at" bson:"processed_at"`
}

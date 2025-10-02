package app

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"github.com/confluentinc/confluent-kafka-go/v2/kafka"
	"wizard/pkg/models" 
)

type Dispatcher struct {
	Producer *kafka.Producer
	Topic    string
}

func NewDispatcher(brokers, topic string) (*Dispatcher, error) {
	p, err := kafka.NewProducer(&kafka.ConfigMap{
		"bootstrap.servers": brokers,
		"client.id":         "wizard-collector",
		"acks":              "all", 
	})

	if err != nil {
		return nil, fmt.Errorf("failed to create Kafka producer: %w", err)
	}

	go func() {
		for e := range p.Events() {
			switch ev := e.(type) {
			case *kafka.Message:
				if ev.TopicPartition.Error != nil {
					fmt.Printf("Delivery failed: %v\n", ev.TopicPartition.Error)
				}
			}
		}
	}()

	return &Dispatcher{
		Producer: p,
		Topic:    topic,
	}, nil
}

func (d *Dispatcher) Close() {
	d.Producer.Close()
}

func (d *Dispatcher) DispatchEvent(ctx context.Context, event *models.CollectorEvent) error {
	eventBytes, err := json.Marshal(event)
	if err != nil {
		return fmt.Errorf("failed to marshal event %s to JSON: %w", event.ID, err)
	}

	err = d.Producer.Produce(&kafka.Message{
		TopicPartition: kafka.TopicPartition{Topic: &d.Topic, Partition: kafka.PartitionAny},
		Key:            []byte(event.UserID),
		Value:          eventBytes,
		Timestamp:      time.Now(),
	}, nil) 

	if err != nil {
		return fmt.Errorf("failed to produce message for event %s: %w", event.ID, err)
	}

	return nil
}

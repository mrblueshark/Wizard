package app

import (
	"log"
	"math/rand"
	"time"
	"encoding/binary"
	"fmt"

	pb "wizard/collector/pkg/transport"
	"github.com/google/uuid"
)

// CaptureEngine is responsible for simulating data capture and generating Packets.
type CaptureEngine struct {
	dispatcher *Dispatcher
	stopChan   chan bool
}

// NewCaptureEngine creates a new engine instance linked to a dispatcher.
func NewCaptureEngine(d *Dispatcher) *CaptureEngine {
	return &CaptureEngine{
		dispatcher: d,
		stopChan:   make(chan bool),
	}
}

// generateMockPacket creates a simulated network packet.
func generateMockPacket() *pb.Packet {
	// Generate random IP addresses
	ip := func() string {
		return fmt.Sprintf("%d.%d.%d.%d", rand.Intn(256), rand.Intn(256), rand.Intn(256), rand.Intn(256))
	}
	
	// Generate a random payload (simulated network traffic)
	payloadSize := rand.Intn(1024) + 128 // 128 to 1151 bytes
	payload := make([]byte, payloadSize)
	binary.BigEndian.PutUint64(payload, uint64(time.Now().UnixNano())) // Put a timestamp in the first 8 bytes
	rand.Read(payload[8:])

	return &pb.Packet{
		Id:             uuid.New().String(),
		TimestampMs:    time.Now().UnixMilli(),
		SourceIp:       ip(),
		DestinationIp:  ip(),
		Payload:        payload,
	}
}

// Start runs the engine, capturing and dispatching packets at intervals.
func (ce *CaptureEngine) Start() {
	log.Println("Capture Engine starting up...")
	
	ticker := time.NewTicker(2 * time.Second) // Dispatch a packet every 2 seconds
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			// 1. Capture/Generate Data
			packet := generateMockPacket()
			
			// 2. Dispatch Data
			ce.dispatcher.DispatchPacket(packet)

		case <-ce.stopChan:
			log.Println("Capture Engine shutting down.")
			return
		}
	}
}

// Stop signals the engine to halt its operations.
func (ce *CaptureEngine) Stop() {
	close(ce.stopChan)
}

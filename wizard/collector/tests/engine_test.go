package tests

import (
	"testing"
	"time"

	"wizard/collector/app" // Assuming app.NewDispatcher is accessible
	pb "wizard/collector/pkg/transport"
)

// MockDispatcher implements the necessary methods for testing without a real gRPC connection.
type MockDispatcher struct {
	LastPacket *pb.Packet
}

func (m *MockDispatcher) DispatchPacket(p *pb.Packet) {
	// Simply stores the last dispatched packet for inspection
	m.LastPacket = p
}

func (m *MockDispatcher) Close() {
	// No-op for mock
}

// TestPacketGeneration verifies that the engine generates a properly formatted packet.
func TestPacketGeneration(t *testing.T) {
	// Note: We access the internal function used by app.CaptureEngine for testing purposes.
	packet := app.GenerateMockPacket()

	if packet.GetId() == "" {
		t.Error("Packet ID cannot be empty.")
	}

	if packet.GetTimestampMs() == 0 {
		t.Error("Packet timestamp cannot be zero.")
	}
	
	// Check if the timestamp is roughly near the current time (within 1 second tolerance)
	currentTimeMs := time.Now().UnixMilli()
	if packet.GetTimestampMs() > currentTimeMs || packet.GetTimestampMs() < currentTimeMs - 1000 {
		t.Errorf("Packet timestamp (%d) is far from current time (%d)", packet.GetTimestampMs(), currentTimeMs)
	}

	if len(packet.GetSourceIp()) < 7 || len(packet.GetDestinationIp()) < 7 { // e.g., "1.1.1.1"
		t.Error("Source/Destination IP appears invalid or too short.")
	}

	if len(packet.GetPayload()) < 128 {
		t.Errorf("Payload size (%d) is less than the expected minimum (128 bytes).", len(packet.GetPayload()))
	}
}

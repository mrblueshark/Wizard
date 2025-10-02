package app

import (
	"context"
	"log"
	"time"

	pb "wizard/collector/pkg/transport" // The generated stubs
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

// Dispatcher holds the connection and client for the storage service.
type Dispatcher struct {
	client pb.DataReceiverClient
	conn   *grpc.ClientConn
}

// NewDispatcher initializes a gRPC connection to the storage service.
func NewDispatcher(storageAddr string) (*Dispatcher, error) {
	// ⚠️ NOTE: Using Insecure transport for simplicity. 
	// In production, always use transport credentials (TLS/SSL).
	conn, err := grpc.Dial(storageAddr, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		return nil, err
	}

	client := pb.NewDataReceiverClient(conn)

	return &Dispatcher{
		client: client,
		conn:   conn,
	}, nil
}

// Close gracefully closes the underlying gRPC connection.
func (d *Dispatcher) Close() {
	if d.conn != nil {
		d.conn.Close()
	}
}

// DispatchPacket sends a single captured Packet to the storage service.
func (d *Dispatcher) DispatchPacket(p *pb.Packet) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	log.Printf("Dispatching packet ID: %s", p.GetId())

	// Call the gRPC method defined in transport.proto
	response, err := d.client.StorePacket(ctx, p)
	if err != nil {
		log.Printf("ERROR: Failed to dispatch packet ID %s: %v", p.GetId(), err)
		return
	}

	if response.GetSuccess() {
		log.Printf("SUCCESS: Packet ID %s stored with ID %s. Message: %s", p.GetId(), response.GetStoredId(), response.GetMessage())
	} else {
		log.Printf("WARNING: Packet ID %s dispatch failed. Message: %s", p.GetId(), response.GetMessage())
	}
}
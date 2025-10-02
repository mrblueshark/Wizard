module wizard/collector

go 1.21

require (
	google.golang.org/grpc v1.60.1
	google.golang.org/protobuf v1.32.0
)

// Ensure generated protobuf files can be imported
replace wizard/collector/pkg/transport => ./pkg/transport
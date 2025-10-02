package utils

import (
	"fmt"

	"github.com/google/uuid"
)

func GenerateUUID() string {
	id, err := uuid.NewRandom()
	if err != nil {
		panic(fmt.Sprintf("Failed to generate UUID: %v", err))
	}
	return id.String()
}

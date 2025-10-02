# Wizard/scripts/build.sh

#!/bin/bash
# Description: Script to build the Docker images for the Go Collector and Python Analyzer microservices.

set -e # Exit immediately if a command exits with a non-zero status

# Define service image names
GO_IMAGE="wizard-collector"
PYTHON_IMAGE="wizard-analyzer"
TAG="latest"

echo "=========================================================="
echo " Starting Microservice Build Process"
echo "=========================================================="

# --- 1. Build Go Collector Image ---
echo "--- Building Go Collector Image: ${GO_IMAGE}:${TAG} ---"
# Explicitly use the 'go' directory as the context and the specific Dockerfile path.
# Assuming the script is run from the project root (Wizard/)
docker build -t ${GO_IMAGE}:${TAG} -f go/Dockerfile . 

echo "✅ Go Collector image built successfully."

# --- 2. Build Python Analyzer Image ---
echo "--- Building Python Analyzer Image: ${PYTHON_IMAGE}:${TAG} ---"
# Explicitly use the 'python' directory as the context (if structure is Wizard/python/...) 
# OR use the root context and specify the Dockerfile.
# We will use the original Dockerfile path for consistency:
docker build -t ${PYTHON_IMAGE}:${TAG} -f analyzer/Dockerfile .

echo "✅ Python Analyzer image built successfully."

echo "=========================================================="
echo " Build Process Complete. Commit this fix and push again!"
echo "=========================================================="

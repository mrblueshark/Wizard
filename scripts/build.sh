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
# Note: Docker will use the go/Dockerfile
docker build -t ${GO_IMAGE}:${TAG} .

echo "✅ Go Collector image built successfully."

# --- 2. Build Python Analyzer Image ---
echo "--- Building Python Analyzer Image: ${PYTHON_IMAGE}:${TAG} ---"
# Note: Docker will use the analyzer/Dockerfile (or python/analyzer/Dockerfile)
# Assuming the root context '.' is sufficient, and the path is configured correctly in the Dockerfile
docker build -t ${PYTHON_IMAGE}:${TAG} .

echo "✅ Python Analyzer image built successfully."

echo "=========================================================="
echo " Build Process Complete."
echo " Images available: ${GO_IMAGE}:${TAG} and ${PYTHON_IMAGE}:${TAG}"
echo "=========================================================="

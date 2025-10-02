# Wizard/scripts/run.sh

#!/bin/bash
# Description: Script to build the images, start the Docker services, and stream logs.

set -e # Exit immediately if a command exits with a non-zero status

echo "--- 1. Ensuring Images are Built ---"
# Call the dedicated build script to make sure collector and analyzer images are ready
./build.sh

echo "--- 2. Starting Services via Docker Compose ---"
# Start the services in detached mode (using the docker-compose.yaml file)
docker-compose up -d

echo "--- 3. Verifying Deployment and Streaming Logs ---"
echo "Services are starting (Mongo, Kafka, Zookeeper, Collector, Analyzer)."
echo "Press Ctrl+C to detach from the logs and leave the services running."
# Stream logs to immediately show the pipeline activity (Go Collector producing, Python Analyzer consuming)
docker-compose logs -f

echo "Service deployment initiated successfully."

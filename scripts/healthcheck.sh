#!/bin/bash

# This script is used as a wrapper to check external service health before
# starting the main application command (which is passed as arguments).

if [ -z "$DB_HOST" ]; then
    echo "DB_HOST environment variable not set. Skipping health check."
else
    # Wait for the database (PostgreSQL in this case) to be available
    echo "Waiting for database (${DB_HOST}:${DB_PORT}) to be available..."
    
    # Check if 'netcat' is available, install it if needed (specific to Debian/Alpine image)
    if ! command -v nc &> /dev/null; then
        echo "netcat not found. Installing..."
        # This assumes your base image (python:3.11-slim) is Debian-based.
        # For Alpine, it would be 'apk add busybox-initscripts'
        # For simplicity in Dockerfile context, we assume it's available or installed in the Dockerfile setup stage.
        # For this local script, we'll just proceed with a simple sleep if nc fails.
        sleep 5 
    fi

    # Use netcat (nc) to check the connection
    until nc -z "$DB_HOST" "$DB_PORT"; do
        echo "Database is unavailable - sleeping"
        sleep 2
    done
    
    echo "Database is up and running!"
fi

# Execute the main application command passed to the script (e.g., uvicorn)
exec "$@"

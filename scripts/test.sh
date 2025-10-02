# Wizard/scripts/test.sh

#!/bin/bash
# Description: Script to run all unit and integration tests for Go and Python services.

set -e # Exit immediately if a command exits with a non-zero status

echo "=========================================================="
echo " Starting Unit and Integration Test Suite"
echo "=========================================================="

# --- 1. Go Collector Service Tests ---
echo "--- 1.1: Running Go Collector Tests ---"
# Navigate to the Go directory
cd go
# FIX: Use -mod=readonly to tell Go to respect go.mod and ignore vendoring inconsistencies.
go test ./... -v -mod=readonly 

# Return to the root directory
cd ..
echo "✅ Go Collector tests passed."


# --- 2. Python Analyzer Service Tests ---
echo "--- 2.1: Running Python Analyzer Tests (using Pytest) ---"
# Run Pytest in the Python directory, pointing to the 'tests' folder
pytest python/tests
echo "✅ Python Analyzer tests passed."

echo "=========================================================="
echo " All Project Tests Complete. Commit this fix and push!"
echo "=========================================================="

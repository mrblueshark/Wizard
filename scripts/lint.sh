# Wizard/scripts/lint.sh

#!/bin/bash
# Description: Robust script to run linters and code formatters for Go and Python using Docker.

set -e # Exit immediately if a command exits with a non-zero status

echo "=========================================================="
echo " Starting Code Linting and Formatting Check (Dockerized)"
echo "=========================================================="

# --- 1. Go Linting and Formatting (Collector) ---
echo "--- 1.1: Running Go fmt, Vet, and Staticcheck ---"
# Use a standard Go image and mount the code volume to run the checks
docker run --rm -v "$(pwd)":/app -w /app golang:1.21 sh -c "
    go install honnef.co/go/tools/cmd/staticcheck@latest && 
    # Check for formatting errors and fail if any are found
    gofmt -l go/ | tee /dev/stderr | [ -z \"\$(cat)\" ] &&
    go vet go/... &&
    staticcheck go/...
"
echo "✅ Go checks passed (fmt, vet, staticcheck)."


# --- 2. Python Linting and Formatting (Analyzer) ---
echo "--- 2.1: Running Python Black formatting check and Flake8 linter ---"
# Use a Python image and install Poetry, then run dev dependencies
docker run --rm -v "$(pwd)":/app -w /app python:3.11-slim sh -c "
    pip install poetry &&
    # Install dev dependencies (pytest, black, flake8) from pyproject.toml
    poetry install --only dev && 
    
    echo '--- Running Black check (Code Formatting) ---' &&
    poetry run black python --check --diff &&
    
    echo '--- Running Flake8 check (Linter) ---' &&
    poetry run flake8 python
"
echo "✅ Python Black and Flake8 checks passed."


echo "=========================================================="
echo " Linting and Quality Checks Complete."
echo "=========================================================="

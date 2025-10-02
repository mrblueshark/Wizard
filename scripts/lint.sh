# Wizard/scripts/lint.sh

#!/bin/bash
# Description: Script to run linters and code formatters for both Go and Python services.

set -e # Exit immediately if a command exits with a non-zero status

echo "=========================================================="
echo " Starting Code Linting and Formatting Check"
echo "=========================================================="

# --- 1. Go Linting and Formatting (Collector) ---
echo "--- 1.1: Running Go fmt check ---"
# Check for unformatted Go files in the 'go' directory
GO_FMT_FILES=$(gofmt -l go)
if [ -n "$GO_FMT_FILES" ]; then
    echo "ERROR: The following Go files are not formatted correctly:"
    echo "$GO_FMT_FILES"
    echo "Run 'gofmt -w go' to fix them."
    exit 1
fi
echo "✅ Go files are correctly formatted."

echo "--- 1.2: Running Go Vet and Staticcheck ---"
# Install staticcheck if not present (only needs to run once)
go install honnef.co/go/tools/cmd/staticcheck@latest 2>/dev/null || true

# Run Go Vet (standard Go static analysis)
go vet go/...
echo "✅ Go Vet passed."

# Run staticcheck (advanced static analysis)
staticcheck go/...
echo "✅ Staticcheck passed."


# --- 2. Python Linting and Formatting (Analyzer) ---
echo "--- 2.1: Running Python Black formatting check ---"
# We assume 'black' is installed (e.g., via pyproject.toml dev dependencies)
# --check flag prevents modification, ensuring it's only a check
black python --check --diff
echo "✅ Python Black formatting check passed."

echo "--- 2.2: Running Python Flake8 linter ---"
# Install flake8 if not present
pip install flake8 2>/dev/null || true

# Run Flake8 linter for common style issues
flake8 python
echo "✅ Python Flake8 linting passed."

echo "=========================================================="
echo " Linting and Quality Checks Complete. All checks passed!"
echo "=========================================================="

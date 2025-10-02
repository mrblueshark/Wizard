# Use a slim Python image for the KMS service
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirement file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code (placeholder for now)
COPY app/ ./app/

# The KMS wrapper will likely run an HTTP/gRPC server
# We use a placeholder command for now.
CMD ["python", "app/main.py"]

# Use a slim Python image for the storage service
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirement file and install dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
# This copies app/, shared/models, and shared/proto stubs
COPY app/ ./app/
COPY ../shared/models/ ./shared/models/
# Assuming stubs are generated in storage/app/
# Ensure you copy transport_pb2.py and transport_pb2_grpc.py into app/

# Command to run the gRPC server
CMD ["python", "app/main.py"]
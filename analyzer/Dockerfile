# Use the official Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies first (for layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY app/ app/

# Set environment variables for configuration (can be overridden by docker-compose)
ENV PYTHONUNBUFFERED 1
ENV MONGO_URI mongodb://mongo:27017/
ENV KAFKA_BROKERS kafka:9092
ENV KAFKA_INPUT_TOPIC events

# Command to run the application
CMD ["python", "app/analyzer.py"]

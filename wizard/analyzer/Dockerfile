# Use a slim Python image for the analyzer service
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirement file and install dependencies
COPY requirements.txt .
# Install requests and pandas, which need build tools
RUN apt-get update && apt-get install -y build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove --purge -y build-essential && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY app/ ./app/
COPY ../shared/models/ ./shared/models/

# Command to run the analyzer main loop
CMD ["python", "app/main.py"]
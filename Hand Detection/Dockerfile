# Base image with Python
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and application files
COPY requirements.txt .
COPY hand_detection_service.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the service port
EXPOSE 5003

# Run the application
CMD ["python", "hand_detection_service.py"]

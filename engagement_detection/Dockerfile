# Base image with Python
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and application files
COPY requirements.txt .
COPY engagement_detection_service.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the service port
EXPOSE 5002

# Run the application
CMD ["python", "engagement_detection_service.py"]

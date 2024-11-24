# Base image with Python
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and application files
COPY requirements.txt .
COPY face_recognition_service.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create the directory for face database
RUN mkdir -p identified_faces

# Expose the service port
EXPOSE 5001

# Run the application
CMD ["python", "face_recognition_service.py"]

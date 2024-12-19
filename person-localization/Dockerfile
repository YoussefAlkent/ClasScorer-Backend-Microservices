FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the necessary files into the container
COPY ./app /app

COPY requirements.txt /app/requirements.txt
# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose the port that FastAPI will run on
EXPOSE 8000

# Run the application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

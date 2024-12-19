from fastapi import FastAPI, HTTPException
import kafka

# Initialize FastAPI app
app = FastAPI()

# Initialize Kafka consumer (running in the background)
import threading
def start_kafka_consumer():
    kafka.consume_messages()

# Start Kafka consumer in a separate thread
consumer_thread = threading.Thread(target=start_kafka_consumer, daemon=True)
consumer_thread.start()

@app.get("/status/")
def get_status():
    """
    Endpoint to check if the consumer is running properly
    """
    return {"status": "Person Detection service is running."}

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

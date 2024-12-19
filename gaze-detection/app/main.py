from fastapi import FastAPI
from pydantic import BaseModel
import threading
from kafka import KafkaConsumer, KafkaProducer
import json
from gaze_model import perform_inference
from utils import decode_image
import kafka_config

# Initialize FastAPI app
app = FastAPI()

# Kafka configuration
consumer = KafkaConsumer(
    kafka_config.INPUT_TOPIC,
    bootstrap_servers=[kafka_config.KAFKA_BROKER],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
producer = KafkaProducer(
    bootstrap_servers=[kafka_config.KAFKA_BROKER],
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

# Data Models
class GazeRequest(BaseModel):
    student_id: str
    image: str  # Base64-encoded image
    bbox: list[float]  # [xmin, ymin, xmax, ymax]

class GazeResponse(BaseModel):
    student_id: str
    is_looking: bool

# FastAPI Endpoint
@app.post("/predict", response_model=GazeResponse)
async def predict_gaze(request: GazeRequest):
    """
    Endpoint for predicting gaze.
    """
    image = decode_image(request.image)
    is_looking, _ = perform_inference(image, request.bbox)
    return GazeResponse(student_id=request.student_id, is_looking=is_looking)

# Kafka Consumer Loop
def kafka_consumer_loop():
    for message in consumer:
        data = message.value
        student_id = data.get("student_id")
        encoded_image = data.get("image")
        bbox = data.get("bbox")

        try:
            image = decode_image(encoded_image)
            is_looking, _ = perform_inference(image, bbox)
            result = {"student_id": student_id, "is_looking": is_looking}
            producer.send(kafka_config.OUTPUT_TOPIC, value=result)
        except Exception as e:
            print(f"Error processing message: {e}")

if __name__ == "__main__":
    import uvicorn

    # Start Kafka consumer in a separate thread
    consumer_thread = threading.Thread(target=kafka_consumer_loop, daemon=True)
    consumer_thread.start()

    # Start FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)

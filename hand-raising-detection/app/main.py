from fastapi import FastAPI
from pydantic import BaseModel
import threading
from kafka import KafkaConsumer, KafkaProducer
import json
from hand_model import hand_model
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
class HandRaisingRequest(BaseModel):
    student_id: str
    image: str  # Base64-encoded image

class HandRaisingResponse(BaseModel):
    student_id: str
    hand_raised: bool

# FastAPI Endpoint
@app.post("/predict", response_model=HandRaisingResponse)
async def predict_hand_raising(request: HandRaisingRequest):
    """
    Endpoint for predicting if a hand is raised.
    """
    image = decode_image(request.image)
    hand_raised = hand_model.predict(image)
    return HandRaisingResponse(student_id=request.student_id, hand_raised=hand_raised)

# Kafka Consumer Loop
def kafka_consumer_loop():
    for message in consumer:
        data = message.value
        student_id = data.get("student_id")
        encoded_image = data.get("image")

        try:
            image = decode_image(encoded_image)
            hand_raised = hand_model.predict(image)
            result = {"student_id": student_id, "hand_raised": hand_raised}
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

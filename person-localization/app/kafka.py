from confluent_kafka import Producer
import json
import config

# Initialize Kafka producer
producer = Producer({'bootstrap.servers': config.KAFKA_BROKER})

# Callback function for Kafka delivery report
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}")

# Function to send message to Kafka
def send_to_kafka(topic: str, message: dict):
    try:
        producer.produce(topic, value=json.dumps(message), callback=delivery_report)
        producer.flush()
    except Exception as e:
        print(f"Error sending message to Kafka: {str(e)}")

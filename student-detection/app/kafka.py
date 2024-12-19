from confluent_kafka import Consumer, KafkaException
import json
import config
import analyze

# Initialize Kafka consumer
consumer = Consumer({
    'bootstrap.servers': config.KAFKA_BROKER,
    'group.id': 'person-detection-group',
    'auto.offset.reset': 'earliest'
})

# Subscribe to the person detection topic
consumer.subscribe([config.KAFKA_PERSON_DETECTION_TOPIC])

# Function to listen for new messages
def consume_messages():
    try:
        while True:
            msg = consumer.poll(timeout=1.0)  # 1 second timeout
            if msg is None:
                continue  # No message, continue polling
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue  # End of partition
                else:
                    raise KafkaException(msg.error())
            
            # Process the message received
            message = json.loads(msg.value().decode('utf-8'))
            analyze.process_person(message)  # Process the person image and ID

    except KeyboardInterrupt:
        print("Consuming stopped.")
    finally:
        consumer.close()

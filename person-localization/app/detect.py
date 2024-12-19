import cv2
from ultralytics import YOLO
import config
from kafka import send_to_kafka

# Load YOLO model
model = YOLO(config.YOLO_MODEL_PATH)

def detect_persons(image_path: str):
    """
    Detect persons in the image and return their bounding box coordinates and class labels.
    """
    img = cv2.imread(image_path)
    results = model(image_path, imgsz=640)
    detections = results[0]

    # Iterate over detections and get bounding boxes for persons
    persons = []
    for box in detections.boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        if label == "person":  # We only care about persons
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cropped = img[y1:y2, x1:x2]
            persons.append({
                "id": len(persons) + 1,
                "bbox": [x1, y1, x2, y2],
                "cropped_image": cropped
            })
    
    return persons

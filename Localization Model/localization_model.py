from flask import Flask, request, jsonify
import cv2
import os
from ultralytics import YOLO

app = Flask(__name__)
model = YOLO("yolov8x-pose-p6.pt")  
os.makedirs("crops", exist_ok=True)

@app.route('/process', methods=['POST'])
def process_image():
    file = request.files['image']
    image_path = "input.jpg"
    file.save(image_path)

    img = cv2.imread(image_path)
    results = model(img, imgsz=640)
    detections = results[0]
    crops = []

    for idx, box in enumerate(detections.boxes):
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        if label == "person":
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cropped = img[y1:y2, x1:x2]
            cropped_path = f"crops/person_{idx}.jpg"
            cv2.imwrite(cropped_path, cropped)
            crops.append(cropped_path)

    response = []
    for crop_path in crops:
        with open(crop_path, 'rb') as f:
            res = requests.post("http://face_recognition_service:5001/process", files={"image": f})
            response.append(res.json())

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify
import mediapipe as mp
import cv2
import numpy as np

app = Flask(__name__)
mp_face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

@app.route('/process', methods=['POST'])
def process_engagement():
    file = request.files['image']
    image_path = "temp.jpg"
    file.save(image_path)

    img = cv2.imread(image_path)
    results = mp_face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    if results.multi_face_landmarks:
        status = "Engaged"
    else:
        status = "Not Engaged"

    return jsonify({"status": status})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

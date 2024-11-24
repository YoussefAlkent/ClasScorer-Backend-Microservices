from flask import Flask, request, jsonify
from deepface import DeepFace
import os
import cv2

app = Flask(__name__)
os.makedirs("identified_faces", exist_ok=True)

@app.route('/process', methods=['POST'])
def process_face():
    file = request.files['image']
    image_path = "temp.jpg"
    file.save(image_path)

    # Run DeepFace
    try:
        result = DeepFace.find(img_path=image_path, db_path="identified_faces")
        if result.empty:
            # Assign a new ID
            new_id = len(os.listdir("identified_faces")) + 1
            os.rename(image_path, f"identified_faces/person_{new_id}.jpg")
            return jsonify({"id": new_id})
        else:
            # Return existing ID
            return jsonify({"id": result.iloc[0]['identity']})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

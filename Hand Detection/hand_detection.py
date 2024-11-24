from flask import Flask, request, jsonify
import mediapipe as mp
import cv2

app = Flask(__name__)
mp_hands = mp.solutions.hands.Hands(static_image_mode=True, max_num_hands=2)

@app.route('/process', methods=['POST'])
def process_hands():
    file = request.files['image']
    image_path = "temp.jpg"
    file.save(image_path)

    img = cv2.imread(image_path)
    results = mp_hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    status = "No Hand Detected"
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            wrist = hand_landmarks.landmark[0]
            index_tip = hand_landmarks.landmark[8]
            if index_tip.y < wrist.y:
                status = "Hand Raised"

    return jsonify({"status": status})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)

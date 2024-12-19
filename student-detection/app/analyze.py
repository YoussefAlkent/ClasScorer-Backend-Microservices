import cv2
import mediapipe as mp
from deepface import DeepFace
import numpy as np

# Initialize MediaPipe for face and hand detection
mp_face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
mp_hands = mp.solutions.hands.Hands(static_image_mode=True, max_num_hands=2)

def analyze_face_and_hand(cropped_img):
    status = ""

    # Run MediaPipe FaceMesh to detect face landmarks
    face_results = mp_face_mesh.process(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
    if face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
            # Estimate engagement using face landmarks (simple engagement based on nose tip and chin)
            nose_tip = np.array([face_landmarks.landmark[1].x, face_landmarks.landmark[1].y])
            chin_center = np.array([face_landmarks.landmark[5].x, face_landmarks.landmark[5].y])
            direction_vector = nose_tip - chin_center

            # If the direction vector is very small, consider the face engaged
            if np.linalg.norm(direction_vector) < 0.1:
                status += "Engaged "
            else:
                status += "Not Engaged "

    # Run MediaPipe Hands to detect if hands are raised
    hand_results = mp_hands.process(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            # Check if the hand is raised (index finger tip above the wrist)
            wrist = hand_landmarks.landmark[0]
            index_finger_tip = hand_landmarks.landmark[8]
            if index_finger_tip.y < wrist.y:  # Hand raised
                status += "Hand Raised"

    return status

def process_person(message):
    """
    Processes a person's cropped image and ID received from the Kafka message.
    """
    person_id = message.get("person_id")
    cropped_image = np.array(message.get("image_data"), dtype=np.uint8)  # Convert list back to image

    # Analyze face engagement and hand raising
    status = analyze_face_and_hand(cropped_image)

    print(f"Person {person_id} - {status}")

    # Here you could send the processed results to the next service in the pipeline (e.g., Gaze Estimation)

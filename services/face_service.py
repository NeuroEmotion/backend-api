import numpy as np
import cv2
from deepface import DeepFace

def analyze_face(file):
    img_bytes = file.read()

    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
    emotion = result[0]['dominant_emotion']

    return {
        "mode": "FACE",
        "emotion": emotion
    }
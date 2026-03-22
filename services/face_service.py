import numpy as np
import cv2
from deepface import DeepFace

def analyze_face(img):
    result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)

    emotion = result[0]['dominant_emotion']
    scores = result[0]['emotion']
    confidence = scores[emotion]

    return {
        "emotion": emotion,
        "confidence": confidence,
        "all_scores": scores
    }
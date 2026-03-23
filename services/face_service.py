import numpy as np
import cv2
from deepface import DeepFace

def analyze_face(img):
    result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)

    deepface_emotion = result[0]['dominant_emotion']
    raw_scores = result[0]['emotion']

    # Map DeepFace emotions to the exact strings your Flutter UI expects
    emotion_mapping = {
        "happy": "Happy",
        "sad": "Sad",
        "angry": "Angry",
        "neutral": "Calm", # Map neutral to Calm
        "fear": "Sad",     
        "disgust": "Angry",
        "surprise": "Happy"
    }

    mapped_emotion = emotion_mapping.get(deepface_emotion, "Calm")

    # Normalize confidence to 0.0 - 1.0 (since Flutter does * 100)
    confidence = raw_scores[deepface_emotion] / 100.0

    # Build a safe scores dictionary matching your 4 frontend metrics
    scores = {
        "Happy": raw_scores.get("happy", 0) / 100.0,
        "Sad": raw_scores.get("sad", 0) / 100.0,
        "Calm": raw_scores.get("neutral", 0) / 100.0,
        "Angry": raw_scores.get("angry", 0) / 100.0
    }

    return {
        "emotion": mapped_emotion,
        "confidence": confidence,
        "all_scores": scores
    }
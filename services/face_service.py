import numpy as np
import cv2
from deepface import DeepFace

def analyze_face(img):
    # Analyze the image
    result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)

    deepface_emotion = result[0]['dominant_emotion']
    raw_scores = result[0]['emotion']

    # Map all 7 DeepFace emotions to Title Case for the Flutter UI
    emotion_mapping = {
        "happy": "Happy",
        "sad": "Sad",
        "angry": "Angry",
        "neutral": "Neutral",
        "fear": "Fear",     
        "disgust": "Disgust",
        "surprise": "Surprise"
    }

    mapped_emotion = emotion_mapping.get(deepface_emotion, deepface_emotion.title())
    
    # Normalize confidence to 0.0 - 1.0
    confidence = raw_scores[deepface_emotion] / 100.0

    # Build the scores dictionary for all 7 emotions
    scores = {emotion_mapping.get(k, k.title()): v / 100.0 for k, v in raw_scores.items()}

    return {
        "emotion": mapped_emotion,
        "confidence": confidence,
        "all_scores": scores
    }
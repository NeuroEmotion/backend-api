from simulation import generate_eeg
from inference import predict_emotion_from_eeg

def process_eeg(eeg_array):
    emotion, confidence, scores = predict_emotion_from_eeg(eeg_array)
    return {
        "emotion": emotion,
        "confidence": confidence,
        "all_scores": scores
    }


def simulate_eeg():
    eeg = generate_eeg(duration_sec=10)
    emotion, confidence, scores = predict_emotion_from_eeg(eeg)
    return {
        "emotion": emotion,
        "confidence": confidence,
        "all_scores": scores,
        "data": eeg.tolist()
    }
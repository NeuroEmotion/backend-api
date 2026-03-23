from simulation import generate_eeg
from inference import predict_emotion_from_eeg

def process_eeg(eeg_array):
    # inference.py returns a dict, so we access it by keys
    res = predict_emotion_from_eeg(eeg_array)
    return {
        "emotion": res["predicted_emotion"],
        "confidence": float(res["confidence"]),
        "all_scores": res["all_probabilities"]
    }

def simulate_eeg():
    eeg = generate_eeg(duration_sec=10)
    res = predict_emotion_from_eeg(eeg)
    return {
        "predicted_emotion": res["predicted_emotion"],
        "confidence": float(res["confidence"]),
        "all_probabilities": res["all_probabilities"],
        "data": eeg.tolist()
    }
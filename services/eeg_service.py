from simulation import generate_eeg
from inference import predict_emotion_from_eeg

def process_eeg(eeg_array):
    result = predict_emotion_from_eeg(eeg_array)
    return {"mode": "EEG", "result": result}


def simulate_eeg():
    eeg = generate_eeg(duration_sec=10)
    result = predict_emotion_from_eeg(eeg)

    return {
        "mode": "EEG",
        "result": result,
        "data": eeg.tolist()
    }
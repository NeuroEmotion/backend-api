import numpy as np
import tensorflow as tf
import joblib
from scipy.signal import welch

# ==============================
# CONFIG (must match training)
# ==============================
FS = 128
WINDOW_SIZE = 128
SEQUENCE_LENGTH = 5
SELECTED_CHANS = [0, 1, 2, 4, 9, 11, 12, 13]  # EEG channels used

EMOTION_MAP = {
    0: "Happy",
    1: "Sad",
    2: "Calm",
    3: "Angry"
}

# ==============================
# Load Scaler + TFLite Model
# ==============================
scaler = joblib.load("scaler.pkl")  # Must be same scaler used in training

interpreter = tf.lite.Interpreter(model_path="lstm_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("Input dtype:", input_details[0]['dtype'])
print("Output dtype:", output_details[0]['dtype'])

# ==============================
# PSD Feature Extraction
# ==============================
def get_psd_features(segment, fs):
    """
    Extracts PSD features (Theta, Alpha, Beta, Gamma bands) from one EEG segment
    """
    bands = {'Theta': (4, 8), 'Alpha': (8, 13),
             'Beta': (13, 30), 'Gamma': (30, 45)}
    features = []

    for ch in range(segment.shape[1]):
        freqs, psd = welch(segment[:, ch], fs, nperseg=segment.shape[0])
        for (low, high) in bands.values():
            idx = np.logical_and(freqs >= low, freqs <= high)
            features.append(np.log1p(np.sum(psd[idx])))

    return np.array(features)

# ==============================
# MAIN INFERENCE FUNCTION
# ==============================
def predict_emotion_from_eeg(raw_eeg):
    """
    raw_eeg: np.array of shape (samples, total_channels)
    returns: dict with predicted emotion and confidence
    """

    # 1️⃣ Select only the channels used during training
    raw_eeg = raw_eeg[:, SELECTED_CHANS]

    # 2️⃣ Convert to 1-second PSD features
    trial_feats = []
    for start in range(0, raw_eeg.shape[0] - WINDOW_SIZE, WINDOW_SIZE):
        segment = raw_eeg[start:start + WINDOW_SIZE]
        trial_feats.append(get_psd_features(segment, FS))

    trial_feats = np.array(trial_feats)

    # Check if enough data
    if len(trial_feats) < SEQUENCE_LENGTH:
        raise ValueError(f"Not enough data to form a {SEQUENCE_LENGTH}-second sequence.")

    # 3️⃣ Take the last SEQUENCE_LENGTH segments
    sequence = trial_feats[-SEQUENCE_LENGTH:]

    # 4️⃣ Flatten → Scale → Reshape
    sequence_flat = sequence.reshape(1, -1)
    sequence_scaled = scaler.transform(sequence_flat)
    sequence_scaled = sequence_scaled.reshape(1, SEQUENCE_LENGTH, 32)

    # 5️⃣ Ensure dtype is float32 for normal TFLite model
    sequence_scaled = sequence_scaled.astype(np.float32)

    # 6️⃣ Run TFLite inference
    interpreter.set_tensor(input_details[0]['index'], sequence_scaled)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]['index'])[0]

    # Convert to dictionary with all emotions
    probabilities = {
        EMOTION_MAP[i]: float(output[i])
        for i in range(len(output))
    }

    pred_class = int(np.argmax(output))

    return {
        "predicted_emotion": EMOTION_MAP[pred_class],
        "confidence": float(np.max(output)),
        "all_probabilities": probabilities
    }

# ==============================
# Example Usage
# ==============================
if __name__ == "__main__":
    # Simulated example: 10 seconds of EEG with 14 channels
    raw_eeg = np.random.randn(1280, 14)  # 128 Hz * 10 sec
    result = predict_emotion_from_eeg(raw_eeg)
    print(result)

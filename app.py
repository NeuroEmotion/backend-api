from flask import Flask, request, jsonify
import numpy as np
from inference import predict_emotion_from_eeg
from simulation import generate_eeg

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json.get("eeg")

    if data is None:
        return jsonify({"error": "No EEG data provided"}), 400

    eeg_array = np.array(data)
    result = predict_emotion_from_eeg(eeg_array)
    return jsonify(result)


@app.route("/simulate", methods=["GET"])
def simulate():
    eeg = generate_eeg(duration_sec=10)
    result = predict_emotion_from_eeg(eeg)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
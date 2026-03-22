from flask import Blueprint, request, jsonify
import numpy as np
from services.eeg_service import process_eeg, simulate_eeg

eeg_bp = Blueprint("eeg", __name__)

@eeg_bp.route("/predict", methods=["POST"])
def predict():
    data = request.json.get("eeg_data")
    if data is None or len(data) < 640:
        return jsonify({"error": "Insufficient EEG data"}), 400

    result = process_eeg(np.array(data))
    return jsonify(result)


@eeg_bp.route("/simulate", methods=["GET"])
def simulate():
    return jsonify(simulate_eeg())

@eeg_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})
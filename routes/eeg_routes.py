from flask import Blueprint, request, jsonify
import numpy as np
from services.eeg_service import process_eeg, simulate_eeg

eeg_bp = Blueprint("eeg", __name__)

@eeg_bp.route("/predict", methods=["POST"])
def predict():
    data = request.json.get("eeg")
    if data is None:
        return jsonify({"error": "No EEG data"}), 400

    result = process_eeg(np.array(data))
    return jsonify(result)


@eeg_bp.route("/simulate", methods=["GET"])
def simulate():
    return jsonify(simulate_eeg())
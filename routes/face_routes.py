from flask import Blueprint, request, jsonify
from services.face_service import analyze_face
import base64
import numpy as np
import cv2

face_bp = Blueprint("face", __name__)

@face_bp.route("/predict_face", methods=["POST"])
def face_emotion():
    data = request.json

    if "image" not in data:
        return jsonify({"error": "No image"}), 400

    # Decode base64 image
    img_bytes = base64.b64decode(data["image"])
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    result = analyze_face(img)

    return jsonify(result)
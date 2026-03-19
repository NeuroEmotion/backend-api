from flask import Blueprint, request, jsonify
from services.face_service import analyze_face

face_bp = Blueprint("face", __name__)

@face_bp.route("/face", methods=["POST"])
def face_emotion():
    if 'image' not in request.files:
        return jsonify({"error": "No image"}), 400

    file = request.files['image']
    result = analyze_face(file)

    return jsonify(result)
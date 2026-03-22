from flask import Flask
from flask_cors import CORS
from routes.eeg_routes import eeg_bp
from routes.face_routes import face_bp
import os

app = Flask(__name__)
CORS(app)  # ✅ ADD THIS

app.register_blueprint(eeg_bp)
app.register_blueprint(face_bp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port)
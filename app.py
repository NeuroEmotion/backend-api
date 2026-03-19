from flask import Flask
from routes.eeg_routes import eeg_bp
from routes.face_routes import face_bp

app = Flask(__name__)

app.register_blueprint(eeg_bp)
app.register_blueprint(face_bp)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

print("Initializing Flask app...")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'safety-monitor-secret-key'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
print("Flask app initialized.")
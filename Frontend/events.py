from flask_socketio import emit
from core import app, socketio  # <-- CHANGED: Import 'app' as well
import state

@socketio.on('connect')
def handle_connect():
    print('Client connected to WebSocket')
    emit('status', {
        'message': 'Connected to Weapon Detection Monitor', 
        'stats': state.violation_stats
    })

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected from WebSocket')

def emit_violation_alert(violation_data):
    """Emit violation alert to all connected clients"""
    with app.app_context():  # <-- CHANGED: Use 'app.app_context()'
        socketio.emit('violation_detected', violation_data)
    print(f"🔔 Violation alert sent to frontend: {violation_data['summary'][:50]}...")

def emit_status_update(status_data):
    """Emit status update to all connected clients"""
    with app.app_context():  # <-- CHANGED: Use 'app.app_context()'
        socketio.emit('status_update', status_data)
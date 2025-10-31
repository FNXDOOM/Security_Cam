from flask import render_template, Response, jsonify
import cv2
import time
from core import app
import state

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/violations')
def get_violations():
    """API endpoint to get recent violations"""
    return jsonify({
        'violations': list(state.latest_violations),
        'stats': state.violation_stats
    })

def generate_frames():
    """Generate video frames for streaming"""
    while True:
        if state.current_frame is not None:
            with state.current_frame_lock:
                frame = state.current_frame.copy()
            
            # Encode frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        else:
            time.sleep(0.1)

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
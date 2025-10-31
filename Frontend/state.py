import threading
from collections import deque

# --- Shared Frame ---
current_frame = None
current_frame_lock = threading.Lock()
last_results = None # To store last YOLO results for drawing

# --- Violation State ---
latest_violations = deque(maxlen=10)  # Store last 10 violations
violation_stats = {
    'total_violations': 0,
    'last_violation_time': None,
    'current_status': 'initializing'
}
violation_history = deque(maxlen=20)
total_violations = 0

# --- Timers and Locks ---
last_alert_time = 0
last_violation_time = 0
frame_counter = 0
violation_processing = False
violation_lock = threading.Lock()

# --- Component Handles ---
vs = None # VideoStream instance
yolo_model = None # YOLO model instance
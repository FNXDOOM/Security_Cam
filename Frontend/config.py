import os

# --- Model & Paths ---
ENGINE_PATH = "best.engine"
SAVE_DIR = "violations"

# --- API & Endpoints ---
DJANGO_API_URL = "http://127.0.0.1:8000/api/alerts/create/" 

# --- Detection Logic ---
# Class IDs from your model: [ 'person', 'weapon']
PERSON_CLASS_ID = 1  # person
WEAPON_CLASS_ID = 2  # weapon

# --- Cooldowns & Performance ---
ALERT_COOLDOWN_SECONDS = 30
VIOLATION_COOLDOWN_SECONDS = 10
DETECTION_SKIP_FRAMES = 3

# --- Directory Setup ---
os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)
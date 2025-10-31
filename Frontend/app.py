import threading
import state
import config  # This will run the os.makedirs commands
from core import app, socketio
from vlm import TORCH_AVAILABLE, TRANSFORMERS_AVAILABLE
from detection_loop import YOLO_AVAILABLE, detection_loop

# These imports are crucial!
# They register the routes and event handlers with the app/socketio instances.
import views
import events

def main():
    # Check device availability
    if TORCH_AVAILABLE:
        import torch
        if torch.cuda.is_available():
            device = "cuda"
            print(f"🚀 Using device: {device}")
        else:
            device = "cpu"
            print(f"🚀 Using device: {device}")
    else:
        device = "cpu"
        print(f"🚀 Using device: {device}")
    
    # Check model availability
    if TRANSFORMERS_AVAILABLE:
        print(f"🤖 SmolVLM2 will be loaded on-demand for efficient memory usage")
    else:
        print(f"⚠️ SmolVLM2 not available - using basic violation descriptions")
        print(f"   To enable advanced descriptions, install: pip install transformers pillow")
    
    if not YOLO_AVAILABLE:
        print("❌ YOLO not available. Cannot proceed without object detection.")
        exit(1)
    
    print("=" * 60)
    print("WEAPON DETECTION CONFIGURATION")
    print("=" * 60)
    print(f"Model: {config.ENGINE_PATH}")
    print(f"Classes: ['criminal', 'person', 'weapon']")
    print(f"Person Class ID: {config.PERSON_CLASS_ID}")
    print(f"Weapon Class ID: {config.WEAPON_CLASS_ID}")
    print(f"Detection Logic: Violation = Person + Weapon proximity")
    print(f"Note: 'criminal' class (ID 0) is IGNORED")
    print("=" * 60)
    
    # Start detection loop in separate thread
    detection_thread = threading.Thread(target=detection_loop, daemon=True)
    detection_thread.start()
    
    print("🌐 Starting Flask web server...")
    print("🌐 Access the frontend at: http://localhost:5000")
    print("🌐 Press Ctrl+C to stop the application")
    
    try:
        # Run Flask app with SocketIO
        socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user...")
    finally:
        print("🛑 Stopping Flask server...")
        if state.vs:
            state.vs.stop()
        if TORCH_AVAILABLE:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        print("✅ Cleanup complete.")

if __name__ == "__main__":
    main()
import cv2
import time
from collections import deque

import state
import config
from camera import VideoStream
from violation_processor import process_violation_async
from vlm import TORCH_AVAILABLE, TRANSFORMERS_AVAILABLE

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    print("❌ YOLO not available. Please install ultralytics: pip install ultralytics")
    YOLO_AVAILABLE = False
    exit(1)

def detection_loop():
    if not YOLO_AVAILABLE:
        return

    print("Loading YOLO model...")
    try:
        state.yolo_model = YOLO(config.ENGINE_PATH)
        print("✅ YOLO model loaded successfully.")
    except Exception as e:
        print(f"❌ Error loading YOLO model: {e}")
        return

    print("Starting threaded video stream...")
    try:
        state.vs = VideoStream(src=0).start()
        time.sleep(2.0)
    except Exception as e:
        print(f"❌ Failed to initialize video stream: {e}")
        return

    fps = state.vs.fps
    buffer_len = int(fps * 12)
    frame_buffer = deque(maxlen=buffer_len)

    print(f"🚀 Starting weapon detection loop...")
    state.last_results = None
    state.violation_stats['current_status'] = 'monitoring'

    try:
        while True:
            frame = state.vs.read()
            if frame is None:
                time.sleep(0.01)
                continue

            state.frame_counter += 1
            
            # Update current frame for streaming
            with state.current_frame_lock:
                state.current_frame = frame.copy()
            
            frame_buffer.append(frame)

            # Run detection on a subset of frames
            if (state.frame_counter % config.DETECTION_SKIP_FRAMES) == 0:
                try:
                    # Detect only person and weapon classes (ignore criminal class)
                    results = state.yolo_model.predict(
                        source=frame, 
                        verbose=False, 
                        conf=0.5, 
                        iou=0.4, 
                        classes=[config.PERSON_CLASS_ID, config.WEAPON_CLASS_ID]
                    )
                    state.last_results = results

                    current_time = time.time()
                    if not state.violation_processing and (current_time - state.last_violation_time) > config.VIOLATION_COOLDOWN_SECONDS:
                        persons, weapons = [], []
                        if results and results[0].boxes is not None:
                            for box in results[0].boxes:
                                class_id = int(box.cls[0])
                                if class_id == config.PERSON_CLASS_ID:
                                    persons.append(box.xyxy[0].cpu().numpy())
                                elif class_id == config.WEAPON_CLASS_ID:
                                    weapons.append(box.xyxy[0].cpu().numpy())

                        # Check if any person is near/carrying a weapon
                        for person_box in persons:
                            person_has_weapon = False
                            px1, py1, px2, py2 = person_box
                            
                            for weapon_box in weapons:
                                wx1, wy1, wx2, wy2 = weapon_box
                                weapon_center_x = (wx1 + wx2) / 2
                                weapon_center_y = (wy1 + wy2) / 2
                                
                                # 1. Weapon center is inside person box
                                if (px1 <= weapon_center_x <= px2 and py1 <= weapon_center_y <= py2):
                                    person_has_weapon = True
                                    break
                                
                                # 2. Weapon box overlaps with person box
                                x_overlap = max(0, min(px2, wx2) - max(px1, wx1))
                                y_overlap = max(0, min(py2, wy2) - max(py1, wy1))
                                
                                if (x_overlap * y_overlap) > 0:
                                    person_has_weapon = True
                                    break
                            
                            if person_has_weapon:
                                ai_status = "SmolVLM2" if TRANSFORMERS_AVAILABLE else "Basic"
                                print(f"🚨 WEAPON THREAT DETECTED! Person with weapon found! Processing with {ai_status}...")
                                process_violation_async(frame.copy(), list(frame_buffer), fps)
                                break  # Process only one violation at a time
                                
                except Exception as e:
                    print(f"❌ YOLO prediction error: {e}")
                    continue
            
            # Add detection overlays to current frame
            if state.last_results:
                try:
                    with state.current_frame_lock:
                        state.current_frame = state.last_results[0].plot(img=state.current_frame)
                        
                        # Add status text
                        ai_mode = "SmolVLM2" if TRANSFORMERS_AVAILABLE else "Basic Mode"
                        status_text = f"{ai_mode} Weapon Detection | Frame: {state.frame_counter} | Processing: {'Yes' if state.violation_processing else 'No'}"
                        cv2.putText(state.current_frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        
                        # Add violation stats
                        stats_text = f"Total Threats: {state.violation_stats['total_violations']} | Status: {state.violation_stats['current_status']}"
                        cv2.putText(state.current_frame, stats_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                except:
                    pass
            
            time.sleep(0.01)  # Small delay to prevent excessive CPU usage

    except KeyboardInterrupt:
        print("\n🛑 Detection loop interrupted by user...")
    except Exception as e:
        print(f"❌ Unexpected error in detection loop: {e}")
    finally:
        print("🛑 Stopping detection loop...")
        if state.vs:
            state.vs.stop()
        if TORCH_AVAILABLE:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        print("✅ Detection cleanup complete.")
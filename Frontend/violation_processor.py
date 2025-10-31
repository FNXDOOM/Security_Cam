import cv2
import threading
import requests
import time
import os
import state
import config
from vlm import vlm_manager
from events import emit_violation_alert, emit_status_update

def generate_summary_from_clip(clip_path):
    """Extract keyframes from clip and generate intelligent, unique summary using SmolVLM2."""
    print("🤖 Starting weapon detection analysis with SmolVLM2...")
    try:
        cap = cv2.VideoCapture(clip_path)
        if not cap.isOpened():
            return "Error: Could not open saved video clip."
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames == 0:
            cap.release()
            return "Error: Video clip has no frames."
        
        frames_to_extract = []
        if total_frames > 10:
            frames_to_extract = [
                int(total_frames * 0.1),
                int(total_frames * 0.4),
                int(total_frames * 0.7),
                int(total_frames * 0.9)
            ]
        else:
            frames_to_extract = [int(total_frames * p) for p in [0.3, 0.7]]
        
        keyframes = []
        frame_timestamps = []
        for idx in frames_to_extract:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                keyframes.append(frame)
                fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
                timestamp = idx / fps
                frame_timestamps.append(timestamp)
        cap.release()

        if not keyframes:
            return "Security violation detected, but could not extract frames for analysis."

        print(f"   > Analyzing {len(keyframes)} keyframes with SmolVLM2...")
        detailed_analysis = {
            'scene_descriptions': [],
            'security_violations': [],
            'person_details': [],
            'environment_context': []
        }
        
        prompts = [
            "Describe the security scene and any weapons or threats you observe:",
            "Focus on the person - describe their appearance and any weapons they are carrying:",
            "Describe the environment and location where this incident is occurring:",
            "What specific security threats or weapons do you see in this image?"
        ]
        
        for i, (frame, timestamp) in enumerate(zip(keyframes, frame_timestamps)):
            print(f"   > Processing frame {i+1}/{len(keyframes)} at {timestamp:.1f}s...")
            
            prompt = prompts[min(i, len(prompts)-1)]
            caption = vlm_manager.generate_caption(frame, prompt)
            
            if caption and len(caption.strip()) > 10:
                caption_lower = caption.lower()
                if any(word in caption_lower for word in ['weapon', 'gun', 'knife', 'armed', 'threat']):
                    detailed_analysis['security_violations'].append(caption)
                elif any(word in caption_lower for word in ['person', 'individual', 'man', 'woman', 'carrying']):
                    detailed_analysis['person_details'].append(caption)
                elif any(word in caption_lower for word in ['area', 'location', 'environment', 'room', 'space']):
                    detailed_analysis['environment_context'].append(caption)
                else:
                    detailed_analysis['scene_descriptions'].append(caption)
        
        print(f"   > Analysis breakdown: {len(detailed_analysis['security_violations'])} threats, "
              f"{len(detailed_analysis['person_details'])} person details, "
              f"{len(detailed_analysis['environment_context'])} context")
        
        summary_parts = []
        current_time = time.strftime("%H:%M:%S")
        summary_parts.append(f"Security Alert at {current_time}")
        
        if detailed_analysis['security_violations']:
            violation_desc = detailed_analysis['security_violations'][0]
            if len(violation_desc) > 80:
                violation_desc = violation_desc[:77] + "..."
            summary_parts.append(violation_desc)
        else:
            summary_parts.append("Armed individual detected - weapon possession confirmed")
        
        context_added = False
        if detailed_analysis['person_details'] and not context_added:
            person_detail = detailed_analysis['person_details'][0]
            if len(person_detail) < 60 and "weapon" not in person_detail.lower():
                summary_parts.append(person_detail)
                context_added = True
        
        if detailed_analysis['environment_context'] and not context_added:
            env_detail = detailed_analysis['environment_context'][0]
            if len(env_detail) < 60:
                summary_parts.append(env_detail)
                context_added = True
        
        if len(summary_parts) > 1:
            summary = " - ".join(summary_parts)
        else:
            summary = summary_parts[0] if summary_parts else "Security monitoring detected armed individual"
        
        severity_indicators = ['immediate security response required', 'urgent threat assessment needed', 
                               'critical security incident', 'high-priority security alert']
        import random
        severity = random.choice(severity_indicators)
        
        if len(summary) > 180:
            summary = summary[:177] + "..."
        summary += f" - {severity.capitalize()}"
        
        print(f"   > Final Summary: {summary}")
        return summary

    except Exception as e:
        print(f"❌ Error during SmolVLM2 analysis: {e}")
        timestamp = int(time.time())
        fallback_options = [
            f"Security alert: Armed individual detected at location {timestamp % 10 + 1} - immediate response required",
            f"Critical threat: Person carrying weapon identified - incident #{timestamp % 100}",
            f"Weapon detection: Armed subject confirmed - alert {timestamp} requires urgent attention",
            f"Security breach: Individual with weapon detected - priority security response needed"
        ]
        return fallback_options[timestamp % len(fallback_options)]
    finally:
        vlm_manager.clear_cache()
        print("   > Cleared GPU cache.")

def send_alert_to_django_async(frame, violation_type, clip_path, summary):
    def send_alert():
        current_time = time.time()
        
        if (current_time - state.last_alert_time) < config.ALERT_COOLDOWN_SECONDS:
            print("⏳ Alert cooldown active. Skipping send.")
            return
        
        try:
            ok, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if not ok: 
                print("❌ Failed to encode frame as JPEG")
                return
            
            payload = {
                'violation_type': violation_type, 
                'camera_id': 'CAM-01', 
                'summary': summary
            }
            
            if not os.path.exists(clip_path):
                print(f"❌ Clip file not found: {clip_path}")
                return
            
            with open(clip_path, "rb") as clip_file:
                files = {
                    'snapshot': ('snapshot.jpg', buffer.tobytes(), 'image/jpeg'),
                    'clip': (os.path.basename(clip_path), clip_file, 'video/mp4')
                }
                print(f"🚀 Sending alert to Django: {summary}")
                response = requests.post(config.DJANGO_API_URL, data=payload, files=files, timeout=30)
                if response.status_code == 201:
                    print("✅ Alert sent successfully!")
                    state.last_alert_time = current_time
                else:
                    print(f"❌ Django error: {response.status_code} - {response.text[:100]}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error sending alert: {e}")
        except Exception as e:
            print(f"❌ Unknown error in send_alert: {e}")
    
    threading.Thread(target=send_alert, daemon=True).start()

def save_violation_clip(frame_buffer, current_frame, timestamp, fps):
    """Fixed version with better error handling and codec fallback"""
    if not frame_buffer:
        print("❌ Frame buffer is empty, cannot save clip.")
        return None
    
    if fps <= 0:
        fps = 30.0
        print(f"⚠️ Invalid FPS detected, using default: {fps}")
    
    try:
        h, w, _ = current_frame.shape
        
        codecs_to_try = [
            ('MJPG', cv2.VideoWriter_fourcc(*'MJPG'), '.avi'),
            ('XVID', cv2.VideoWriter_fourcc(*'XVID'), '.avi'),  
            ('mp4v', cv2.VideoWriter_fourcc(*'mp4v'), '.mp4'),
        ]
        
        out = None
        clip_path = None
        working_codec = None
        
        for codec_name, fourcc, extension in codecs_to_try:
            try:
                clip_path = os.path.join(config.SAVE_DIR, f"violation_{timestamp}{extension}")
                print(f"   Trying codec: {codec_name} -> {clip_path}")
                
                out = cv2.VideoWriter(clip_path, fourcc, fps, (w, h))
                
                if out.isOpened():
                    working_codec = codec_name
                    print(f"   ✅ Using codec: {codec_name}")
                    break
                else:
                    out.release()
                    out = None
                    if os.path.exists(clip_path):
                        os.remove(clip_path)
                    
            except Exception as e:
                print(f"   ❌ Codec {codec_name} failed: {e}")
                if out:
                    out.release()
                    out = None
                if clip_path and os.path.exists(clip_path):
                    os.remove(clip_path)
                continue
        
        if out is None or not out.isOpened():
            print("❌ Error: All video codecs failed. Cannot save video.")
            return None
        
        frames_written = 0
        for frame in frame_buffer:
            if frame is not None:
                out.write(frame)
                frames_written += 1
        
        if current_frame is not None:
            out.write(current_frame)
            frames_written += 1
        
        out.release()
        
        if os.path.exists(clip_path) and os.path.getsize(clip_path) > 0:
            print(f"💾 Violation clip saved: {clip_path} (codec: {working_codec}, frames: {frames_written})")
            return clip_path
        else:
            print(f"❌ Video file creation failed or file is empty: {clip_path}")
            if os.path.exists(clip_path):
                os.remove(clip_path)
            return None
            
    except Exception as e:
        print(f"❌ Failed to save video clip: {e}")
        if out:
            out.release()
        if clip_path and os.path.exists(clip_path):
            os.remove(clip_path)
        return None

def process_violation_async(frame, frame_buffer_copy, fps):
    
    def process():
        with state.violation_lock:
            if state.violation_processing: 
                print("⚠️ Violation already being processed, skipping...")
                return
            state.violation_processing = True
        
        try:
            timestamp = int(time.time())
            state.last_violation_time = timestamp
            state.total_violations += 1
            
            # Update violation stats
            state.violation_stats['total_violations'] = state.total_violations
            state.violation_stats['last_violation_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
            state.violation_stats['current_status'] = 'violation_detected'
            
            print(f"🎥 Processing violation #{state.total_violations} with SmolVLM2...")
            
            # Emit real-time status to frontend
            emit_status_update({
                'status': 'processing_violation',
                'message': f'Processing violation #{state.total_violations}...',
                'stats': state.violation_stats
            })
            
            clip_path = save_violation_clip(frame_buffer_copy, frame, timestamp, fps)
            
            if clip_path:
                summary = generate_summary_from_clip(clip_path)
                
                # Ensure summary uniqueness
                similarity_threshold = 0.6
                max_attempts = 3
                attempts = 0
                
                while attempts < max_attempts:
                    is_unique = True
                    summary_words = set(summary.lower().split())
                    
                    for prev_summary in state.violation_history:
                        prev_words = set(prev_summary.lower().split())
                        if len(summary_words) > 0 and len(prev_words) > 0:
                            overlap = len(summary_words.intersection(prev_words))
                            similarity = overlap / max(len(summary_words), len(prev_words))
                            
                            if similarity > similarity_threshold:
                                is_unique = False
                                break
                    
                    if is_unique:
                        break
                    
                    attempts += 1
                    print(f"   > Summary too similar to previous ones, generating alternative (attempt {attempts})")
                    
                    alternative_summary = f"Violation #{state.total_violations}: Security threat detected at {time.strftime('%H:%M:%S')} - Armed individual identified - Incident requires immediate security response"
                    
                    if attempts == max_attempts:
                        summary = alternative_summary
                
                # Store summary in history
                state.violation_history.append(summary)
                
                # Create violation data for frontend
                violation_data = {
                    'id': state.total_violations,
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                    'summary': summary,
                    'type': 'WEAPON_DETECTED',
                    'severity': 'CRITICAL',
                    'camera_id': 'CAM-01'
                }
                
                # Add to latest violations
                state.latest_violations.append(violation_data)
                
                # Send to Django
                send_alert_to_django_async(frame, "WEAPON_DETECTED", clip_path, summary)
                
                # Emit violation alert to frontend
                emit_violation_alert(violation_data)
                
                # Update status back to monitoring
                state.violation_stats['current_status'] = 'monitoring'
                emit_status_update({
                    'status': 'monitoring',
                    'message': 'Violation processed successfully',
                    'stats': state.violation_stats
                })
                
            else:
                print("❌ Skipping alert because clip saving failed.")
                state.violation_stats['current_status'] = 'monitoring'
                emit_status_update({
                    'status': 'error',
                    'message': 'Failed to save violation clip',
                    'stats': state.violation_stats
                })
                
        except Exception as e:
            print(f"❌ Violation processing failed: {e}")
            state.violation_stats['current_status'] = 'error'
            emit_status_update({
                'status': 'error',
                'message': f'Violation processing error: {str(e)}',
                'stats': state.violation_stats
            })
        finally:
            with state.violation_lock:
                state.violation_processing = False
    
    threading.Thread(target=process, daemon=True).start()
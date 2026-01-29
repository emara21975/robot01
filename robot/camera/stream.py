
import cv2
import numpy as np
from flask import Response
from robot.camera.camera import camera

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def get_placeholder_frame(text="NO CAMERA SIGNAL"):
    """Generate a black frame with text."""
    blank_image = np.zeros((480, 640, 3), np.uint8)
    cv2.putText(blank_image, text, (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (0, 0, 255), 2, cv2.LINE_AA)
    
    # Add timestamp
    import datetime
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    cv2.putText(blank_image, ts, (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, (255, 255, 255), 1)
                
    return blank_image


# Initialize Face Engine (Lazy Load to prevent startup delay)
face_engine = None
faces_db = {}
last_db_refresh = 0

# Shared state for access by other modules (app.py)
last_recognized_face = {
    "name": "Unknown",
    "score": 0.0,
    "time": 0
}

# ⚡ PERFORMANCE: Frame counter for skipping
frame_count = 0

def get_last_face():
    """Returns the last recognized face and its timestamp."""
    return last_recognized_face

def get_face_engine():
    global face_engine, faces_db, last_db_refresh
    if face_engine is None:
        try:
            print("🚀 Loading Face Engine...")
            from robot.camera.face_engine import FaceEngine
            from robot.camera.face_db import load_faces
            face_engine = FaceEngine()
            faces_db = load_faces()
            print("✅ Face Engine Loaded.")
        except Exception as e:
            print(f"❌ Error loading FaceEngine: {e}")
            face_engine = False # valid but disabled
    
    # Reload DB occasionally (e.g. every 10 seconds)
    import time
    if time.time() - last_db_refresh > 10:
        if face_engine:
             from robot.camera.face_db import load_faces
             faces_db = load_faces()
             last_db_refresh = time.time()
             
    return face_engine

def force_reload_faces():
    """Force reloading the face database on the next frame."""
    global last_db_refresh
    last_db_refresh = 0
    print("🔄 Face DB reload requested.")

def gen_frames():
    import time
    from robot.camera.face_db import match_face
    
    last_rec_time = 0
    
    while True:
        if camera:
            frame = camera.get_frame()
        else:
            frame = None

        if frame is None:
            # Yield a placeholder frame instead of stopping
            frame = get_placeholder_frame("Wait for Camera...")
            
            # Encode
            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
            if ret:
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            time.sleep(1.0)
            continue
        
        try:
            # ⚡ PERFORMANCE: Time-based throttling for Face Recognition (Every 0.5s)
            
            # Face Recognition Overlay
            engine = get_face_engine()
            current_time = time.time()
            
            if engine and (current_time - last_rec_time > 0.5):
                last_rec_time = current_time
                
                # ⚡ PERFORMANCE: Resize for faster detection
                small_frame = cv2.resize(frame, (320, 240)) # Even smaller for detection speed
                faces = engine.detect(small_frame)
                
                # ⚡ PERFORMANCE: Only process single face to reduce CPU load
                if len(faces) == 1:
                    face = faces[0]
                    
                    # Bounding Box (scale back to original size 640/320 = 2)
                    # NOTE: If we changed camera res to 640x480, and resize to 320x240, scale is 2.
                    x1, y1, x2, y2 = [int(v * 2) for v in face.bbox]
                    

                    # Recognition
                    name, score = match_face(face.embedding, faces_db, threshold=0.5)
                    
                    # UPDATE GLOBAL STATE (For app.py)
                    if name != "Unknown":
                        last_recognized_face["name"] = name
                        last_recognized_face["score"] = float(score)
                        last_recognized_face["time"] = time.time()
                    
                    # Color: Green for known, Red for Unknown
                    color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                    
                    # Draw Box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    
                    # Draw Name Label
                    label = f"{name} ({score:.2f})"
                    
                    # Background for text
                    cv2.rectangle(frame, (x1, y1 - 30), (x2, y1), color, -1)
                    
                    # Text
                    cv2.putText(
                        frame,
                        label,
                        (x1 + 5, y1 - 7),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        2
                    )
                elif len(faces) > 1:
                    # Multiple faces - show warning
                    cv2.putText(
                        frame,
                        "Multiple faces detected",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 165, 255),
                        2
                    )

        except Exception as e:
            # In case of overlay error, print but still yield frame
            print(f"Overlay Error: {e}")

        # ⚡ PERFORMANCE: Reduced JPEG quality (60) for faster encoding
        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
        if not ret:
            continue
            
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
               
        # ⚡ PERFORMANCE: FPS Limit (~20 FPS)
        time.sleep(0.05)

def video_stream():
    """Returns a Flask Response with the video stream"""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

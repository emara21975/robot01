
import cv2
from flask import Response
from robot.camera.camera import camera

# Global Camera Instance (Imported)
# camera is already imported

# Load Haar Cascade for fast face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def gen_frames():
    while True:
        frame = camera.get_frame()
        if frame is None:
            # If no frame is captured, we can yield a placeholder or just continue
            continue
        
        try:
            # Face Detection Overlay (Lightweight)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Draw rectangles
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Draw Status
            status_text = f"Status: Monitoring"
            if len(faces) > 0:
                status_text = f"Status: Face Detected ({len(faces)})"
            
            cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
        except Exception as e:
            print(f"Overlay Error: {e}")

        # Encoding frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
            
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def video_stream():
    """Returns a Flask Response with the video stream"""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

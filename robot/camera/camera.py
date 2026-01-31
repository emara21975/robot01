
import threading
import time
import numpy as np

# Try importing Picamera2 and libcamera controls
try:
    from picamera2 import Picamera2
    try:
        from libcamera import controls
    except ImportError:
        controls = None
    _PICAMERA_AVAILABLE = True
except ImportError:
    _PICAMERA_AVAILABLE = False
    print("❌ Picamera2 library not found. Camera will be disabled.")


class Camera:
    """Camera class with ON-DEMAND control - starts OFF by default."""
    
    def __init__(self, width=640, height=480):
        self.frame = None
        self.lock = threading.Lock()
        self.running = False
        self.picam2 = None
        self.thread = None
        self.width = width
        self.height = height
        
        # Don't auto-start - camera stays OFF until start() is called
        print("📷 Camera initialized (OFF by default)")
        print("   Call camera.start() to activate")
    
    def start(self):
        """Start the camera. Call this when camera is needed."""
        if self.running:
            print("📷 Camera is already running")
            return True
            
        if not _PICAMERA_AVAILABLE:
            print("⚠️ Picamera2 not available - mock mode")
            self.running = True
            return True
        
        try:
            print(f"🚀 Starting camera ({self.width}x{self.height})...")
            self.picam2 = Picamera2()
            
            # Create configuration
            config = self.picam2.create_preview_configuration(
                main={"format": "BGR888", "size": (self.width, self.height)},
                controls={"FrameRate": 20}
            )
            self.picam2.configure(config)
            
            # Apply ISP Controls if available
            if controls:
                try:
                    self.picam2.set_controls({
                        controls.AeEnable: True,
                        controls.AwbEnable: True,
                        controls.AeMeteringMode: controls.AeMeteringModeEnum.CentreWeighted,
                        controls.NoiseReductionMode: controls.NoiseReductionModeEnum.HighQuality,
                        controls.Sharpness: 1.2,
                        controls.Contrast: 1.1,
                        controls.Brightness: 0.0,
                        controls.Saturation: 1.1
                    })
                except Exception as e_ctrl:
                    print(f"⚠️ ISP controls failed: {e_ctrl}")

            self.picam2.start()
            self.running = True
            
            # Start background update thread
            self.thread = threading.Thread(target=self._update, daemon=True)
            self.thread.start()
            
            print("✅ Camera started successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start camera: {e}")
            self.running = False
            return False
    
    def stop(self):
        """Stop the camera to save resources."""
        if not self.running:
            print("📷 Camera is already stopped")
            return
            
        print("⏹️ Stopping camera...")
        self.running = False
        
        # Wait for thread to finish
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)
        
        # Stop Picamera2
        if self.picam2:
            try:
                self.picam2.stop()
                self.picam2.close()
            except:
                pass
            self.picam2 = None
        
        # Clear frame
        with self.lock:
            self.frame = None
            
        print("✅ Camera stopped")
    
    def is_running(self):
        """Check if camera is currently running."""
        return self.running

    def _update(self):
        """Background thread to capture frames continuously."""
        while self.running:
            try:
                if self.picam2:
                    frame = self.picam2.capture_array()
                    if frame is not None and frame.size > 0:
                        with self.lock:
                            self.frame = frame
            except Exception as e:
                print(f"⚠️ Camera capture error: {e}")
                time.sleep(1)

    def get_frame(self):
        """Return the latest frame, or None if camera is off."""
        if not self.running:
            return None
        with self.lock:
            if self.frame is not None:
                return self.frame.copy()
        return None


# Global Singleton (starts OFF)
try:
    camera = Camera()
except Exception as e:
    print(f"❌ Critical Camera Init Error: {e}")
    camera = None

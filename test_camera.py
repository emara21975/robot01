
import cv2
import time

def test_camera(index, backend_name="AUTO", backend_id=None):
    print(f"\n--- Testing Camera Index {index} [{backend_name}] ---")
    
    if backend_id is not None:
        cap = cv2.VideoCapture(index, backend_id)
    else:
        cap = cv2.VideoCapture(index)

    if not cap.isOpened():
        print(f"❌ Failed to open camera index {index}")
        return False
    
    # Try to force MJPG (often helps on Pi)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Read properties
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"ℹ️ Camera Properties: {width}x{height} @ {fps} FPS")

    print("Reading frames...")
    success_count = 0
    for i in range(10):
        ret, frame = cap.read()
        if ret:
            print(f"✅ Frame {i+1} captured. Shape: {frame.shape}")
            success_count += 1
            if i == 0:
                cv2.imwrite(f"debug_cam_{index}_{backend_name}.jpg", frame)
        else:
            print(f"⚠️ Frame {i+1} failed.")
            time.sleep(0.2)
            
    cap.release()
    return success_count > 0

if __name__ == "__main__":
    print("=== Advanced Camera Diagnostic Tool ===")
    
    # 1. Try Default
    if not test_camera(0, "DEFAULT"):
        # 2. Try V4L2 explicit
        test_camera(0, "V4L2", cv2.CAP_V4L2)
        
    print("\n=== Troubleshooting Tips ===")
    print("If all tests fail, run these commands on the Pi:")
    print("1. ls -l /dev/video*  (Check if device exists)")
    print("2. vcgencmd get_camera (Check if hardware is detected)")
    print("3. sudo modprobe bcm2835-v4l2 (Load legacy driver)")

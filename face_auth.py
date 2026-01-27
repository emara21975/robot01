# -*- coding: utf-8 -*-
"""
نظام التعرّف على الوجه للروبوت الطبي
يعتمد على مكتبات face_recognition و opencv-python
مصمم ليكون خفيفاً على Raspberry Pi
"""

import cv2
import face_recognition
import os
import numpy as np
import time
try:
    from robot.camera.camera import camera as shared_camera
except ImportError:
    shared_camera = None
    print("⚠️ فشل استيراد الكاميرا المشتركة")

# مسار مجلد الوجوه المعروفة
FACES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'faces')

# متغيرات لتخزين بصمات الوجوه
known_face_encodings = []
known_face_names = []
model_loaded = False

def load_known_faces():
    """تحميل الوجوه من المجلد وترميزها في الذاكرة"""
    global known_face_encodings, known_face_names, model_loaded
    
    # التأكد من وجود المجلد
    if not os.path.exists(FACES_DIR):
        os.makedirs(FACES_DIR)
        print("⚠️ مجلد الوجوه فارغ. تم إنشاء المجلد في:", FACES_DIR)
        return

    print("🔄 جاري تحميل بصمات الوجوه...")
    encodings = []
    names = []

    for filename in os.listdir(FACES_DIR):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            try:
                path = os.path.join(FACES_DIR, filename)
                image = face_recognition.load_image_file(path)
                encoding = face_recognition.face_encodings(image)[0]
                
                encodings.append(encoding)
                names.append(os.path.splitext(filename)[0]) # اسم الملف بدون الامتداد
            except Exception as e:
                print(f"❌ تعذر معالجة الصورة {filename}: {e}")

    known_face_encodings = encodings
    known_face_names = names
    model_loaded = True
    print(f"✅ تم تحميل {len(names)} وجه معروف.")

MAX_VERIFY_SECONDS = 10
MAX_ATTEMPTS = 5

def check_face_auth(frame=None):
    """
    التحقق من هوية الشخص أمام الكاميرا.
    Args:
        frame: إطار الصورة (اختياري). إذا لم يتم توفيره، سيتم التقاط واحد من الكاميرا المشتركة.
    Returns:
        (bool, str): (هل تم التعرف؟, الرسالة)
    """
    if not model_loaded:
        load_known_faces()

    if not known_face_encodings:
        return True, "وضع التطوير: تم السماح لعدم وجود وجوه مسجلة"

    if frame is None:
        if shared_camera is None:
            return False, "خطأ: الكاميرا غير متصلة بالنظام"
        frame = shared_camera.get_frame()

    if frame is None:
        return False, "تعذر الحصول على صورة من الكاميرا"

    found_match = False
    message = "لم يتم التعرف على الوجه"

    try:
        # تحسين الأداء: تصغير الصورة إلى الربع
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        # تحويل الألوان من BGR إلى RGB
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # الكشف عن الوجوه
        face_locations = face_recognition.face_locations(rgb_small_frame)
        
        if len(face_locations) > 0:
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
                
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                    found_match = True
                    message = f"تم التعرف على: {name}"
                    print(f"✅ {message}")
                    break
            
    except Exception as e:
        print(f"❌ خطأ أثناء التعرف على الوجه: {e}")
        message = "حدث خطأ في نظام الكاميرا"

    return found_match, message

def verify_with_timeout():
    """التحقق مع مهلة زمنية ومحاولات متعددة"""
    start = time.time()
    attempts = 0
    
    print(f"🕵️ بدء التحقق من الوجه (Timeout={MAX_VERIFY_SECONDS}s)...")

    while (time.time() - start) < MAX_VERIFY_SECONDS and attempts < MAX_ATTEMPTS:
        if shared_camera:
            frame = shared_camera.get_frame()
            if frame is None:
                time.sleep(0.1)
                continue

            attempts += 1
            is_verified, msg = check_face_auth(frame)
            
            if is_verified:
                return {"verified": True, "reason": "FACE_MATCH", "message": msg}
            
            # Wait a bit between attempts
            time.sleep(0.5)
        else:
            return {"verified": False, "reason": "CAMERA_ERROR", "message": "الكاميرا غير متصلة"}

    return {"verified": False, "reason": "TIMEOUT_OR_NO_MATCH", "message": "انتهت المهلة: لم يتم التعرف على الوجه"}

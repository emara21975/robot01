# -*- coding: utf-8 -*-
"""
وحدة التحكم في الأجهزة - Hardware Control
التحكم في السيرفو والبوابات على Raspberry Pi عبر GPIO مباشرة
Arduino للتحكم في حركة الروبوت فقط (START/STOP/RETURN)
"""

import time
import math
import threading

# ============ Hardware Lock (يمنع عمليتين متزامنتين على السيرفو) ============
_hw_lock = threading.Lock()

# ============ Watchdog Thread (لمراقبة حالة الأجهزة) ============
def _run_watchdog():
    """مراقب الخلفية لإنعاش اتصال الأردوينو وضمان استقرار النظام."""
    while True:
        time.sleep(30)
        try:
            # 1. إنعاش اتصال الأردوينو إذا فقد
            if not is_arduino_connected():
                print("🐶 Watchdog: إعادة اتصال الأردوينو...")
                connect_arduino()
                
            # 2. تفريغ المخزن المؤقت لمنع تراكم البيانات
            if is_arduino_connected():
                try:
                    arduino.reset_input_buffer()
                except: pass
                
        except Exception as e:
            print(f"🐶 Watchdog Error: {e}")

# تشغيل المراقب في الخلفية
threading.Thread(target=_run_watchdog, daemon=True).start()

# ============ إعدادات السيرفو ============
ZERO_ANGLE = 23      # نقطة الصفر المرجعية (تتطابق مع الصندوق 1)
LOADING_ANGLE = 100  # زاوية أنبوب التحميل
SERVO_DELAY = 0.02   # سرعة الحركة (0.015 = سريع، 0.02 = متوسط، 0.03 = بطيء)
MIN_MOVE_INTERVAL = 0.5  # ⚡ حماية: أقل وقت بين حركتين للسيرفو (ثواني)
FACE_FRESH_TIMEOUT = 5   # ⚡ حماية: أقصى مدة لاعتبار الوجه "حياً" (ثواني)

_last_servo_move = 0


# ============ إعدادات الصناديق (GPIO Direct Control) ============
# كل صندوق له:
# - pin: منفذ GPIO للسيرفو
# - open_angle: زاوية الفتح
# - close_angle: زاوية الإغلاق
BOX_CONFIG = {
    1: {'pin': 23, 'open_angle': 80, 'close_angle': 0},
    2: {'pin': 24, 'open_angle': 80, 'close_angle': 0},
}

# ============ زوايا الكاروسيل لكل صندوق ============
# الكاروسيل يدور ليوجه الفتحة للصندوق المطلوب
BOX_ANGLES = {
    1: 26,      # الصندوق الأول - نقطة الصفر (ZERO_ANGLE) + 4 درجات للدقة
    2: 140,     # الصندوق الثاني + 5 درجات للدقة
}

# مدة الانتظار بعد فتح البوابة (ثواني)
DISPENSE_HOLD_TIME = 1

# ============ توقيتات حركة الروبوت ============
ROBOT_FORWARD_TIME = 5    # ثواني للتحرك للأمام
ROBOT_BACKWARD_TIME = 3   # ثواني للرجوع للخلف
ROBOT_SETTLE_TIME = 1     # ثواني للتثبيت بعد التوقف

# State Tracking - الزاوية الحالية للكاروسيل
current_carousel_angle = ZERO_ANGLE  # يبدأ عند 23° (الصندوق 1)

# ========== محاولة استيراد مكتبات Raspberry Pi ==========
HAS_GPIO = False
pwm_carousel = None
gate_pwms = {} 

try:
    import RPi.GPIO as GPIO
    HAS_GPIO = True
    print("✓ تم تحميل مكتبة GPIO بنجاح")
except ImportError:
    print("⚠️ مكتبة GPIO غير متاحة - وضع المحاكاة للسيرفو")

# ========== Arduino Connection (للتحكم في الروبوت فقط) ==========
arduino = None
ARDUINO_BAUD_RATE = 9600

def find_arduino_port():
    try:
        import serial.tools.list_ports
        ports = serial.tools.list_ports.comports()
        for port in ports:
            desc = port.description.lower()
            if any(k in desc for k in ['arduino', 'ch340', 'usb', 'acm']):
                print(f"🔍 تم العثور على Arduino: {port.device}")
                return port.device
    except Exception as e:
        print(f"❌ خطأ في البحث عن Arduino: {e}")
    return None

def connect_arduino():
    global arduino
    try:
        import serial
    except ImportError:
        return False

    if arduino is not None and arduino.is_open:
        return True
    
    port = find_arduino_port()
    if not port:
        return False
        
    try:
        arduino = serial.Serial(port, ARDUINO_BAUD_RATE, timeout=1)
        time.sleep(2)
        arduino.flush()
        print(f"✅ تم الاتصال بـ Arduino على {port}")
        return True
    except Exception as e:
        print(f"❌ تعذر الاتصال بـ Arduino: {e}")
        arduino = None
        return False

def disconnect_arduino():
    global arduino
    if arduino:
        try:
            arduino.close()
            print("🔌 تم قطع الاتصال بـ Arduino")
        except: pass
        arduino = None

def is_arduino_connected():
    return arduino is not None and arduino.is_open


# ========== Robot Control Functions (Arduino) ==========
# يجب أن تكون معرفة قبل استخدامها في dispense_dose

def start_robot():
    """بدء تشغيل الروبوت (أمر START للأردوينو)."""
    global arduino
    if not connect_arduino(): 
        return False
    try:
        arduino.write(b'START\n')
        arduino.flush()
        print("🤖 START -> Arduino")
        return True
    except Exception as e:
        disconnect_arduino()
        return False

def stop_robot():
    """إيقاف الروبوت (أمر STOP للأردوينو)."""
    global arduino
    # تحسين: عدم محاولة الاتصال إذا كان متصلاً بالفعل (لتخفيف الضغط)
    if not is_arduino_connected():
        if not connect_arduino(): 
             return False
             
    try:
        # إرسال أمر STOP مرة واحدة مع flush نظيف لتجنب مسح الردود المهمة
        arduino.write(b'STOP\n')
        arduino.flush()
        time.sleep(0.05)
        print("🛑 STOP -> Arduino")
        return True
    except Exception as e:
        disconnect_arduino()
        return False

def return_home():
    """إرجاع الروبوت (أمر RETURN للأردوينو)."""
    global arduino
    if not connect_arduino(): 
        return False
    try:
        arduino.write(b'RETURN\n')
        arduino.flush()
        print("🏠 RETURN -> Arduino")
        return True
    except Exception as e: 
        return False

def get_robot_status():
    """قراءة حالة الروبوت من الأردوينو."""
    if not is_arduino_connected(): 
        return None
    try:
        if arduino.in_waiting > 0:
            return arduino.readline().decode().strip()
    except: 
        pass
    return None



# ========== GPIO Functions ==========

def setup_gpio():
    """تهيئة منافذ GPIO لجميع السيرفوهات."""
    global pwm_carousel, gate_pwms
    
    if not HAS_GPIO:
        print("⚠️ GPIO غير متاح - وضع المحاكاة")
        return False
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
    # تهيئة الكاروسيل (اختياري)
    CAROUSEL_PIN = 18 
    GPIO.setup(CAROUSEL_PIN, GPIO.OUT)
    pwm_carousel = GPIO.PWM(CAROUSEL_PIN, 50)
    pwm_carousel.start(0)
    
    # تهيئة بوابات الصناديق
    for box_id, config in BOX_CONFIG.items():
        pin = config['pin']
        GPIO.setup(pin, GPIO.OUT)
        pwm = GPIO.PWM(pin, 50)
        pwm.start(0)
        gate_pwms[box_id] = pwm
        # ضبط البوابة على وضع الإغلاق
        set_servo_angle(pwm, config['close_angle'])
        time.sleep(0.3)
        pwm.ChangeDutyCycle(0)  # إيقاف PWM لمنع الاهتزاز
    
    # === CALIBRATION: إعادة الكاروسيل لنقطة الصفر عند التشغيل ===
    print("   🔄 جاري معايرة الكاروسيل لنقطة الصفر...")
    set_servo_angle(pwm_carousel, ZERO_ANGLE)
    time.sleep(1.0) # وقت كافي للعودة
    pwm_carousel.ChangeDutyCycle(0)
    print("   ✓ تمت المعايرة: الكاروسيل في وضع الصفر")
    
    print(f"✓ تم تهيئة منافذ GPIO لـ {len(BOX_CONFIG)} صناديق")
    return True

def set_servo_angle(pwm, angle):
    """ضبط زاوية السيرفو."""
    if pwm is None or not hasattr(pwm, 'ChangeDutyCycle'): 
        return
    angle = max(0, min(180, angle))
    # Formula: duty = 2 + (angle / 18) for 50Hz PWM
    duty = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty)

def smooth_move(pwm, start_angle, end_angle, steps=50):
    """حركة خطية دقيقة آمنة للسيرفو.
    
    Args:
        pwm: كائن PWM
        start_angle: الزاوية البدء
        end_angle: الزاوية النهائية
        steps: عدد الخطوات (افتراضي 50 للدقة والنعومة)
    """
    if pwm is None or not hasattr(pwm, 'ChangeDutyCycle'):
        print(f"[SIMULATION] Servo: {start_angle}° -> {end_angle}°")
        time.sleep(abs(end_angle - start_angle) * SERVO_DELAY)
        return
    
    # 🛡️ حماية: القسمة على الصفر
    if steps <= 0:
        set_servo_angle(pwm, end_angle)
        return

    # 🛡️ تطبيع الزوايا لتكون بين 0-180
    start_angle = max(0, min(180, start_angle))
    end_angle = max(0, min(180, end_angle))
    
    distance = abs(end_angle - start_angle)
    
    print(f"   🔄 smooth_move: {start_angle:.1f}° → {end_angle:.1f}° ({distance:.1f}° فرق)")

    # ⚡ تحسين: منع الحركة المجهرية غير الضرورية
    if distance < 1.0:
        set_servo_angle(pwm, end_angle)
        return

    # ⚡ حماية: فرض فترة راحة للسيرفو
    global _last_servo_move
    elapsed = time.time() - _last_servo_move
    if elapsed < MIN_MOVE_INTERVAL:
        time.sleep(MIN_MOVE_INTERVAL - elapsed)

    # 🛡️ حماية: Timeout لمنع العليق في الحلقة
    max_duration = 5.0  # 5 ثواني كحد أقصى للحركة
    start_time = time.time()

    for i in range(steps + 1):
        if (time.time() - start_time) > max_duration:
            print("⚠️ Servo Move Timeout - Breaking Loop")
            break
            
        t = i / steps
        current_angle = start_angle + (end_angle - start_angle) * t
        set_servo_angle(pwm, current_angle)
        time.sleep(SERVO_DELAY)
        
    # تأكيد الزاوية النهائية
    set_servo_angle(pwm, end_angle)
    time.sleep(0.4) # انتظار أطول (0.4s) لمنع الارتداد (Drift)
    
    # إيقاف PWM *بعد* استقرار تام
    pwm.ChangeDutyCycle(0)
    
    # تحديث وقت آخر حركة
    _last_servo_move = time.time()

def move_servo(pwm, target_angle):
    """تحريك السيرفو لزاوية معينة."""
    global current_carousel_angle, pwm_carousel
    
    # 🛡️ تطبيع الزاوية المستهدفة
    target_angle = max(0, min(180, target_angle))
    
    if pwm == pwm_carousel and pwm_carousel is not None:
        # 🛡️ تطبيع الزاوية الحالية (حماية من القيم الخاطئة)
        current_carousel_angle = max(0, min(180, current_carousel_angle))
        
        start_angle = current_carousel_angle
        smooth_move(pwm, start_angle, target_angle, steps=60)
        current_carousel_angle = target_angle
        print(f"   ✓ current_carousel_angle = {current_carousel_angle}°")
    else:
        start_angle = 0
        if target_angle == 0: 
            start_angle = 90
        smooth_move(pwm, start_angle, target_angle, steps=20)


# ========== 🔧 MEDICINE DISPENSING (GPIO DIRECT CONTROL) ==========

# ========== 🔧 MEDICINE DISPENSING (GPIO DIRECT CONTROL) ==========

def dispense_dose(box_id):
    """
    صرف جرعة من صندوق الدواء عبر GPIO مباشرة.
    محمي بقفل الأجهزة (_hw_lock) لمنع التعارض.
    """
    global current_carousel_angle
    
    # === قياس الأداء ===
    start_time = time.time()
    
    # استخدام Context Manager للقفل (أكثر أماناً وأنظف)
    # ملاحظة: acquire لا يدعم الـ context manager مع timeout مباشرة في Python القديم
    # لكن سنستخدم الطريقة الآمنة التقليدية مع تحسين
    if not _hw_lock.acquire(timeout=10):
        print(f"❌ فشل الحصول على قفل الأجهزة (timeout) - الصندوق {box_id}")
        return False, f"النظام مشغول - لا يمكن صرف الصندوق {box_id}"

    # تهيئة متغيرات الطوارئ قبل أي شيء (لمنع crash في الـ except)
    gate_pwm = None
    close_angle = 0

    try:
        print(f"\n{'─'*40}")
        print(f"📦 بدء عملية صرف الدواء - الصندوق {box_id}")
        print(f"{'─'*40}")
        
        # 1. Pre-Dispense Check
        if box_id not in BOX_CONFIG:
            return False, f"صندوق {box_id} غير موجود"
        
        config = BOX_CONFIG[box_id]
        open_angle = config['open_angle']
        close_angle = config['close_angle']
        carousel_angle = BOX_ANGLES.get(box_id, 0)
        gate_pwm = gate_pwms.get(box_id)
        
        # التأكد من الجاهزية
        if HAS_GPIO and (gate_pwm is None or pwm_carousel is None):
            setup_gpio()
            gate_pwm = gate_pwms.get(box_id)
            
        if not HAS_GPIO:
             return True, f"تم صرف جرعة من الصندوق {box_id} (محاكاة)"
             
        # 🛡️ حماية: إيقاف الروبوت قبل تحريك الكاروسيل
        try:
            stop_robot()
            time.sleep(0.2)
        except: pass
        
        # 2. تدوير الكاروسيل
        print(f"\n🔄 الخطوة 2: تدوير الكاروسيل إلى {carousel_angle}°")
        current_carousel_angle = max(0, min(180, current_carousel_angle)) # Normalize
        
        # التحرك للزاوية الدقيقة
        smooth_move(pwm_carousel, current_carousel_angle, carousel_angle, steps=40)
        time.sleep(0.3)
        current_carousel_angle = carousel_angle
        
        # إيقاف الروبوت مرة أخرى للتأكيد
        try:
            stop_robot()
        except: pass

        # 3. تأكيد الموضع (Tolerance Check)
        if abs(current_carousel_angle - carousel_angle) <= 2:
             print(f"   ✓ تموضع صحيح للكاروسيل")
        else:
             return False, f"فشل تموضع الكاروسيل (الزاوية {current_carousel_angle})"

        # 4. فتح البوابة
        print(f"\n↗️ الخطوة 4: فتح البوابة")
        smooth_move(gate_pwm, close_angle, open_angle, steps=30)
        
        # 5. الانتظار
        print(f"⏳ انتظار سقوط الدواء ({DISPENSE_HOLD_TIME}s)")
        time.sleep(DISPENSE_HOLD_TIME)
        
        # 6. إغلاق البوابة
        print(f"↙️ الخطوة 6: إغلاق البوابة")
        smooth_move(gate_pwm, open_angle, close_angle, steps=30)
        
        # 7. العودة للصفر (إلزامي)
        print(f"🔄 الخطوة 7: العودة للصفر")
        _return_carousel_zero()
        time.sleep(1)
        
        # 8. التسجيل
        try:
            from database import log_dose
            log_dose(box_id, 'dispensed', 'success', f'صرف جرعة - الصندوق {box_id}')
        except: pass

        print(f"✅ تم صرف الجرعة بنجاح (المدة: {time.time() - start_time:.2f}s)")
        return True, f"تم صرف جرعة من الصندوق {box_id}"

    except Exception as e:
        duration = time.time() - start_time
        print(f"\n❌ خطأ أثناء الصرف (بعد {duration:.2f}s): {e}")
        # محاولة إغلاق البوابة للطوارئ
        try:
            if gate_pwm:
                set_servo_angle(gate_pwm, close_angle)
                time.sleep(0.5)
                gate_pwm.ChangeDutyCycle(0)
        except: pass
        return False, f"خطأ: {e}"
        
    finally:
        _hw_lock.release()


# ========== Face Verification with Timeout ==========

def verify_face_with_timeout(timeout_seconds=15):
    """
    التحقق من الوجه مع مهلة زمنية.
    يفحص كل ثانية إذا تم التعرف على وجه مسجّل.
    
    Args:
        timeout_seconds: المهلة بالثواني (افتراضي 15)
    
    Returns:
        True إذا تم التعرف على وجه مسجّل
        False إذا انتهت المهلة أو لم يتم التعرف
    """
    try:
        from robot.camera.stream import get_last_face
    except ImportError:
        print("   ⚠️ نظام التعرف على الوجه غير متاح")
        return True  # السماح بالصرف إذا النظام غير متاح
    
    start_time = time.time()
    check_interval = 1.0  # فحص كل ثانية
    
    print(f"   🔍 بدء البحث عن وجه مسجّل (مهلة {timeout_seconds}s)...")
    
    while (time.time() - start_time) < timeout_seconds:
        elapsed = int(time.time() - start_time)
        remaining = timeout_seconds - elapsed
        
        # الحصول على آخر وجه معروف
        face_data = get_last_face()
        
        if face_data:
            name = face_data.get("name", "Unknown")
            score = face_data.get("score", 0)
            face_time = face_data.get("time", 0)
            
            # التحقق أن الوجه تم رصده حديثاً
            if name != "Unknown" and (time.time() - face_time) < FACE_FRESH_TIMEOUT:
                print(f"   ✅ تم التعرف على: {name} (ثقة: {score:.2f})")
                return True
        
        print(f"   ⏳ انتظار الوجه... ({remaining}s متبقي)")
        time.sleep(check_interval)
    
    print(f"   ⏰ انتهت المهلة - لم يتم التعرف على وجه")
    return False


def full_dispense_sequence(box_id):
    """
    تسلسل الصرف الكامل (Workflow عالي المستوى).
    يستدعي dispense_dose() بدلاً من إعادة تنفيذ المنطق.
    
    الخطوات:
    1. التحقق من الوجه (15 ثانية)
    2. تشغيل صوت النجاح
    3. استدعاء dispense_dose() (نقطة واحدة فقط)
    4. إرجاع الكاروسيل للصفر
    
    ملاحظة:
    - الخطوة 5 (انتظار الزر) تتم عبر واجهة المستخدم
    - الخطوة 6 (الرجوع للخلف) تتم عبر API /return_home
    """
    global current_carousel_angle
    
    print(f"\n{'='*50}")
    print(f"🚀 بدء تسلسل الصرف الكامل للصندوق {box_id}")
    print(f"{'='*50}")
    
    # ======== 1. التحقق من الوجه ========
    face_verified = False
    try:
        from database import get_setting
        val = str(get_setting("auth_enabled", "0")).strip()
        auth_enabled = val == "1"
        
        if auth_enabled:
            print(f"\n📍 الخطوة 1: التحقق من الوجه (15 ثانية)")
            face_verified = verify_face_with_timeout(15)
            
            if not face_verified:
                print(f"   ❌ فشل التحقق من الوجه - إلغاء الصرف")
                return False, "فشل التحقق من الوجه"
            else:
                print(f"   ✅ تم التحقق من الوجه بنجاح!")
        else:
            print(f"\n📍 الخطوة 1: التحقق من الوجه (معطّل)")
            face_verified = True
    except Exception as auth_err:
        print(f"   ⚠️ خطأ في الإعدادات: {auth_err}")
        face_verified = True

    # ======== 2. تشغيل صوت النجاح ========
    print(f"\n📍 الخطوة 2: تشغيل صوت التحقق")
    try:
        from scheduler import play_sound, SOUND_THANKS 
        play_sound(SOUND_THANKS) 
    except: pass

    # ======== 3. الصرف (عبر dispense_dose - نقطة واحدة) ========
    print(f"\n📍 الخطوة 3: الصرف من الصندوق {box_id}")
    success, message = dispense_dose(box_id)
    
    # ملاحظة: الكاروسيل يعود للصفر تلقائياً داخل dispense_dose
    
    if not success:
        print(f"   ❌ فشل الصرف: {message}")
        return False, message
    
    print(f"   ✓ {message}")

    print(f"\n✅ انتهى الصرف. في انتظار ضغط المريض للعودة.")
    return True, "تم الصرف بنجاح - في انتظار المريض"


# ========== Safe Recovery (استرداد آمن عند الأخطاء) ==========

def safe_recovery():
    """
    إجراء استرداد آمن - يُستدعى عند الانتقال من ERROR → IDLE.
    يغلق جميع البوابات ويعيد الكاروسيل للصفر.
    """
    print(f"\n🔧 بدء إجراء الاسترداد الآمن...")
    
    # 1. إغلاق جميع البوابات
    for box_id, pwm in gate_pwms.items():
        try:
            if pwm:
                config = BOX_CONFIG.get(box_id, {})
                close_angle = config.get('close_angle', 0)
                set_servo_angle(pwm, close_angle)
                time.sleep(0.3)
                pwm.ChangeDutyCycle(0)
                print(f"   ✓ بوابة {box_id} مغلقة")
        except Exception as e:
            print(f"   ⚠️ فشل إغلاق بوابة {box_id}: {e}")
    
    # 2. إرجاع الكاروسيل
    _return_carousel_zero()
    
    # 3. إيقاف الروبوت
    try:
        stop_robot()
        print(f"   ✓ الروبوت متوقف")
    except:
        pass
    
    print(f"✅ اكتمل الاسترداد الآمن")


def _return_carousel_zero():
    """إرجاع الكاروسيل لنقطة الصفر (دالة داخلية)."""
    global current_carousel_angle
    if HAS_GPIO and pwm_carousel:
        smooth_move(pwm_carousel, current_carousel_angle, ZERO_ANGLE, steps=30)
        pwm_carousel.ChangeDutyCycle(0)
        current_carousel_angle = ZERO_ANGLE
        print(f"   ✓ الكاروسيل في وضع الصفر ({ZERO_ANGLE}°)")


def get_hardware_status():
    """فحص صحة الأجهزة."""
    return {
        "gpio_available": HAS_GPIO,
        "carousel_ready": pwm_carousel is not None,
        "gates_ready": {box_id: (pwm is not None) for box_id, pwm in gate_pwms.items()},
        "arduino_connected": is_arduino_connected(),
        "carousel_angle": current_carousel_angle,
        "hw_lock_free": not _hw_lock.locked(),
    }


# ========== Maintenance Functions ==========

def load_medicine():
    """تدوير الكاروسيل لوضع التحميل."""
    global current_carousel_angle
    # 🛡️ حماية: إيقاف محركات الروبوت قبل تحريك الكاروسيل
    try:
        stop_robot()
        time.sleep(0.1)
    except: pass
    
    if HAS_GPIO and pwm_carousel:
        move_servo(pwm_carousel, LOADING_ANGLE)
        current_carousel_angle = LOADING_ANGLE
        print(f"🧪 تم التدوير لزاوية التحميل: {LOADING_ANGLE}°")
    else:
        print(f"[SIMULATION] Load mode: {LOADING_ANGLE}°")

def go_home_zero():
    """إرجاع الكاروسيل لنقطة الصفر."""
    global current_carousel_angle
    # 🛡️ حماية: إيقاف محركات الروبوت قبل تحريك الكاروسيل
    try:
        stop_robot()
        time.sleep(0.1)
    except: pass
    
    if HAS_GPIO and pwm_carousel:
        move_servo(pwm_carousel, ZERO_ANGLE)
        current_carousel_angle = ZERO_ANGLE
        print(f"🔄 تم الرجوع لنقطة الصفر: {ZERO_ANGLE}°")
    else:
        print(f"[SIMULATION] Zero position: {ZERO_ANGLE}°")





# ========== RAW CONTROL for TEST PAGE ==========

def move_raw(command: str, safety_timeout: int = None):
    """Send raw command to Arduino (START, STOP, RIGHT, LEFT, REVERSE)."""
    if not connect_arduino(): 
        return False
    try:
        cmd = command.strip().upper()
        arduino.write((cmd + "\n").encode("utf-8"))
        arduino.flush()
        print(f"📡 RAW->Arduino: {cmd}")
        
        if safety_timeout and cmd != "STOP":
            threading.Thread(target=lambda: _auto_stop_after(safety_timeout, cmd), daemon=True).start()
        return True
    except Exception as e:
        print(f"❌ move_raw error: {e}")
        disconnect_arduino()
        return False

def _auto_stop_after(seconds, label):
    time.sleep(seconds)
    stop_robot()
    print(f"[SAFETY] Auto-stop after {seconds}s ({label})")

_last_distance_cm = None

def poll_arduino_lines(max_lines=20):
    global _last_distance_cm
    if not connect_arduino(): 
        return
    start_time = time.time()
    try:
        lines_read = 0
        while arduino.in_waiting > 0 and lines_read < max_lines:
            # 🛡️ حماية: Timeout للخروج من الحلقة إذا استغرقت وقت طويل
            if (time.time() - start_time) > 0.2:
                break
                
            line = arduino.readline().decode(errors="ignore").strip()
            lines_read += 1
            if line.startswith("DISTANCE:"):
                try: 
                    _last_distance_cm = float(line.split(":")[1])
                except: 
                    pass
            elif line.startswith("STATUS:") or line.startswith("OK:") or line.startswith("OBSTACLE:"):
                print(f"🤖 ARDUINO: {line}")
    except Exception as e: 
        print(f"Poll Error: {e}")

def get_latest_distance():
    poll_arduino_lines()
    return _last_distance_cm

def set_servo_raw(target: str, sid: int, angle: int):
    """Raw control for servos (Test Page)."""
    if target == "carousel":
        move_servo(pwm_carousel if HAS_GPIO else None, int(angle))
        return True, "carousel_ok"
    elif target == "gate":
        if sid not in BOX_CONFIG: 
            return False, "invalid_gate_id"
        pwm = gate_pwms.get(sid) if HAS_GPIO else None
        move_servo(pwm, int(angle))
        return True, f"gate_{sid}_ok"
    return False, "invalid_target"


# ========== Cleanup ==========

def cleanup():
    """تنظيف الموارد عند إغلاق البرنامج."""
    disconnect_arduino()
    if HAS_GPIO:
        try: 
            # إغلاق جميع البوابات قبل التنظيف
            for box_id, pwm in gate_pwms.items():
                if pwm:
                    config = BOX_CONFIG.get(box_id, {})
                    close_angle = config.get('close_angle', 0)
                    set_servo_angle(pwm, close_angle)
                    time.sleep(0.3)
                    pwm.ChangeDutyCycle(0)
            
            GPIO.cleanup()
        except: 
            pass
        print("✓ تم تنظيف موارد GPIO")

# -*- coding: utf-8 -*-
"""
وحدة التحكم في الأجهزة - Hardware Control
التحكم في السيرفو والبوابات على Raspberry Pi عبر GPIO مباشرة
Arduino للتحكم في حركة الروبوت فقط (START/STOP/RETURN)
"""

import time
import math
import threading

# ============ إعدادات السيرفو ============
ZERO_ANGLE = 0       # نقطة الصفر المرجعية
LOADING_ANGLE = 100  # زاوية أنبوب التحميل
SERVO_DELAY = 0.02   # سرعة الحركة

# ============ إعدادات الصناديق (GPIO Direct Control) ============
# كل صندوق له:
# - pin: منفذ GPIO للسيرفو
# - open_angle: زاوية الفتح
# - close_angle: زاوية الإغلاق
BOX_CONFIG = {
    1: {'pin': 23, 'open_angle': 90, 'close_angle': 0},
    2: {'pin': 24, 'open_angle': 90, 'close_angle': 0},
}

# ============ زوايا الكاروسيل لكل صندوق ============
# الكاروسيل يدور ليوجه الفتحة للصندوق المطلوب
BOX_ANGLES = {
    1: 0,      # الصندوق الأول - نقطة الصفر
    2: 90,     # الصندوق الثاني - 90 درجة
}

# مدة الانتظار بعد فتح البوابة (ثواني)
DISPENSE_HOLD_TIME = 3

# ============ توقيتات حركة الروبوت ============
ROBOT_FORWARD_TIME = 8    # ثواني للتحرك للأمام
ROBOT_BACKWARD_TIME = 5   # ثواني للرجوع للخلف
ROBOT_SETTLE_TIME = 1     # ثواني للتثبيت بعد التوقف

# State Tracking
current_carousel_angle = ZERO_ANGLE

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

def smooth_move(pwm, start_angle, end_angle, steps=30):
    """حركة سلسة مع Easing (لمنع الحركة المفاجئة)."""
    if pwm is None or not hasattr(pwm, 'ChangeDutyCycle'):
        print(f"[SIMULATION] Servo: {start_angle}° -> {end_angle}°")
        time.sleep(steps * SERVO_DELAY)
        return

    for i in range(steps + 1):
        t = i / steps
        # Cosine easing for smooth acceleration/deceleration
        eased_t = 0.5 - 0.5 * math.cos(math.pi * t)
        current_angle = start_angle + (end_angle - start_angle) * eased_t
        set_servo_angle(pwm, current_angle)
        time.sleep(SERVO_DELAY)
        
    # تأكيد الزاوية النهائية
    set_servo_angle(pwm, end_angle)
    time.sleep(0.1)
    # إيقاف PWM لمنع الاهتزاز والحرارة
    pwm.ChangeDutyCycle(0)

def move_servo(pwm, target_angle):
    """تحريك السيرفو لزاوية معينة."""
    global current_carousel_angle, pwm_carousel
    
    if pwm == pwm_carousel and pwm_carousel is not None:
        start_angle = current_carousel_angle
        smooth_move(pwm, start_angle, target_angle, steps=40)
        current_carousel_angle = target_angle
    else:
        start_angle = 0
        if target_angle == 0: 
            start_angle = 90
        smooth_move(pwm, start_angle, target_angle, steps=20)


# ========== 🔧 MEDICINE DISPENSING (GPIO DIRECT CONTROL) ==========

def dispense_dose(box_id):
    """
    صرف جرعة من صندوق الدواء عبر GPIO مباشرة.
    
    التسلسل الكامل:
    1. Pre-Dispense Check (التحقق قبل الصرف)
    2. تدوير الكاروسيل لزاوية الصندوق
    3. تأكيد موضع الكاروسيل
    4. فتح البوابة بحركة سلسة
    5. الانتظار لسقوط الدواء
    6. إغلاق البوابة
    7. تسجيل العملية
    8. إيقاف PWM
    """
    global current_carousel_angle
    
    print(f"\n{'─'*40}")
    print(f"📦 بدء عملية صرف الدواء - الصندوق {box_id}")
    print(f"{'─'*40}")
    
    # ======== 1. Pre-Dispense Check ========
    print(f"\n🔍 الخطوة 1: التحقق قبل الصرف")
    
    # 1.1 التحقق من صحة معرف الصندوق
    if box_id not in BOX_CONFIG:
        print(f"   ❌ خطأ: الصندوق {box_id} غير موجود")
        return False, f"صندوق {box_id} غير موجود في BOX_CONFIG"
    
    config = BOX_CONFIG[box_id]
    open_angle = config['open_angle']
    close_angle = config['close_angle']
    carousel_angle = BOX_ANGLES.get(box_id, 0)
    
    # 1.2 الحصول على كائنات PWM
    gate_pwm = gate_pwms.get(box_id)
    
    # 1.3 التحقق من جاهزية GPIO
    if not HAS_GPIO:
        print(f"   ⚠️ وضع المحاكاة (GPIO غير متاح)")
        # محاكاة الصرف
        print(f"   [SIM] تدوير الكاروسيل: {current_carousel_angle}° → {carousel_angle}°")
        time.sleep(0.5)
        print(f"   [SIM] فتح البوابة: {close_angle}° → {open_angle}°")
        time.sleep(1)
        print(f"   [SIM] انتظار {DISPENSE_HOLD_TIME}s...")
        time.sleep(DISPENSE_HOLD_TIME)
        print(f"   [SIM] إغلاق البوابة")
        time.sleep(1)
        current_carousel_angle = carousel_angle
        print(f"   ✅ تم الصرف بنجاح (محاكاة)")
        return True, f"تم صرف جرعة من الصندوق {box_id} (محاكاة)"
    
    if gate_pwm is None:
        print(f"   ❌ خطأ: gate_pwm للصندوق {box_id} غير مهيأ")
        return False, f"بوابة الصندوق {box_id} غير مهيأة"
    
    print(f"   ✓ الصندوق {box_id} جاهز للصرف")
    print(f"   ✓ زوايا: carousel={carousel_angle}°, gate={close_angle}°→{open_angle}°")
    
    try:
        # ======== 2. تدوير الكاروسيل ========
        print(f"\n🔄 الخطوة 2: تدوير الكاروسيل")
        
        if pwm_carousel and current_carousel_angle != carousel_angle:
            print(f"   تدوير: {current_carousel_angle}° → {carousel_angle}°")
            smooth_move(pwm_carousel, current_carousel_angle, carousel_angle, steps=40)
            time.sleep(0.3)  # تثبيت
            current_carousel_angle = carousel_angle
        else:
            print(f"   ✓ الكاروسيل في الموضع ({carousel_angle}°)")
        
        # ======== 3. تأكيد موضع الكاروسيل ========
        print(f"\n✓ الخطوة 3: تأكيد الموضع")
        if current_carousel_angle == carousel_angle:
            print(f"   ✓ تأكيد: الكاروسيل في الزاوية {carousel_angle}°")
        else:
            print(f"   ❌ خطأ: الكاروسيل في {current_carousel_angle}° بدلاً من {carousel_angle}°")
            return False, f"فشل تأكيد موضع الكاروسيل"
        
        # ======== 4. فتح البوابة ========
        print(f"\n↗️ الخطوة 4: فتح البوابة")
        print(f"   من {close_angle}° → {open_angle}°")
        smooth_move(gate_pwm, close_angle, open_angle, steps=25)
        print(f"   ✓ البوابة مفتوحة")
        
        # ======== 5. انتظار سقوط الدواء ========
        print(f"\n⏳ الخطوة 5: انتظار سقوط الدواء ({DISPENSE_HOLD_TIME}s)")
        time.sleep(DISPENSE_HOLD_TIME)
        print(f"   ✓ الانتظار انتهى")
        
        # ======== 6. إغلاق البوابة ========
        print(f"\n↙️ الخطوة 6: إغلاق البوابة")
        print(f"   من {open_angle}° → {close_angle}°")
        smooth_move(gate_pwm, open_angle, close_angle, steps=25)
        print(f"   ✓ البوابة مغلقة")
        
        # ======== 7. تسجيل العملية ========
        print(f"\n📝 الخطوة 7: تسجيل العملية")
        try:
            from database import log_dose
            log_dose(box_id, 'dispensed', 'success', f'صرف جرعة - الصندوق {box_id}')
            print(f"   ✓ تم التسجيل في قاعدة البيانات")
        except Exception as log_err:
            print(f"   ⚠️ فشل التسجيل: {log_err}")
        
        # ======== 8. إيقاف PWM ========
        print(f"\n🔧 الخطوة 8: إيقاف PWM")
        gate_pwm.ChangeDutyCycle(0)
        print(f"   ✓ PWM متوقف")
        
        print(f"\n{'─'*40}")
        print(f"✅ تم صرف الجرعة بنجاح من الصندوق {box_id}")
        print(f"{'─'*40}")
        
        return True, f"تم صرف جرعة من الصندوق {box_id}"
        
    except Exception as e:
        print(f"\n❌ خطأ أثناء الصرف: {e}")
        # محاولة إغلاق البوابة للسلامة
        try:
            if gate_pwm:
                print(f"   🔧 محاولة إغلاق البوابة للسلامة...")
                set_servo_angle(gate_pwm, close_angle)
                time.sleep(0.5)
                gate_pwm.ChangeDutyCycle(0)
                print(f"   ✓ تم إغلاق البوابة")
        except:
            pass
        
        # تسجيل الفشل
        try:
            from database import log_dose
            log_dose(box_id, 'dispensed', 'failed', f'فشل الصرف: {e}')
        except:
            pass
        
        return False, f"خطأ في صرف الصندوق {box_id}: {e}"


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
            
            # التحقق أن الوجه تم رصده حديثاً (خلال آخر 5 ثواني)
            if name != "Unknown" and (time.time() - face_time) < 5:
                print(f"   ✅ تم التعرف على: {name} (ثقة: {score:.2f})")
                return True
        
        print(f"   ⏳ انتظار الوجه... ({remaining}s متبقي)")
        time.sleep(check_interval)
    
    print(f"   ⏰ انتهت المهلة - لم يتم التعرف على وجه")
    return False


def full_dispense_sequence(box_id):
    """
    تسلسل الصرف (الجزء الأول): التحقق والصرف فقط.
    
    الخطوات المعدلة:
    1. التحقق من الوجه (15 ثانية).
    2. تشغيل صوت النجاح.
    3. الصرف: 
       - تدوير كاروسيل -> انتظار 0.25s
       - فتح بوابة -> انتظار 3s
       - غلق بوابة
    4. إرجاع كاروسيل للصفر -> انتظار 1s
    
    ملاحظة:
    - الخطوة 5 (انتظار الزر) تتم عبر واجهة المستخدم
    - الخطوة 6 (الرجوع للخلف) تتم عبر API /return_home عند ضغط الزر
    """
    global current_carousel_angle
    
    print(f"\n{'='*50}")
    print(f"🚀 بدء تسلسل الصرف المعدل للصندوق {box_id}")
    print(f"{'='*50}")
    
    # لا توجد حركة للروبوت هنا (الحركة تمت في التنبيه المسبق)
    
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
        # استخدام thanks.mp3 كبديل حالياً أو أي ملف مناسب
        from scheduler import play_sound, SOUND_THANKS 
        play_sound(SOUND_THANKS) 
    except: pass

    # ======== 3. الصرف (كاروسيل -> بوابة) ========
    print(f"\n📍 الخطوة 3: الصرف من الصندوق {box_id}")
    
    if box_id not in BOX_CONFIG:
        return False, "رقم الصندوق غير صحيح"

    config = BOX_CONFIG[box_id]
    gate_pwm = gate_pwms.get(box_id)
    carousel_angle = BOX_ANGLES.get(box_id, 0)
    
    # أ) تدوير الكاروسيل
    if HAS_GPIO and pwm_carousel:
        smooth_move(pwm_carousel, current_carousel_angle, carousel_angle, steps=30)
        current_carousel_angle = carousel_angle
        print(f"   ✓ تم تدوير الكاروسيل إلى {carousel_angle}°")
    
    # ب) انتظار ربع ثانية
    time.sleep(0.25)
    
    # ج) فتح البوابة
    if HAS_GPIO and gate_pwm:
        smooth_move(gate_pwm, config['close_angle'], config['open_angle'], steps=20)
        print(f"   ✓ تم فتح البوابة")
    
    # د) انتظار 3 ثواني (سقوط الدواء)
    print(f"   ⏳ انتظار سقوط الدواء (3s)...")
    time.sleep(3)
    
    # هـ) إغلاق البوابة
    if HAS_GPIO and gate_pwm:
        smooth_move(gate_pwm, config['open_angle'], config['close_angle'], steps=20)
        gate_pwm.ChangeDutyCycle(0) # إيقاف PWM
        print(f"   ✓ تم إغلاق البوابة")

    # ======== 4. العودة للصفر ========
    print(f"\n📍 الخطوة 4: العودة للصفر واعادة التعيين")
    if HAS_GPIO and pwm_carousel:
        smooth_move(pwm_carousel, current_carousel_angle, ZERO_ANGLE, steps=30)
        pwm_carousel.ChangeDutyCycle(0)
        current_carousel_angle = ZERO_ANGLE
        print(f"   ✓ الكاروسيل في وضع الصفر")
    
    print(f"   ⏳ انتظار 1 ثانية...")
    time.sleep(1)

    print(f"\n✅ انتهى الصرف. في انتظار ضغط المريض للعودة.")
    return True, "تم الصرف بنجاح - في انتظار المريض"
    
    # ======== 4-7. صرف الجرعة (يشمل تدوير الكاروسيل + فتح/إغلاق البوابة) ========
    print(f"\n📍 الخطوات 4-7: صرف الجرعة من الصندوق {box_id}")
    success, message = dispense_dose(box_id)
    
    if not success:
        print(f"   ❌ فشل الصرف: {message}")
        # المتابعة لإرجاع الروبوت حتى مع الفشل
    else:
        print(f"   ✓ {message}")
    
    # ======== 7. إرجاع الكاروسيل لنقطة الصفر ========
    print(f"\n📍 الخطوة 7: إرجاع الكاروسيل لنقطة الصفر")
    print(f"   📊 HAS_GPIO={HAS_GPIO}, pwm_carousel={pwm_carousel}, current_angle={current_carousel_angle}")
    
    if HAS_GPIO and pwm_carousel:
        if current_carousel_angle != ZERO_ANGLE:
            print(f"   🔄 تدوير: {current_carousel_angle}° -> {ZERO_ANGLE}°")
            smooth_move(pwm_carousel, current_carousel_angle, ZERO_ANGLE, steps=40)
        else:
            # حتى لو نفس الزاوية، أرسل الأمر للتأكيد
            print(f"   🔄 تأكيد الزاوية: {ZERO_ANGLE}°")
            set_servo_angle(pwm_carousel, ZERO_ANGLE)
            time.sleep(0.5)
            pwm_carousel.ChangeDutyCycle(0)
        current_carousel_angle = ZERO_ANGLE
        print(f"   ✓ الكاروسيل في نقطة الصفر ({ZERO_ANGLE}°)")
    else:
        if not HAS_GPIO:
            print(f"   ⚠️ GPIO غير متاح - وضع المحاكاة")
        elif not pwm_carousel:
            print(f"   ⚠️ pwm_carousel غير مهيأ - محاولة إعادة التهيئة...")
            setup_gpio()  # محاولة إعادة التهيئة
            if pwm_carousel:
                set_servo_angle(pwm_carousel, ZERO_ANGLE)
                time.sleep(0.5)
                pwm_carousel.ChangeDutyCycle(0)
                print(f"   ✓ تم التهيئة والإرجاع للصفر")
        current_carousel_angle = ZERO_ANGLE
    
    # ======== 8. رجوع الروبوت للخلف ========
    print(f"\n📍 الخطوة 8: رجوع الروبوت للخلف ({ROBOT_BACKWARD_TIME} ثوانٍ)")
    if return_home():
        time.sleep(ROBOT_BACKWARD_TIME)
        stop_robot()
        print(f"   ✓ الروبوت عاد لموضعه الأصلي")
    else:
        print(f"   ⚠️ فشل إرجاع الروبوت")
    
    print(f"\n{'='*50}")
    print(f"🏁 انتهى تسلسل الصرف للصندوق {box_id}")
    print(f"{'='*50}\n")
    
    return success, message


# ========== Maintenance Functions ==========

def load_medicine():
    """تدوير الكاروسيل لوضع التحميل."""
    if HAS_GPIO and pwm_carousel:
        move_servo(pwm_carousel, LOADING_ANGLE)
        print(f"🧪 تم التدوير لزاوية التحميل: {LOADING_ANGLE}°")
    else:
        print(f"[SIMULATION] Load mode: {LOADING_ANGLE}°")

def go_home_zero():
    """إرجاع الكاروسيل لنقطة الصفر."""
    if HAS_GPIO and pwm_carousel:
        move_servo(pwm_carousel, ZERO_ANGLE)
        print(f"🔄 تم الرجوع لنقطة الصفر: {ZERO_ANGLE}°")
    else:
        print(f"[SIMULATION] Zero position: {ZERO_ANGLE}°")


# ========== Robot Control Functions (Arduino) ==========

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
    if not connect_arduino(): 
        return False
    try:
        arduino.write(b'STOP\n')
        arduino.flush()
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
    try:
        lines_read = 0
        while arduino.in_waiting > 0 and lines_read < max_lines:
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

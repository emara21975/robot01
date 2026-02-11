# -*- coding: utf-8 -*-
"""
نظام توزيع الأدوية الذكي - Flask Server
ملف التطبيق الرئيسي (منظم ومختصر)
"""

from flask import Flask, request, jsonify, render_template, Response
import time
import threading

# استيراد وحدة قاعدة البيانات
from database import (
    init_database, get_all_schedules, save_schedule, 
    log_dose, get_dose_logs, get_dose_statistics, get_today_doses,
    get_setting, save_setting
)

# استيراد وحدة الأجهزة
from hardware import (
    HAS_GPIO, setup_gpio, dispense_dose, load_medicine, 
    go_home_zero, start_robot, stop_robot, get_robot_status,
    is_arduino_connected, connect_arduino, return_home,
    safe_recovery, get_hardware_status
)

# استيراد نظام الجدولة
from scheduler import (
    start_scheduler, stop_scheduler, is_scheduler_running,
    get_robot_moved_status, reset_robot_moved_status
)

# استيراد آلة الحالة (State Machine)
from robot.state_machine import robot_state, RobotState

# استيراد نظام السجلات (Audit Log)
try:
    from robot.audit_log import log_event
except ImportError:
    def log_event(*args, **kwargs): pass

# استيراد نظام التعرف على الوجه (من stream فقط)
try:
    from robot.camera.stream import get_last_face, get_face_engine, force_reload_faces
except ImportError:
    def get_last_face(): return {"name": "Unknown", "score": 0.0, "time": 0}
    def get_face_engine(): return None
    def force_reload_faces(): pass


# ============ إنشاء التطبيق ============
app = Flask(__name__)


# ========== صفحات HTML ==========


BOX_COUNT = 4  # عدد الصناديق في النظام

@app.route("/")
def index():
    """لوحة التحكم الرئيسية."""
    return render_template("admin.html", boxes=range(1, BOX_COUNT + 1))


@app.route("/patient")
def patient():
    """شاشة المريض."""
    return render_template("patient.html", boxes=range(1, BOX_COUNT + 1))


@app.route("/statistics")
def statistics():
    """صفحة الإحصائيات."""
    return render_template("statistics.html")


# ========== API الجداول ==========

@app.route("/api/schedules", methods=["GET"])
def get_schedules():
    """الحصول على جداول الأدوية من قاعدة البيانات."""
    try:
        schedules = get_all_schedules()
        return jsonify(schedules)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/schedules", methods=["POST"])
def update_schedules():
    """تحديث جداول الأدوية وحفظها في قاعدة البيانات."""
    try:
        data = request.get_json()
        box = int(data.get("box", 0))
        
        if 1 <= box <= BOX_COUNT:
            save_schedule(
                box_id=box,
                hour=data.get("hour"),
                minute=data.get("minute"),
                enabled=data.get("enabled", False),
                days=data.get("days", []),
                medicine_name=data.get("medicine_name"),
                stock_count=data.get("stock_count"),
                dose_per_dispense=data.get("dose_per_dispense"),
                low_stock_threshold=data.get("low_stock_threshold"),
                pharmacy_url=data.get("pharmacy_url")
            )
            # تسجيل الحدث
            log_dose(box, 'schedule_updated', 'success', 
                     f"تم تحديث الجدول: {data.get('hour')}:{data.get('minute')}")
            return jsonify({"status": "success", "message": "تم حفظ الجدول بنجاح"})
        return jsonify({"status": "error", "message": "رقم الصندوق غير صحيح"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ========== API السجلات والإحصائيات ==========

@app.route("/api/logs", methods=["GET"])
def get_logs():
    """الحصول على سجل الجرعات."""
    try:
        box_id = request.args.get("box", type=int)
        limit = request.args.get("limit", 50, type=int)
        logs = get_dose_logs(box_id, limit)
        return jsonify(logs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/logs/today", methods=["GET"])
def get_today_logs():
    """الحصول على جرعات اليوم."""
    try:
        logs = get_today_doses()
        return jsonify(logs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/statistics", methods=["GET"])
def get_stats():
    """الحصول على إحصائيات الجرعات."""
    try:
        stats = get_dose_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ========== Video Streaming ==========
try:
    from robot.camera.stream import video_stream
except ImportError as e:
    print(f"⚠️ خطأ في استيراد الكاميرا: {e}")
    def video_stream():
        return "Camera Error", 500

@app.route('/video')
def video():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return video_stream()


# ========== API الإعدادات ==========

@app.route("/api/settings", methods=["GET", "POST"])
def handle_settings():
    """التحكم في إعدادات النظام."""
    if request.method == "POST":
        data = request.get_json()
        if "auth_enabled" in data:
            save_setting("auth_enabled", "1" if data["auth_enabled"] else "0")
        return jsonify({"status": "success", "message": "تم حفظ الإعدادات"})
    else:
        val = str(get_setting("auth_enabled", "0")).strip()
        auth_enabled = val == "1"
        return jsonify({"auth_enabled": auth_enabled})


# ========== Face Enrollment ==========

@app.route("/enroll")
def enroll_page():
    """صفحة تسجيل وجه مريض جديد."""
    return render_template("enroll.html")

@app.route("/enroll-test")
def enroll_test_page():
    """صفحة تشخيص مشاكل التسجيل."""
    return render_template("enroll_test.html")

@app.route("/api/enroll_face", methods=["POST"])
def api_enroll_face():
    """API لحفظ وجه جديد من الكاميرا الحالية."""
    try:
        from robot.camera.stream import get_face_engine, force_reload_faces
        from robot.camera.camera import camera
        from robot.camera.face_db import save_face
        
        data = request.get_json()
        name = data.get("name")
        
        if not name:
            return jsonify({"status": "error", "message": "الاسم مطلوب"}), 400
            
        if not camera:
            return jsonify({"status": "error", "message": "الكاميرا غير متصلة"}), 500
            
        # Get frame
        frame = camera.get_frame()
        if frame is None:
             return jsonify({"status": "error", "message": "فشل التقاط صورة من الكاميرا"}), 500
             
        # Detect Face
        engine = get_face_engine()
        if not engine:
             return jsonify({"status": "error", "message": "محرك الوجوه غير جاهز"}), 500
             
        faces = engine.detect(frame)
        
        if len(faces) == 0:
             return jsonify({"status": "error", "message": "لم يتم العثور على وجه! تأكد من الإضاءة وواجه الكاميرا."}), 400
             
        if len(faces) > 1:
             return jsonify({"status": "error", "message": "تم كشف أكثر من وجه. يرجى أن يكون شخص واحد فقط أمام الكاميرا."}), 400
             
        # Save Face
        face = faces[0]
        save_face(name, face.embedding)
        
        # Trigger DB Refresh
        force_reload_faces()
        
        return jsonify({"status": "success", "message": f"تم تسجيل الوجه بنجاح: {name}"})
        
    except Exception as e:
        print(f"Enrollment Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/verify-face")
def verify():
    """✨ التحقق البسيط من الوجه - يعتمد فقط على آخر نتيجة من الكاميرا."""
    
    # 0. التحقق من تفعيل النظام
    val = str(get_setting("auth_enabled", "0")).strip()
    auth_enabled = val == "1"
    
    print(f"🔍 [VERIFY] auth_enabled من DB: '{val}' → النتيجة: {auth_enabled}")
    
    if not auth_enabled:
        # ⚠️ النظام معطل - السماح المباشر (بدون تحقق)
        log_event("VERIFY", "SKIPPED", "Authentication disabled - auto-approved", "INFO")
        robot_state.set(RobotState.VERIFIED)
        return jsonify({
            "verified": True,
            "reason": "AUTH_DISABLED",
            "message": "تم السماح بالفتح مباشرة (التحقق معطّل)"
        })
    
    # 1. فحص إذا كان النظام مشغول
    if robot_state.current in [RobotState.VERIFYING, RobotState.DISPENSING]:
        return jsonify({"verified": False, "reason": "BUSY", "message": "النظام مشغول حالياً"}), 200

    # 2. تغيير الحالة للتحقق
    robot_state.set(RobotState.VERIFYING)

    try:
        # 3. قراءة آخر وجه تم التعرف عليه من الكاميرا
        current_face = get_last_face()
        now = time.time()
        
        # 4. التحقق إذا كان الوجه حديث (آخر 5 ثواني)
        if (now - current_face["time"]) < 5.0:
            name = current_face["name"]
            score = current_face.get("score", 0)
            
            if name != "Unknown":
                # ✅ نجح التحقق
                msg = f"أهلاً {name}"
                log_event("VERIFY", "VERIFIED", f"Face matched: {name} (score: {score:.2f})", "SUCCESS")
                robot_state.set(RobotState.VERIFIED)
                return jsonify({
                    "verified": True, 
                    "reason": "FACE_MATCH", 
                    "message": msg,
                    "name": name,
                    "score": score
                })
            else:
                # ❌ وجه مش معروف
                log_event("VERIFY", "REJECTED", "Unknown face detected", "FAIL")
                robot_state.set(RobotState.IDLE)
                return jsonify({
                    "verified": False, 
                    "reason": "UNKNOWN_FACE", 
                    "message": "وجه غير مسجل! اضغط 'تسجيل' أولاً"
                })
        else:
            # ⚠️ مفيش وجه اتشاف حديثاً
            robot_state.set(RobotState.IDLE)
            return jsonify({
                "verified": False, 
                "reason": "NO_FACE", 
                "message": "لم يتم رصد وجه. تأكد من النظر للكاميرا"
            })

    except Exception as e:
        # ❌ خطأ تقني
        robot_state.set(RobotState.IDLE)
        print(f"❌ Verify Error: {e}")
        log_event("VERIFY", "ERROR", str(e), "ERROR")
        return jsonify({
            "verified": False, 
            "reason": "ERROR", 
            "message": "خطأ في النظام"
        }), 500


# ========== Camera Control API ==========

@app.route("/camera/start", methods=["POST"])
def camera_start():
    """تشغيل الكاميرا عند الطلب."""
    try:
        from robot.camera.camera import camera
        if camera:
            success = camera.start()
            if success:
                return jsonify({"status": "success", "message": "تم تشغيل الكاميرا", "running": True})
            else:
                return jsonify({"status": "error", "message": "فشل تشغيل الكاميرا"}), 500
        return jsonify({"status": "error", "message": "الكاميرا غير متاحة"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/camera/stop", methods=["POST"])
def camera_stop():
    """إيقاف الكاميرا لتوفير الموارد."""
    try:
        from robot.camera.camera import camera
        if camera:
            camera.stop()
            return jsonify({"status": "success", "message": "تم إيقاف الكاميرا", "running": False})
        return jsonify({"status": "error", "message": "الكاميرا غير متاحة"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/camera/status", methods=["GET"])
def camera_status():
    """الحصول على حالة الكاميرا."""
    try:
        from robot.camera.camera import camera
        if camera:
            return jsonify({
                "status": "success",
                "running": camera.is_running()
            })
        return jsonify({"status": "error", "running": False, "message": "الكاميرا غير متاحة"})
    except Exception as e:
        return jsonify({"status": "error", "running": False, "message": str(e)})


# ========== API التحكم في الصناديق ==========

@app.route("/open_box", methods=["POST"])
def open_box():
    """فتح صندوق دواء وصرف الجرعة (مع التحقق المشروط وآلة الحالة)."""
    try:
        data = request.get_json(silent=True) or {}
        box = int(data.get("box", 0))
        
        # 🚨 صرف طوارئ (يدوي) - الروبوت لم يتحرك
        reset_robot_moved_status()
        
        # 0. التحقق من تفعيل الكاميرا
        val = str(get_setting("auth_enabled", "0")).strip()
        auth_enabled = val == "1"
        
        auth_msg = "تم تخطي التحقق (النظام معطل)"
        
        # ✅ إذا النظام مفعل → لازم التحقق من الوجه
        if auth_enabled:
            # التحقق من State Machine
            if robot_state.current != RobotState.VERIFIED:
                 log_dose(box, 'auth_failed', 'failed', "رفض الصرف: لم يتم التحقق من الوجه")
                 log_event("DISPENSE_DENIED", robot_state.current, f"Box {box}: Auth required but not verified", "FAIL")
                 return jsonify({
                    "status": "⛔ رفض الصرف: يرجى التحقق من الوجه أولاً",
                    "error": "auth_failed",
                    "can_confirm": False
                }), 403
            auth_msg = "تم التحقق من الهوية بنجاح ✅"
        else:
            # ⚠️ النظام معطل → السماح بالصرف المباشر
            print(f"🔓 التحقق معطل، السماح بالصرف المباشر للصندوق {box}")
            auth_msg = "تم تخطي التحقق (نظام الوجه معطل)"

        # تسجيل الرسالة
        print(f"🔓 {auth_msg}")

        # 1. التحقق من المخزون
        from database import get_schedule
        schedule = get_schedule(box)
        
        if schedule:
            stock = schedule.get('stock_count', 0) or 0
            dose = schedule.get('dose_per_dispense', 1) or 1
            
            if stock < dose:
                return jsonify({
                    "status": "✗ عذراً، المخزون غير كافٍ للصرف!",
                    "error": "low_stock"
                }), 400

        # State Transition -> DISPENSING
        robot_state.set(RobotState.DISPENSING)
        log_event("DISPENSE_START", robot_state.current, f"Box: {box}", "INFO")

        try:
            # 🔊 تشغيل صوت الطوارئ
            try:
                from scheduler import play_sound, SOUND_EMERGENCY
                play_sound(SOUND_EMERGENCY)
            except Exception as sound_err:
                print(f"⚠️ خطأ في تشغيل الصوت: {sound_err}")
            
            # 2. محاولة الصرف
            success, message = dispense_dose(box)
            
            if success:
                log_event("DISPENSE_DONE", robot_state.current, f"Box: {box} - Success", "SUCCESS")
                # 3. تحديث المخزون
                warning_msg = None
                pharmacy_url = None
                
                if schedule:
                    new_stock = max(0, stock - dose)
                    save_schedule(
                        box_id=box,
                        hour=schedule['hour'],
                        minute=schedule['minute'],
                        enabled=schedule['enabled'],
                        days=schedule['days'],
                        medicine_name=schedule['medicine_name'],
                        stock_count=new_stock,
                        dose_per_dispense=dose,
                        low_stock_threshold=schedule.get('low_stock_threshold', 5),
                        pharmacy_url=schedule.get('pharmacy_url')
                    )
                    
                    # التحقق من الحد الأدنى
                    threshold = schedule.get('low_stock_threshold', 5) or 5
                    if new_stock < threshold:
                        warning_msg = f"تنبيه: المخزون منخفض ({new_stock} قرص)!"
                        pharmacy_url = schedule.get('pharmacy_url')
    
                log_dose(box, 'dispensed', 'success', f"{auth_msg} - تم الصرف")
                
                # الصوت سيعمل عند ضغط المريض على "تم أخذ الدواء"
                # ملاحظة: العودة للصفر تتم تلقائياً داخل hardware.dispense_dose الآن
                response = {"status": f"✓ {message}"}
                if warning_msg:
                    response["warning_message"] = warning_msg
                    response["pharmacy_url"] = pharmacy_url
                    
                return jsonify(response)
            else:
                return jsonify({"status": f"✗ {message}"}), 400
        finally:
             # الانتقال لـ WAIT_CONFIRM بعد الصرف الناجح، أو IDLE عند الفشل
             if robot_state.current == RobotState.DISPENSING:
                 robot_state.set(RobotState.WAIT_CONFIRM)
             elif robot_state.current != RobotState.WAIT_CONFIRM:
                 robot_state.set(RobotState.IDLE)
            
    except Exception as e:
        # استرداد آمن عند الخطأ
        try:
            safe_recovery()
        except:
            pass
        robot_state.force_idle(f"open_box error: {e}")
        return jsonify({"status": f"✗ خطأ: {str(e)}"}), 500


@app.route("/load_mode", methods=["POST"])
def load_mode():
    """تدوير العلبة لوضع إدخال الدواء."""
    try:
        load_medicine()
        
        # ⏳ انتظار المستخدم لتعبئة الدواء
        # ملاحظة: المستخدم يضغط زر آخر بعد التعبئة للعودة للصفر
        # أو يمكن إضافة sleep طويل (مثلاً 10 ثواني)
        
        return jsonify({"status": "✓ تم تدوير العلبة لوضع التحميل - اضغط زر 'صندوق 1' للعودة بعد التعبئة"})
    except Exception as e:
        return jsonify({"status": f"✗ خطأ: {str(e)}"}), 500


# ... existing code ...

def monitor_movement(duration=30):
    """Safety timeout to stop robot after a set duration."""
    time.sleep(duration)
    if robot_running:
        print(f"⏰ Safety Timeout ({duration}s): Stopping Robot.")
        stop_robot()
        # Note: global robot_running update happens in stop_robot() wrapper or we should update it here?
        # The API /robot/stop updates the global. Here we call hardware.stop_robot().
        # We should ideally call the API logic or update global, but hardware.stop_robot() is the core.

@app.route("/return_home", methods=["POST"])
def go_home_return():
    """إرجاع الروبوت لنقطة البداية (Return to Home)."""
    try:
        # 🔊 تشغيل صوت الشكر عند التأكيد
        try:
            from scheduler import play_sound, SOUND_THANKS
            play_sound(SOUND_THANKS)
        except Exception as sound_err:
            print(f"⚠️ خطأ في تشغيل الصوت: {sound_err}")
        
<<<<<<< HEAD
        # تغيير الحالة إلى RETURNING
        if robot_state.current in [RobotState.WAIT_CONFIRM, RobotState.IDLE,
                                    RobotState.DISPENSING]:
            robot_state.set(RobotState.RETURNING)
        
        if return_home():
             # Start Safety Timer (30 seconds)
             threading.Thread(target=monitor_movement, args=(30,), daemon=True).start()
             
             # إطلاق قفل العملية
             robot_state.release_operation()
             
             # جدولة العودة لـ IDLE بعد 10 ثواني (وقت كافي للعودة)
             def _finish_return():
                 time.sleep(10)
                 if robot_state.current == RobotState.RETURNING:
                     robot_state.force_idle("return home completed")
             threading.Thread(target=_finish_return, daemon=True).start()
             
             return jsonify({"status": "✓ شكراً لك! جاري الرجوع..."})
        else:
             robot_state.force_idle("return_home failed")
             return jsonify({"status": "✗ فشل إرسال أمر الرجوع"}), 500
    except Exception as e:
        robot_state.force_idle(f"return_home error: {e}")
=======
        # ✅ تحقق: هل الروبوت تحرك للأمام؟
        robot_status = get_robot_moved_status()
        print(f"🔍 /return_home: robot_moved_status = {robot_status}")
        
        if robot_status:
            # الصرف التلقائي - الروبوت تحرك → يجب أن يرجع
            print("🔙 الروبوت سيرجع للخلف (صرف تلقائي)")
            if return_home():
                 # Start Safety Timer (30 seconds)
                 threading.Thread(target=monitor_movement, args=(30,), daemon=True).start()
                 reset_robot_moved_status()  # إعادة تعيين
                 print("✅ تم إعادة تعيين robot_moved_forward إلى False")
                 return jsonify({"status": "✓ شكراً لك! جاري الرجوع..."})
            else:
                 return jsonify({"status": "✗ فشل إرسال أمر الرجوع"}), 500
        else:
            # صرف طوارئ - الروبوت لم يتحرك → لا يرجع
            print("🏠 الروبوت لم يتحرك (صرف طوارئ) - لا حاجة للرجوع")
            return jsonify({"status": "✓ شكراً لك! نتمنى لك الشفاء العاجل ❤️"})
            
    except Exception as e:
        reset_robot_moved_status()  # إعادة تعيين عند الخطأ
>>>>>>> 7bb6203313304bb920a8e7a4bc132c55be3998bf
        return jsonify({"status": f"✗ خطأ: {str(e)}"}), 500


@app.route("/go_zero", methods=["POST"])
def go_zero():
    """إرجاع العلبة لنقطة الصفر."""
    try:
        go_home_zero()
        return jsonify({"status": "✓ تمت العودة لنقطة الصفر"})
    except Exception as e:
        return jsonify({"status": f"✗ خطأ: {str(e)}"}), 500


# ========== API التحكم في الروبوت ==========

robot_running = False

@app.route("/robot/start", methods=["POST"])
def robot_start():
    """بدء تشغيل الروبوت."""
    global robot_running
    
    if start_robot():
        robot_running = True
        # Start Safety Timer (30 seconds)
        threading.Thread(target=monitor_movement, args=(30,), daemon=True).start()
        return jsonify({"status": "started"})
    else:
        return jsonify({"status": "error", "message": "Arduino غير متصل"})


@app.route("/robot/stop", methods=["POST"])
def robot_stop():
    """إيقاف الروبوت."""
    global robot_running
    
    stop_robot()
    robot_running = False
    return jsonify({"status": "stopped", "message": "تم إيقاف الروبوت"})


@app.route("/robot/status", methods=["GET"])
def robot_status():
    """الحصول على حالة الروبوت."""
    status = get_robot_status()
    return jsonify({
        "running": robot_running, 
        "sensor": status,
        "arduino_connected": is_arduino_connected()
    })


# ========== API حالة النظام ==========
@app.route("/state")
def get_state():
    """Get current robot state with full details"""
    info = robot_state.get_info()
    info["can_verify"] = robot_state.can_verify()
    info["can_dispense"] = robot_state.can_dispense()
    return jsonify(info)

@app.route("/api/hardware/status")
def hw_status():
    """Get hardware health status"""
    return jsonify(get_hardware_status())

# ========== API أدوات النظام ==========

@app.route("/api/system/restart", methods=["POST"])
def system_restart():
    """تنظيف الكاش وإعادة تشغيل النظام."""
    def restart_sequence():
        time.sleep(1) # Wait for response to be sent
        print("🧹 Cleaning system...")
        
        # 1. Run cleanup script
        import subprocess
        import sys
        import os
        
        try:
            # Make sure script is executable (Linux only)
            if os.name != 'nt':
                subprocess.run(["chmod", "+x", "clean.sh"])
                subprocess.run(["./clean.sh"], shell=True)
            else:
                # Windows fallback (just print)
                print("   (Cleanup script skipped on Windows)")
                
        except Exception as e:
            print(f"⚠️ Cleanup error: {e}")

        # 2. Restart Application
        print("🔄 Restarting Flask Application...")
        stop_scheduler() # Stop threads first
        
        # Re-execute the current script
        os.execl(sys.executable, sys.executable, *sys.argv)

    # Run in thread to allow returning response first
    threading.Thread(target=restart_sequence).start()
    
    return jsonify({"status": "success", "message": "جاري تنظيف الكاش وإعادة التشغيل... انتظر 10 ثواني"})


if __name__ == "__main__":
    # تهيئة قاعدة البيانات
    init_database()
    
    # تهيئة GPIO على Raspberry Pi
    setup_gpio() # Safe to call even if HAS_GPIO is False (handled internally)
    
<<<<<<< HEAD
    # تأكيد اكتمال التهيئة
    robot_state.mark_initialized()
=======
    # ✅ العودة لوضع الصندوق 1 عند البدء (Home Position)
    try:
        go_home_zero()
        print("🏠 تم إرجاع الكاروسيل للصندوق 1 (وضع البداية)")
    except Exception as home_err:
        print(f"⚠️ خطأ في تحديد الوضع الابتدائي: {home_err}")
>>>>>>> 7bb6203313304bb920a8e7a4bc132c55be3998bf
    
    # تشغيل نظام الجدولة التلقائية
    start_scheduler()
    
    print("=" * 50)
    print("🤖 نظام توزيع الأدوية الذكي")
    print("=" * 50)
    print(f"GPIO متاح: {HAS_GPIO}")
    print(f"الجدولة التلقائية: {'✅ تعمل' if is_scheduler_running() else '❌ متوقفة'}")
    print(f"State Machine: {robot_state.current}")
    print("العنوان: http://0.0.0.0:5000")
    print("اضغط Ctrl+C للإيقاف")
    print("=" * 50)
    
    try:
        app.run(host="0.0.0.0", port=5000, debug=False)
    finally:
        stop_scheduler()

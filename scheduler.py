# -*- coding: utf-8 -*-
"""
نظام الجدولة التلقائية - Scheduler
يعمل في الخلفية ويفحص الجداول وينفذ الجرعات تلقائياً
مع دعم التنبيهات الصوتية
"""

import threading
import time
import os
from datetime import datetime, timedelta

# متغيرات الحالة
scheduler_thread = None
scheduler_running = False
last_dispensed = {1: None, 2: None}  # لمنع التكرار في نفس الدقيقة
pre_notified = {1: None, 2: None}    # لمنع تكرار التنبيه المسبق
missed_notified = {1: None, 2: None} # لمنع تكرار تنبيه الفوات

# تتبع حركة الروبوت (للتمييز بين الصرف التلقائي والطوارئ)
robot_moved_forward = False

# مسارات الأصوات
VOICES_DIR = os.path.join(os.path.dirname(__file__), 'voices')
SOUND_PRE_NOTIFY = os.path.join(VOICES_DIR, 'med_time01.mp3')   # قبل الموعد بـ 30 ثانية
SOUND_MISSED = os.path.join(VOICES_DIR, 'attentiion.mp3')       # عند فوات الموعد
SOUND_THANKS = os.path.join(VOICES_DIR, 'thanks.mp3')           # بعد أخذ الدواء
SOUND_EMERGENCY = os.path.join(VOICES_DIR, 'emergency.mp3')     # عند فتح الطوارئ
SOUND_CAMERA = os.path.join(VOICES_DIR, 'start_camera.mp3')     # قبل تشغيل الكاميرا


def play_sound(sound_path):
    """
    تشغيل ملف صوتي.
    يعمل على Raspberry Pi باستخدام mpg123 أو pygame.
    """
    if not os.path.exists(sound_path):
        print(f"⚠️ ملف الصوت غير موجود: {sound_path}")
        return False
    
    try:
        # محاولة استخدام pygame
        try:
            import pygame  # type: ignore
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
            print(f"🔊 تشغيل: {os.path.basename(sound_path)}")
            return True
        except ImportError:
            pass
        
        # محاولة استخدام mpg123 (متوفر على Pi)
        os.system(f'mpg123 -q "{sound_path}" &')
        print(f"🔊 تشغيل: {os.path.basename(sound_path)}")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل الصوت: {e}")
        return False


def check_and_dispense():
    """
    فحص الجداول وتنفيذ الجرعات إذا حان الموعد.
    تُستدعى كل 10 ثواني للتحقق من التنبيهات.
    يتحقق من State Machine قبل بدء أي عملية.
    """
    from database import get_all_schedules
    from database import log_dose
    from robot.state_machine import robot_state, RobotState
    
    try:
        # === فحص إذا كان النظام مشغول ===
        if robot_state.is_busy():
            return  # تخطي - النظام يعمل على عملية أخرى
        
        now = datetime.now()
        current_day = now.weekday()  # 0=Monday, 6=Sunday
        # تحويل لنظام JavaScript (0=Sunday)
        js_day = (current_day + 1) % 7
        current_hour = now.hour
        current_minute = now.minute
        current_second = now.second
        
        schedules = get_all_schedules()
        
        for box_id_str, schedule in schedules.items():
            box_id = int(box_id_str)
            
            if not schedule.get('enabled'):
                continue
                
            target_hour = schedule.get('hour')
            target_minute = schedule.get('minute')
            days = schedule.get('days', [])
            
            if target_hour is None:
                continue
            
            # تحقق إذا كان اليوم مطابقاً
            if js_day not in days:
                continue
            
            # إنشاء وقت الجرعة المستهدف
            target_time = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
            time_diff = (target_time - now).total_seconds()
            
            current_date_key = f"{now.date()}-{target_hour}-{target_minute}"
            
            # ====== 0. تشغيل الكاميرا (1 دقيقة قبل الموعد) ======
            if 55 <= time_diff <= 65:  # بين 55-65 ثانية
                camera_started_key = f"camera_{current_date_key}"
                if pre_notified.get(camera_started_key) != current_date_key:
                    # ✅ التحقق: هل نظام الكاميرا مفعّل؟
                    from database import get_setting
                    auth_enabled = str(get_setting("auth_enabled", "0")).strip() == "1"
                    
                    if auth_enabled:
                        print(f"📷 [{now.strftime('%H:%M:%S')}] تشغيل الكاميرا (قبل دقيقة) - النظام مفعّل")
                        try:
                            play_sound(SOUND_CAMERA)
                            from robot.camera.camera import camera
                            if camera and not camera.is_running():
                                camera.start()
                        except Exception as cam_err:
                            print(f"⚠️ خطأ في تشغيل الكاميرا: {cam_err}")
                    else:
                        print(f"📷 [{now.strftime('%H:%M:%S')}] تخطي تشغيل الكاميرا - النظام معطّل")
                    
                    pre_notified[camera_started_key] = current_date_key
            
            # ====== 1. التنبيه المسبق والحركة الذكية (30 ثانية قبل الموعد) ======
            if 25 <= time_diff <= 35:  # بين 25-35 ثانية
                if pre_notified.get(box_id) != current_date_key:
                    # فحص النظام قبل الحركة
                    if robot_state.is_busy():
                        print(f"⏳ النظام مشغول - تخطي التنبيه المسبق")
                        continue
                    
                    print(f"🔔 [{now.strftime('%H:%M:%S')}] تنبيه وحركة ذكية (قبل 30 ثانية)")
                    play_sound(SOUND_PRE_NOTIFY)
                    
                    # تغيير الحالة إلى MOVING
                    robot_state.set(RobotState.MOVING)
                    
                    # 🤖 الحركة الذكية للروبوت (مع كشف العقبات)
                    try:
                        from hardware import start_robot, stop_robot, get_latest_distance
                        global robot_moved_forward
                        
                        print("   🤖 بدء الحركة للأمام...")
                        if start_robot():
                            # ✅ تعيين العلم: الروبوت تحرك للأمام
                            robot_moved_forward = True
                            print(f"   ✅ تم تعيين robot_moved_forward = True")
                            
                            # الحركة لمدة أقصاها 5 ثواني
                            # لكن يتوقف فوراً لو اكتشف عقبة (سرير المريض)
                            OBSTACLE_THRESHOLD = 20  # سم - المسافة الآمنة
                            MAX_MOVE_TIME = 5  # ثواني
                            
                            for i in range(MAX_MOVE_TIME):
                                time.sleep(1)
                                distance = get_latest_distance()
                                
                                if distance is not None and distance < OBSTACLE_THRESHOLD:
                                    print(f"   🛑 اكتشاف عقبة على بعد {distance:.1f} سم - توقف!")
                                    print(f"   ✅ وصل الروبوت للسرير")
                                    break
                                elif distance is not None:
                                    print(f"   📏 المسافة: {distance:.1f} سم - استمرار...")
                            
                            stop_robot()
                            print(f"   ✓ توقف الروبوت (جاهز للصرف)")
                        else:
                            print(f"   ❌ فشل start_robot() - الروبوت لم يتحرك")
                            print(f"   ⚠️ robot_moved_forward يبقى = {robot_moved_forward}")
                    except Exception as move_err:
<<<<<<< HEAD
                        print(f"⚠️ فشل الحركة: {move_err}")
                    
                    # العودة لـ IDLE بعد الحركة
                    robot_state.force_idle("pre-notify movement done")

=======
                        print(f"⚠️ خطأ في الحركة: {move_err}")
                        print(f"   ⚠️ robot_moved_forward الحالي = {robot_moved_forward}")
                    
>>>>>>> 7bb6203313304bb920a8e7a4bc132c55be3998bf
                    pre_notified[box_id] = current_date_key
            
            # ====== 2. تحقق إذا حان الموعد (نفس الساعة والدقيقة) ======
            if current_hour == target_hour and current_minute == target_minute:
                # تحقق أننا لم نصرف هذه الجرعة في هذه الدقيقة
                last_time = last_dispensed.get(box_id)
                
                if last_time == current_date_key:
                    continue  # تم الصرف بالفعل
                
<<<<<<< HEAD
                # فحص النظام قبل الصرف
                if robot_state.is_busy():
                    print(f"⏳ النظام مشغول ({robot_state.current}) - تأجيل صرف الصندوق {box_id}")
                    continue
                
                # الحصول على قفل العملية
                op_id = robot_state.acquire_operation(timeout=5)
                if not op_id:
                    print(f"⚠️ فشل الحصول على قفل العملية - تخطي الصندوق {box_id}")
                    continue
=======
                # صرف الجرعة (بدون حركة روبوت - الحركة تمت في التنبيه المسبق)
                print(f"⏰ [{now.strftime('%H:%M:%S')}] حان موعد الصندوق {box_id}!")
                
                # استخدام التسلسل الكامل (الصرف فقط - الروبوت وصل بالفعل عند -30 ثانية)
                from hardware import full_dispense_sequence
                success, message = full_dispense_sequence(box_id)
>>>>>>> 7bb6203313304bb920a8e7a4bc132c55be3998bf
                
                try:
                    # صرف الجرعة
                    print(f"⏰ [{now.strftime('%H:%M:%S')}] حان موعد الصندوق {box_id}! [op:{op_id}]")
                    
                    # تغيير الحالة إلى DISPENSING
                    robot_state.set(RobotState.DISPENSING)
                    
                    # استخدام التسلسل الكامل
                    from hardware import full_dispense_sequence
                    success, message = full_dispense_sequence(box_id)
                    
                    if success:
                        last_dispensed[box_id] = current_date_key
                        log_dose(box_id, 'auto_dispensed', 'success',
                                 f'جرعة تلقائية [op:{op_id}] - {message}')
                        print(f"✅ تم صرف جرعة من الصندوق {box_id}")
                        
                        # تغيير الحالة إلى WAIT_CONFIRM
                        robot_state.set(RobotState.WAIT_CONFIRM)
                    else:
                        log_dose(box_id, 'auto_dispensed', 'failed', message)
                        print(f"❌ فشل صرف جرعة من الصندوق {box_id}: {message}")
                        # العودة لـ IDLE عند الفشل
                        robot_state.force_idle(f"dispense failed: {message}")
                
                except Exception as dispense_err:
                    print(f"❌ خطأ في عملية الصرف: {dispense_err}")
                    robot_state.force_idle(f"dispense error: {dispense_err}")
                finally:
                    # إطلاق قفل العملية (إلا إذا في WAIT_CONFIRM)
                    if robot_state.current != RobotState.WAIT_CONFIRM:
                        robot_state.release_operation()
                
                # ====== إيقاف الكاميرا بعد الصرف (لتوفير الموارد) ======
                try:
                    from database import get_setting
                    auth_enabled = str(get_setting("auth_enabled", "0")).strip() == "1"
                    
                    if auth_enabled:
                        from robot.camera.camera import camera
                        if camera and camera.is_running():
                            print(f"📷 [{now.strftime('%H:%M:%S')}] إيقاف الكاميرا بعد الصرف")
                            camera.stop()
                except Exception as cam_err:
                    print(f"⚠️ خطأ في إيقاف الكاميرا: {cam_err}")
            
            # ====== 3. تنبيه فوات الموعد (بعد 5 دقائق من الموعد بدون أخذ) ======
            if -300 <= time_diff < -280:  # بين 280-300 ثانية بعد الموعد
                if missed_notified.get(box_id) != current_date_key:
                    if last_dispensed.get(box_id) != current_date_key:
                        print(f"⚠️ [{now.strftime('%H:%M:%S')}] فات موعد الصندوق {box_id}!")
                        play_sound(SOUND_MISSED)
                        log_dose(box_id, 'missed', 'warning', 'فات موعد الجرعة بدون أخذها')
                    missed_notified[box_id] = current_date_key
                    
    except Exception as e:
        print(f"❌ خطأ في الجدولة: {e}")


def scheduler_loop():
    """
    الحلقة الرئيسية للجدولة.
    تعمل في thread منفصل.
    """
    global scheduler_running
    
    print("🔄 بدء تشغيل نظام الجدولة التلقائية...")
    
    while scheduler_running:
        try:
            check_and_dispense()
        except Exception as e:
            print(f"❌ خطأ في حلقة الجدولة: {e}")
        
        # انتظار 10 ثواني قبل الفحص التالي (لدقة التنبيهات)
        for _ in range(10):
            if not scheduler_running:
                break
            time.sleep(1)
    
    print("⏹️ تم إيقاف نظام الجدولة")


def start_scheduler():
    """بدء تشغيل نظام الجدولة."""
    global scheduler_thread, scheduler_running
    
    if scheduler_running:
        print("⚠️ نظام الجدولة يعمل بالفعل")
        return
    
    scheduler_running = True
    scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
    scheduler_thread.start()
    print("✅ تم تشغيل نظام الجدولة التلقائية")


def stop_scheduler():
    """إيقاف نظام الجدولة."""
    global scheduler_running
    
    scheduler_running = False
    print("⏹️ جاري إيقاف نظام الجدولة...")


def is_scheduler_running():
    """التحقق من حالة الجدولة."""
    return scheduler_running


def get_robot_moved_status():
    """الحصول على حالة حركة الروبوت."""
    return robot_moved_forward


def reset_robot_moved_status():
    """إعادة تعيين حالة حركة الروبوت."""
    global robot_moved_forward
    robot_moved_forward = False

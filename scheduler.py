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

# مسارات الأصوات
VOICES_DIR = os.path.join(os.path.dirname(__file__), 'voices')
SOUND_PRE_NOTIFY = os.path.join(VOICES_DIR, 'med_time01.mp3')   # قبل الموعد بـ 30 ثانية
SOUND_MISSED = os.path.join(VOICES_DIR, 'attentiion.mp3')       # عند فوات الموعد
SOUND_THANKS = os.path.join(VOICES_DIR, 'thanks.mp3')           # بعد أخذ الدواء
SOUND_EMERGENCY = os.path.join(VOICES_DIR, 'emergency.mp3')     # عند فتح الطوارئ


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
            import pygame
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
    """
    from database import get_all_schedules
    from hardware import dispense_dose
    from database import log_dose
    
    try:
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
            
            # ====== 1. التنبيه المسبق (30 ثانية قبل الموعد) ======
            if 25 <= time_diff <= 35:  # بين 25-35 ثانية قبل الموعد
                if pre_notified.get(box_id) != current_date_key:
                    print(f"🔔 [{now.strftime('%H:%M:%S')}] تنبيه مسبق للصندوق {box_id}!")
                    play_sound(SOUND_PRE_NOTIFY)
                    pre_notified[box_id] = current_date_key
            
            # ====== 2. تحقق إذا حان الموعد (نفس الساعة والدقيقة) ======
            if current_hour == target_hour and current_minute == target_minute:
                # تحقق أننا لم نصرف هذه الجرعة في هذه الدقيقة
                last_time = last_dispensed.get(box_id)
                
                if last_time == current_date_key:
                    continue  # تم الصرف بالفعل
                
                # صرف الجرعة مع حركة الروبوت الكاملة
                print(f"⏰ [{now.strftime('%H:%M:%S')}] حان موعد الصندوق {box_id}!")
                
                # استخدام التسلسل الكامل (مع حركة الروبوت)
                from hardware import full_dispense_sequence
                success, message = full_dispense_sequence(box_id)
                
                if success:
                    last_dispensed[box_id] = current_date_key
                    log_dose(box_id, 'auto_dispensed', 'success', f'جرعة تلقائية - {message}')
                    print(f"✅ تم صرف جرعة من الصندوق {box_id}")
                    # صوت الشكر سيعمل عند ضغط المريض على "تم أخذ الدواء"
                else:
                    log_dose(box_id, 'auto_dispensed', 'failed', message)
                    print(f"❌ فشل صرف جرعة من الصندوق {box_id}: {message}")
            
            # ====== 3. تنبيه فوات الموعد (بعد 5 دقائق من الموعد بدون أخذ) ======
            # إذا مر الموعد بـ 5 دقائق ولم يتم الصرف
            if -300 <= time_diff < -280:  # بين 280-300 ثانية بعد الموعد (حوالي 5 دقائق)
                if missed_notified.get(box_id) != current_date_key:
                    # تحقق إذا لم يتم الصرف
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

# -*- coding: utf-8 -*-
"""
نظام الجدولة التلقائية - Scheduler
يعمل في الخلفية ويفحص الجداول وينفذ الجرعات تلقائياً
"""

import threading
import time
from datetime import datetime

# متغيرات الحالة
scheduler_thread = None
scheduler_running = False
last_dispensed = {1: None, 2: None}  # لمنع التكرار في نفس الدقيقة


def check_and_dispense():
    """
    فحص الجداول وتنفيذ الجرعات إذا حان الموعد.
    تُستدعى كل 30 ثانية.
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
            
            # تحقق إذا حان الموعد (نفس الساعة والدقيقة)
            if current_hour == target_hour and current_minute == target_minute:
                # تحقق أننا لم نصرف هذه الجرعة في هذه الدقيقة
                last_time = last_dispensed.get(box_id)
                current_key = f"{now.date()}-{current_hour}-{current_minute}"
                
                if last_time == current_key:
                    continue  # تم الصرف بالفعل
                
                # صرف الجرعة
                print(f"⏰ [{now.strftime('%H:%M:%S')}] حان موعد الصندوق {box_id}!")
                
                success, message = dispense_dose(box_id)
                
                if success:
                    last_dispensed[box_id] = current_key
                    log_dose(box_id, 'auto_dispensed', 'success', f'جرعة تلقائية - {message}')
                    print(f"✅ تم صرف جرعة من الصندوق {box_id}")
                else:
                    log_dose(box_id, 'auto_dispensed', 'failed', message)
                    print(f"❌ فشل صرف جرعة من الصندوق {box_id}: {message}")
                    
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
        
        # انتظار 30 ثانية قبل الفحص التالي
        for _ in range(30):
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

# -*- coding: utf-8 -*-
"""
آلة الحالة - Robot State Machine
تتحكم في حالة الروبوت وتمنع تعارض العمليات

الحالات:
  IDLE → MOVING → VERIFYING → VERIFIED → DISPENSING → WAIT_CONFIRM → RETURNING → IDLE
                                                    ↘ ERROR → IDLE
"""

import threading
import time
import uuid


class RobotState:
    """جميع الحالات الممكنة للروبوت"""
    IDLE         = "IDLE"          # جاهز - لا شيء يحدث
    MOVING       = "MOVING"        # يتحرك نحو المريض
    VERIFYING    = "VERIFYING"     # يتحقق من الوجه
    VERIFIED     = "VERIFIED"      # تم التحقق - جاهز للصرف
    DISPENSING   = "DISPENSING"    # يصرف الدواء الآن
    WAIT_CONFIRM = "WAIT_CONFIRM"  # ينتظر تأكيد المريض
    RETURNING    = "RETURNING"     # يعود لنقطة البداية
    ERROR        = "ERROR"         # خطأ - يحتاج استرداد


# ============ خريطة الانتقالات الصالحة ============
# كل حالة → الحالات التي يمكن الانتقال إليها
VALID_TRANSITIONS = {
    RobotState.IDLE:         [RobotState.MOVING, RobotState.VERIFYING, RobotState.DISPENSING, RobotState.ERROR],
    RobotState.MOVING:       [RobotState.IDLE, RobotState.VERIFYING, RobotState.ERROR],
    RobotState.VERIFYING:    [RobotState.VERIFIED, RobotState.IDLE, RobotState.ERROR],
    RobotState.VERIFIED:     [RobotState.DISPENSING, RobotState.IDLE, RobotState.ERROR],
    RobotState.DISPENSING:   [RobotState.WAIT_CONFIRM, RobotState.IDLE, RobotState.ERROR],
    RobotState.WAIT_CONFIRM: [RobotState.RETURNING, RobotState.IDLE, RobotState.ERROR],
    RobotState.RETURNING:    [RobotState.IDLE, RobotState.ERROR],
    RobotState.ERROR:        [RobotState.IDLE],
}

# ============ مهلة زمنية لكل حالة (ثواني) ============
# إذا بقي النظام في حالة أطول من المهلة، يعود لـ IDLE تلقائياً
STATE_TIMEOUTS = {
    RobotState.IDLE:         0,     # لا مهلة
    RobotState.MOVING:       30,    # 30 ثانية للحركة
    RobotState.VERIFYING:    20,    # 20 ثانية للتحقق
    RobotState.VERIFIED:     60,    # 60 ثانية قبل انتهاء التحقق
    RobotState.DISPENSING:   30,    # 30 ثانية للصرف
    RobotState.WAIT_CONFIRM: 120,   # دقيقتين لتأكيد المريض
    RobotState.RETURNING:    30,    # 30 ثانية للعودة
    RobotState.ERROR:        60,    # دقيقة قبل الاسترداد التلقائي
}


class StateMachine:
    """آلة حالة آمنة للتعدد (Thread-Safe State Machine)"""

    def __init__(self):
        self._state = RobotState.IDLE
        self._lock = threading.Lock()
        self._operation_lock = threading.Lock()  # قفل العمليات - يمنع عمليتين متزامنتين
        self._state_time = time.time()           # وقت الدخول في الحالة الحالية
        self._error_code = None                  # كود الخطأ الحالي
        self._error_details = None               # تفاصيل الخطأ
        self._operation_id = None                # معرف العملية الحالية
        self._initialized = False                # هل تم تهيئة النظام
        self._history = []                       # تاريخ الانتقالات (آخر 50)
        self._MAX_HISTORY = 50

    # ========== الخصائص ==========

    @property
    def current(self):
        """الحالة الحالية مع فحص المهلة الزمنية"""
        with self._lock:
            self._check_timeout()
            return self._state

    @property
    def error_code(self):
        """كود الخطأ الحالي"""
        with self._lock:
            return self._error_code

    @property
    def error_details(self):
        """تفاصيل الخطأ"""
        with self._lock:
            return self._error_details

    @property
    def operation_id(self):
        """معرف العملية الحالية"""
        with self._lock:
            return self._operation_id

    @property
    def state_duration(self):
        """مدة البقاء في الحالة الحالية (ثواني)"""
        with self._lock:
            return time.time() - self._state_time

    # ========== انتقال الحالة ==========

    def set(self, new_state, error_code=None, error_details=None):
        """
        انتقال إلى حالة جديدة مع التحقق من صلاحية الانتقال.

        Args:
            new_state: الحالة الجديدة
            error_code: كود الخطأ (اختياري، للحالة ERROR)
            error_details: تفاصيل الخطأ (اختياري)

        Returns:
            True إذا نجح الانتقال، False إذا كان الانتقال غير صالح
        """
        with self._lock:
            old_state = self._state

            # التحقق من صلاحية الانتقال
            valid_targets = VALID_TRANSITIONS.get(old_state, [])
            if new_state not in valid_targets:
                print(f"⚠️ انتقال غير صالح: {old_state} → {new_state} "
                      f"(المسموح: {valid_targets})")
                return False

            # تنفيذ الانتقال
            self._state = new_state
            self._state_time = time.time()

            # معالجة حالة الخطأ
            if new_state == RobotState.ERROR:
                self._error_code = error_code or "UNKNOWN"
                self._error_details = error_details or ""
            elif new_state == RobotState.IDLE:
                self._error_code = None
                self._error_details = None
                self._operation_id = None

            # تسجيل في التاريخ
            self._history.append({
                "from": old_state,
                "to": new_state,
                "time": time.time(),
                "operation_id": self._operation_id,
                "error_code": error_code,
            })
            if len(self._history) > self._MAX_HISTORY:
                self._history = self._history[-self._MAX_HISTORY:]

            print(f"🔄 State: {old_state} → {new_state}"
                  + (f" [err={error_code}]" if error_code else ""))
            return True

    def force_idle(self, reason="forced"):
        """إعادة قسرية لـ IDLE (للطوارئ فقط)"""
        with self._lock:
            old = self._state
            self._state = RobotState.IDLE
            self._state_time = time.time()
            self._error_code = None
            self._error_details = None
            self._operation_id = None
            print(f"🔴 Force IDLE: {old} → IDLE (reason: {reason})")

    # ========== قفل العمليات ==========

    def acquire_operation(self, timeout=5):
        """
        الحصول على قفل العملية (يمنع عمليتين متزامنتين).

        Args:
            timeout: مهلة الانتظار بالثواني

        Returns:
            operation_id إذا نجح، None إذا فشل
        """
        acquired = self._operation_lock.acquire(timeout=timeout)
        if acquired:
            with self._lock:
                self._operation_id = str(uuid.uuid4())[:8]
                return self._operation_id
        else:
            print(f"⚠️ فشل الحصول على قفل العملية (timeout={timeout}s)")
            return None

    def release_operation(self):
        """إطلاق قفل العملية"""
        try:
            self._operation_lock.release()
        except RuntimeError:
            pass  # القفل لم يكن مأخوذاً

    # ========== فحوصات الحالة ==========

    def is_busy(self):
        """هل النظام مشغول بعملية حرجة"""
        return self.current in [
            RobotState.VERIFYING,
            RobotState.DISPENSING,
            RobotState.MOVING,
            RobotState.RETURNING,
        ]

    def can_verify(self):
        """هل يمكن بدء التحقق"""
        return self.current in [RobotState.IDLE, RobotState.VERIFIED, RobotState.MOVING]

    def can_dispense(self):
        """هل يمكن بدء الصرف (يجب أن يكون VERIFIED أو التحقق معطل)"""
        return self.current in [RobotState.VERIFIED, RobotState.IDLE]

    def mark_initialized(self):
        """تأكيد اكتمال تهيئة النظام"""
        self._initialized = True
        print("✅ State Machine initialized")

    @property
    def is_initialized(self):
        """هل تم تهيئة النظام"""
        return self._initialized

    # ========== معلومات الحالة ==========

    def get_info(self):
        """الحصول على معلومات شاملة عن الحالة"""
        with self._lock:
            self._check_timeout()
            timeout = STATE_TIMEOUTS.get(self._state, 0)
            elapsed = time.time() - self._state_time
            return {
                "state": self._state,
                "duration_s": round(elapsed, 1),
                "timeout_s": timeout,
                "remaining_s": round(max(0, timeout - elapsed), 1) if timeout > 0 else None,
                "is_busy": self._state in [RobotState.VERIFYING, RobotState.DISPENSING,
                                           RobotState.MOVING, RobotState.RETURNING],
                "operation_id": self._operation_id,
                "error_code": self._error_code,
                "error_details": self._error_details,
                "initialized": self._initialized,
            }

    def get_history(self, count=10):
        """الحصول على آخر N انتقالات"""
        with self._lock:
            return list(self._history[-count:])

    # ========== داخلي ==========

    def _check_timeout(self):
        """فحص المهلة الزمنية (يُستدعى داخل القفل فقط)"""
        timeout = STATE_TIMEOUTS.get(self._state, 0)
        if timeout > 0:
            elapsed = time.time() - self._state_time
            if elapsed > timeout:
                old = self._state
                # تسجيل الفوات إذا كان في انتظار التأكيد
                if old == RobotState.WAIT_CONFIRM:
                    print(f"⏰ Timeout: WAIT_CONFIRM ({elapsed:.0f}s) → "
                          f"تسجيل missed_dose")
                    try:
                        from database import log_dose
                        log_dose(0, 'missed_dose', 'warning',
                                 f'المريض لم يؤكد أخذ الدواء (timeout {elapsed:.0f}s)')
                    except Exception:
                        pass

                print(f"⏰ State Timeout: {old} ({elapsed:.0f}s > {timeout}s) → IDLE")
                self._state = RobotState.IDLE
                self._state_time = time.time()
                self._error_code = None
                self._error_details = None

                # إطلاق قفل العملية إذا كان مأخوذاً
                try:
                    self._operation_lock.release()
                except RuntimeError:
                    pass

                self._history.append({
                    "from": old,
                    "to": RobotState.IDLE,
                    "time": time.time(),
                    "operation_id": self._operation_id,
                    "error_code": "TIMEOUT",
                })


# ========== Singleton Instance ==========
robot_state = StateMachine()

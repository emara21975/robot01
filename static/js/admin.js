/**
 * لوحة التحكم - Admin JavaScript
 */

let timers = { 1: null, 2: null };
let timerCountdowns = { 1: 0, 2: 0 };
let selectedDays = { 1: [], 2: [] };
let schedules = {
    1: { hour: null, minute: null, enabled: false },
    2: { hour: null, minute: null, enabled: false }
};

function toggleDay(boxId, dayIndex) {
    const btn = document.getElementById(`box${boxId}-day-${dayIndex}`);
    const index = selectedDays[boxId].indexOf(dayIndex);

    if (index > -1) {
        selectedDays[boxId].splice(index, 1);
        btn.classList.remove('active');
    } else {
        selectedDays[boxId].push(dayIndex);
        btn.classList.add('active');
    }
}

function setTimer(boxId) {
    const hours = parseInt(document.getElementById(`box${boxId}-hours`).value);
    const minutes = parseInt(document.getElementById(`box${boxId}-minutes`).value) || 0;

    if (isNaN(hours) || hours < 0 || hours > 23 || minutes < 0 || minutes > 59) {
        document.getElementById('result').innerText = `✗ يرجى إدخال وقت صحيح للصندوق ${boxId}`;
        return;
    }

    if (selectedDays[boxId].length === 0) {
        document.getElementById('result').innerText = `✗ يرجى اختيار يوم واحد على الأقل للصندوق ${boxId}`;
        return;
    }

    if (timers[boxId]) {
        clearInterval(timers[boxId]);
    }

    schedules[boxId] = { hour: hours, minute: minutes, enabled: true };
    calculateNextSchedule(boxId);
    document.getElementById(`timer-display-${boxId}`).classList.add('active');

    const daysText = selectedDays[boxId].map(d => ['الأحد', 'الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت'][d]).join('، ');
    document.getElementById('result').innerText = `✓ تم تفعيل الجدولة للصندوق ${boxId} - الموعد: ${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')} في أيام: ${daysText}`;

    // إضافة اسم الدواء
    const medicineName = document.getElementById(`box${boxId}-name`).value;

    fetch('/api/schedules', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            box: boxId,
            hour: hours,
            minute: minutes,
            enabled: true,
            days: selectedDays[boxId],
            medicine_name: medicineName
        })
    });

    timers[boxId] = setInterval(() => {
        if (timerCountdowns[boxId] > 0) {
            timerCountdowns[boxId]--;
            updateTimerDisplay(boxId);

            if (timerCountdowns[boxId] <= 0) {
                openBox(boxId);
                document.getElementById('result').innerText = `✓ حان موعد الدواء - تم فتح الصندوق ${boxId} تلقائياً!`;
                setTimeout(() => calculateNextSchedule(boxId), 2000);
            }
        }
    }, 1000);
}

function calculateNextSchedule(boxId) {
    if (!schedules[boxId].enabled) return;

    const now = new Date();
    const currentDay = now.getDay();
    const currentHour = now.getHours();
    const currentMinute = now.getMinutes();
    const targetHour = schedules[boxId].hour;
    const targetMinute = schedules[boxId].minute;

    let nextDate = new Date();
    let daysToAdd = 0;
    const sortedDays = [...selectedDays[boxId]].sort((a, b) => a - b);
    let found = false;

    if (sortedDays.includes(currentDay)) {
        const targetTime = targetHour * 60 + targetMinute;
        const currentTime = currentHour * 60 + currentMinute;
        if (targetTime > currentTime) {
            found = true;
        }
    }

    if (!found) {
        for (let i = 1; i <= 7; i++) {
            const checkDay = (currentDay + i) % 7;
            if (sortedDays.includes(checkDay)) {
                daysToAdd = i;
                found = true;
                break;
            }
        }
    }

    nextDate.setDate(nextDate.getDate() + daysToAdd);
    nextDate.setHours(targetHour);
    nextDate.setMinutes(targetMinute);
    nextDate.setSeconds(0);
    nextDate.setMilliseconds(0);

    const diff = Math.floor((nextDate - now) / 1000);
    timerCountdowns[boxId] = diff > 0 ? diff : 0;
    updateTimerDisplay(boxId);
}

function updateTimerDisplay(boxId) {
    const totalSeconds = timerCountdowns[boxId];
    const days = Math.floor(totalSeconds / 86400);
    const h = Math.floor((totalSeconds % 86400) / 3600);
    const m = Math.floor((totalSeconds % 3600) / 60);
    const s = totalSeconds % 60;

    let displayText = '';
    if (days > 0) {
        displayText = `${days} يوم، ${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    } else {
        displayText = `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    }

    document.getElementById(`timer-countdown-${boxId}`).innerText = displayText;
}

async function openBox(boxId) {
    document.getElementById('status').className = 'status-indicator status-working';
    document.getElementById('status').innerHTML = '<span class="status-dot"></span><span>جاري فتح الصندوق...</span>';
    document.getElementById('result').innerText = `جاري فتح الصندوق ${boxId}...`;

    try {
        const response = await fetch('/open_box', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ box: boxId })
        });

        const data = await response.json();
        document.getElementById('result').innerText = data.status;
        document.getElementById('status').className = 'status-indicator status-ready';
        document.getElementById('status').innerHTML = '<span class="status-dot"></span><span>جاهز للعمل</span>';
    } catch (error) {
        document.getElementById('result').innerText = `✗ فشل في فتح الصندوق ${boxId}`;
        document.getElementById('status').className = 'status-indicator status-error';
        document.getElementById('status').innerHTML = '<span class="status-dot"></span><span>خطأ في النظام</span>';
    }
}

async function loadMode() {
    document.getElementById('status').className = 'status-indicator status-working';
    document.getElementById('status').innerHTML = '<span class="status-dot"></span><span>جاري التحضير...</span>';
    document.getElementById('result').innerText = 'جاري تدوير العلبة لوضع إدخال الدواء...';

    try {
        const response = await fetch('/load_mode', { method: 'POST' });
        const data = await response.json();

        document.getElementById('result').innerText = data.status;
        document.getElementById('status').className = 'status-indicator status-ready';
        document.getElementById('status').innerHTML = '<span class="status-dot"></span><span>جاهز للعمل</span>';
    } catch (error) {
        document.getElementById('result').innerText = '✗ حدث خطأ في وضع التحميل';
        document.getElementById('status').className = 'status-indicator status-error';
        document.getElementById('status').innerHTML = '<span class="status-dot"></span><span>خطأ في النظام</span>';
    }
}

async function goZero() {
    document.getElementById('status').className = 'status-indicator status-working';
    document.getElementById('status').innerHTML = '<span class="status-dot"></span><span>جاري الرجوع...</span>';
    document.getElementById('result').innerText = 'جاري الرجوع إلى نقطة الصفر...';

    try {
        const response = await fetch('/go_zero', { method: 'POST' });
        const data = await response.json();

        document.getElementById('result').innerText = data.status;
        document.getElementById('status').className = 'status-indicator status-ready';
        document.getElementById('status').innerHTML = '<span class="status-dot"></span><span>جاهز للعمل</span>';
    } catch (error) {
        document.getElementById('result').innerText = '✗ حدث خطأ في العودة للصفر';
        document.getElementById('status').className = 'status-indicator status-error';
        document.getElementById('status').innerHTML = '<span class="status-dot"></span><span>خطأ في النظام</span>';
    }
}

function updateTime() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');

    document.getElementById('hours').innerText = hours;
    document.getElementById('minutes').innerText = minutes;
    document.getElementById('seconds').innerText = seconds;
}

// التحكم في الروبوت
let robotRunning = false;

async function startRobot() {
    const btn = document.getElementById('robotBtn');

    if (!robotRunning) {
        try {
            const response = await fetch('/robot/start', { method: 'POST' });
            const data = await response.json();

            if (data.status === 'started') {
                robotRunning = true;
                btn.classList.add('running');
                btn.innerHTML = `
          <svg class="icon-svg" style="width: 20px; height: 20px;" viewBox="0 0 24 24" fill="currentColor">
            <rect x="6" y="4" width="4" height="16"/>
            <rect x="14" y="4" width="4" height="16"/>
          </svg>
          <span>إيقاف الحركة</span>
        `;
                document.getElementById('result').innerText = '✓ الروبوت يتحرك - سيتوقف عند اكتشاف عائق';
                document.getElementById('status').className = 'status-indicator status-working';
                document.getElementById('status').innerHTML = '<span class="status-dot"></span><span>الروبوت يعمل</span>';
            }
        } catch (error) {
            document.getElementById('result').innerText = '✗ خطأ في الاتصال بالروبوت';
        }
    } else {
        try {
            const response = await fetch('/robot/stop', { method: 'POST' });
            const data = await response.json();

            if (data.status === 'stopped') {
                robotRunning = false;
                btn.classList.remove('running');
                btn.innerHTML = `
          <svg class="icon-svg" style="width: 20px; height: 20px;" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zM4 7v2h16V7H4zm8 3c-1.1 0-2 .9-2 2v8h4v-8c0-1.1-.9-2-2-2zm-6 0c-1.1 0-2 .9-2 2v8h4v-8c0-1.1-.9-2-2-2zm12 0c-1.1 0-2 .9-2 2v8h4v-8c0-1.1-.9-2-2-2z"/>
          </svg>
          <span>تحريك الروبوت</span>
        `;
                document.getElementById('result').innerText = data.message || '✓ تم إيقاف الروبوت';
                document.getElementById('status').className = 'status-indicator status-ready';
                document.getElementById('status').innerHTML = '<span class="status-dot"></span><span>جاهز للعمل</span>';
            }
        } catch (error) {
            document.getElementById('result').innerText = '✗ خطأ في إيقاف الروبوت';
        }
    }
}

// تحميل الجداول المحفوظة من السيرفر
async function loadSchedules() {
    try {
        const response = await fetch('/api/schedules');
        const data = await response.json();

        for (let boxId in data) {
            if (data[boxId].enabled && data[boxId].hour !== null) {
                // تحديث الحقول
                document.getElementById(`box${boxId}-hours`).value = data[boxId].hour;
                document.getElementById(`box${boxId}-minutes`).value = data[boxId].minute || 0;

                // تحديث الأيام المحددة
                selectedDays[boxId] = data[boxId].days || [];
                selectedDays[boxId].forEach(dayIndex => {
                    const btn = document.getElementById(`box${boxId}-day-${dayIndex}`);
                    if (btn) btn.classList.add('active');
                });

                // تحديث اسم الدواء
                if (data[boxId].medicine_name) {
                    document.getElementById(`box${boxId}-name`).value = data[boxId].medicine_name;
                }

                // تحديث الجدولة
                schedules[boxId] = {
                    hour: data[boxId].hour,
                    minute: data[boxId].minute,
                    enabled: true
                };

                // بدء العد التنازلي
                calculateNextSchedule(boxId);
                document.getElementById(`timer-display-${boxId}`).classList.add('active');

                // بدء المؤقت
                if (timers[boxId]) {
                    clearInterval(timers[boxId]);
                }

                timers[boxId] = setInterval(() => {
                    if (timerCountdowns[boxId] > 0) {
                        timerCountdowns[boxId]--;
                        updateTimerDisplay(boxId);

                        if (timerCountdowns[boxId] <= 0) {
                            openBox(boxId);
                            document.getElementById('result').innerText = `✓ حان موعد الدواء - تم فتح الصندوق ${boxId} تلقائياً!`;
                            setTimeout(() => calculateNextSchedule(boxId), 2000);
                        }
                    }
                }, 1000);
            }
        }
    } catch (error) {
        console.error('Error loading schedules:', error);
    }
}

window.onload = function () {
    updateTime();
    setInterval(updateTime, 1000);
    loadSchedules();
};

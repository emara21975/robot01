/**
 * شاشة المريض - Patient JavaScript
 */

let schedules = {
    1: { hour: null, minute: null, enabled: false, name: 'الدواء الأول', icon: '<svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor"><path d="M4.22 11.29l6.36-6.36c1.95-1.95 5.12-1.95 7.07 0 1.95 1.95 1.95 5.12 0 7.07l-6.36 6.36c-1.95 1.95-5.12 1.95-7.07 0-1.95-1.95-1.95-5.12 0-7.07z"/><path d="M15 9l-6 6" stroke="white" stroke-width="1.5"/></svg>', color: 'blue' },
    2: { hour: null, minute: null, enabled: false, name: 'الدواء الثاني', icon: '<svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor"><path d="M4.22 11.29l6.36-6.36c1.95-1.95 5.12-1.95 7.07 0 1.95 1.95 1.95 5.12 0 7.07l-6.36 6.36c-1.95 1.95-5.12 1.95-7.07 0-1.95-1.95-1.95-5.12 0-7.07z"/><path d="M15 9l-6 6" stroke="white" stroke-width="1.5"/></svg>', color: 'green' }
};

let selectedDays = { 1: [], 2: [] };
let audioPlayed = { 1: false, 2: false };

// جلب الجداول من السيرفر
async function fetchSchedules() {
    try {
        const response = await fetch('/api/schedules');
        const data = await response.json();

        for (let boxId in data) {
            if (data[boxId]) {
                schedules[boxId] = {
                    ...schedules[boxId],
                    hour: data[boxId].hour,
                    minute: data[boxId].minute,
                    enabled: data[boxId].enabled,
                    name: data[boxId].medicine_name || schedules[boxId].name
                };
                selectedDays[boxId] = data[boxId].days || [];
            }
        }

        renderMedicationCards();
    } catch (error) {
        console.error('Error fetching schedules:', error);
        document.getElementById('no-schedule').style.display = 'block';
        document.getElementById('medicines-container').innerHTML = '';
    }
}

function renderMedicationCards() {
    const container = document.getElementById('medicines-container');
    const noSchedule = document.getElementById('no-schedule');

    let hasActiveSchedules = false;
    let cardsHTML = '';

    for (let boxId in schedules) {
        if (schedules[boxId].enabled && schedules[boxId].hour !== null) {
            hasActiveSchedules = true;

            const colorClass = boxId == 1 ? 'medication-1' : 'medication-2';

            cardsHTML += `
        <div class="medication-card ${colorClass}" id="card-${boxId}">
          <div class="card-header">
            <div>
              <div class="medication-name">${schedules[boxId].name}</div>
            </div>
            <div class="medication-icon">${schedules[boxId].icon}</div>
          </div>
          <div class="card-content">
            <div class="time-display">
              <span class="time-label">موعد الجرعة</span>
              <span class="current-time">${String(schedules[boxId].hour).padStart(2, '0')}:${String(schedules[boxId].minute).padStart(2, '0')}</span>
            </div>
            <div class="next-dose">
              <h3>
                <svg viewBox="0 0 24 24"><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/></svg>
                الوقت المتبقي
              </h3>
              <p class="next-dose-time" id="time-remaining-${boxId}">جاري الحساب...</p>
              <p class="dose-description" id="days-desc-${boxId}"></p>
            </div>
          </div>
        </div>
      `;
        }
    }

    if (hasActiveSchedules) {
        container.innerHTML = cardsHTML;
        noSchedule.style.display = 'none';
    } else {
        container.innerHTML = '';
        noSchedule.style.display = 'block';
    }
}

// صوت التنبيه المحسّن - نغمة قوية ومتكررة
function playWarningSound() {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();

    function playTone(frequency, startTime, duration, volume) {
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        oscillator.frequency.value = frequency;
        oscillator.type = 'square';

        gainNode.gain.setValueAtTime(volume, startTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + duration);

        oscillator.start(startTime);
        oscillator.stop(startTime + duration);
    }

    const now = audioContext.currentTime;

    playTone(600, now, 0.15, 0.5);
    playTone(800, now + 0.2, 0.15, 0.5);
    playTone(1000, now + 0.4, 0.15, 0.6);
    playTone(800, now + 0.6, 0.15, 0.5);
    playTone(1000, now + 0.8, 0.3, 0.7);

    setTimeout(() => {
        const ctx2 = new (window.AudioContext || window.webkitAudioContext)();
        const now2 = ctx2.currentTime;

        function playTone2(freq, start, dur, vol) {
            const osc = ctx2.createOscillator();
            const gain = ctx2.createGain();
            osc.connect(gain);
            gain.connect(ctx2.destination);
            osc.frequency.value = freq;
            osc.type = 'square';
            gain.gain.setValueAtTime(vol, start);
            gain.gain.exponentialRampToValueAtTime(0.01, start + dur);
            osc.start(start);
            osc.stop(start + dur);
        }

        playTone2(600, now2, 0.15, 0.5);
        playTone2(800, now2 + 0.2, 0.15, 0.5);
        playTone2(1000, now2 + 0.4, 0.15, 0.6);
        playTone2(800, now2 + 0.6, 0.15, 0.5);
        playTone2(1000, now2 + 0.8, 0.3, 0.7);
    }, 1500);
}

// حساب الوقت المتبقي
function calculateTimeRemaining(boxId) {
    if (!schedules[boxId].enabled) return null;

    const now = new Date();
    const currentDay = now.getDay();

    // التحقق من أن اليوم الحالي من الأيام المختارة
    if (!selectedDays[boxId].includes(currentDay)) {
        // البحث عن اليوم التالي
        for (let i = 1; i <= 7; i++) {
            const checkDay = (currentDay + i) % 7;
            if (selectedDays[boxId].includes(checkDay)) {
                const nextDate = new Date();
                nextDate.setDate(nextDate.getDate() + i);
                nextDate.setHours(schedules[boxId].hour);
                nextDate.setMinutes(schedules[boxId].minute);
                nextDate.setSeconds(0);
                return Math.floor((nextDate - now) / 1000);
            }
        }
        return null;
    }

    // حساب الموعد اليوم
    const targetTime = new Date();
    targetTime.setHours(schedules[boxId].hour);
    targetTime.setMinutes(schedules[boxId].minute);
    targetTime.setSeconds(0);

    let diff = Math.floor((targetTime - now) / 1000);

    // إذا فات الموعد اليوم، احسب للموعد التالي
    if (diff < 0) {
        for (let i = 1; i <= 7; i++) {
            const checkDay = (currentDay + i) % 7;
            if (selectedDays[boxId].includes(checkDay)) {
                const nextDate = new Date();
                nextDate.setDate(nextDate.getDate() + i);
                nextDate.setHours(schedules[boxId].hour);
                nextDate.setMinutes(schedules[boxId].minute);
                nextDate.setSeconds(0);
                return Math.floor((nextDate - now) / 1000);
            }
        }
    }

    return diff;
}

function formatTimeRemaining(seconds) {
    if (seconds === null || seconds < 0) return 'انتظر...';

    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    if (days > 0) {
        return `${days} يوم ${String(hours).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }
    return `${String(hours).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

function updateTimeDisplay() {
    for (let boxId in schedules) {
        if (schedules[boxId].enabled && schedules[boxId].hour !== null) {
            const remaining = calculateTimeRemaining(boxId);
            const el = document.getElementById(`time-remaining-${boxId}`);
            const card = document.getElementById(`card-${boxId}`);

            if (el) {
                el.innerText = formatTimeRemaining(remaining);

                // تنسيق حسب الوقت المتبقي
                el.classList.remove('warning', 'danger');
                if (card) card.classList.remove('urgent');

                if (remaining <= 300 && remaining > 0) { // أقل من 5 دقائق
                    el.classList.add('danger');
                    if (card) card.classList.add('urgent');

                    if (!audioPlayed[boxId]) {
                        playWarningSound();
                        audioPlayed[boxId] = true;
                    }
                } else if (remaining <= 900 && remaining > 0) { // أقل من 15 دقيقة
                    el.classList.add('warning');
                } else {
                    audioPlayed[boxId] = false;
                }

                // عرض الأيام
                const daysEl = document.getElementById(`days-desc-${boxId}`);
                if (daysEl && selectedDays[boxId].length > 0) {
                    const dayNames = ['الأحد', 'الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت'];
                    const daysText = selectedDays[boxId].map(d => dayNames[d]).join(' • ');
                    daysEl.innerText = `الأيام: ${daysText}`;
                }
            }
        }
    }
}

// التهيئة
window.onload = function () {
    fetchSchedules();
    setInterval(updateTimeDisplay, 1000);
    setInterval(fetchSchedules, 30000); // تحديث كل 30 ثانية
};

function verifyFace() {
    const statusDiv = document.getElementById("face-status");
    if (statusDiv) statusDiv.innerHTML = "⏳ جاري التحقق...";

    fetch("/verify-face")
        .then(res => res.json())
        .then(data => {
            if (statusDiv) {
                if (data.verified) {
                    statusDiv.innerHTML = `<span style="color: var(--success)">✅ ${data.message || "تم التحقق"}</span>`;
                } else {
                    statusDiv.innerHTML = `<span style="color: var(--danger)">❌ ${data.message || "غير مصرح"}</span>`;
                }
            } else {
                alert(data.verified ? "✅ تم التحقق" : "❌ غير مصرح");
            }
        })
        .catch(err => {
            console.error(err);
            if (statusDiv) statusDiv.innerHTML = `<span style="color: var(--danger)">❌ خطأ في الاتصال</span>`;
            else alert("❌ خطأ في الاتصال");
        });
}

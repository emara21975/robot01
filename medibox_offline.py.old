# صفحة الإدارة - بدون إنترنت
HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>لوحة تحكم الروبوت الذكي لتوزيع الأدوية</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
      min-height: 100vh;
      padding: 20px;
    }
    
    .container {
      max-width: 1200px;
      margin: 0 auto;
    }
    
    .dashboard-card {
      background: white;
      border-radius: 20px;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
      padding: 40px;
    }
    
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 40px;
      flex-wrap: wrap;
      gap: 20px;
    }
    
    .header-title {
      display: flex;
      align-items: center;
      gap: 20px;
    }
    
    .robot-icon {
      background: #dbeafe;
      width: 80px;
      height: 80px;
      border-radius: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 40px;
    }
    
    h1 {
      font-size: 2em;
      color: #1f2937;
      font-weight: 700;
    }
    
    .subtitle {
      color: #6b7280;
      margin-top: 5px;
    }
    
    .time-status {
      background: #dbeafe;
      border-radius: 20px;
      padding: 20px;
      display: flex;
      align-items: center;
      gap: 20px;
      flex-wrap: wrap;
    }
    
    .time-display {
      display: flex;
      gap: 15px;
    }
    
    .time-box {
      text-align: center;
    }
    
    .time-label {
      font-size: 0.8em;
      color: #6b7280;
      display: block;
      margin-bottom: 5px;
    }
    
    .time-value {
      background: white;
      padding: 10px 15px;
      border-radius: 10px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      color: #1e40af;
      font-weight: 700;
      font-size: 1.2em;
    }
    
    .status-indicator {
      display: flex;
      align-items: center;
      padding: 10px 20px;
      border-radius: 20px;
      font-weight: 600;
      gap: 10px;
    }
    
    .status-ready {
      background: rgba(72, 187, 120, 0.15);
      color: #22543d;
    }
    
    .status-working {
      background: rgba(237, 137, 54, 0.15);
      color: #7b341e;
    }
    
    .status-error {
      background: rgba(245, 101, 101, 0.15);
      color: #742a2a;
    }
    
    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: currentColor;
    }
    
    .btn {
      padding: 12px 24px;
      border: none;
      border-radius: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s;
      font-size: 1em;
      display: inline-flex;
      align-items: center;
      gap: 10px;
      text-decoration: none;
    }
    
    .btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    .btn-green {
      background: #10b981;
      color: white;
    }
    
    .btn-blue {
      background: #3b82f6;
      color: white;
    }
    
    .btn-cyan {
      background: #06b6d4;
      color: white;
    }
    
    .btn-purple {
      background: #8b5cf6;
      color: white;
    }
    
    .btn-orange {
      background: #f97316;
      color: white;
    }
    
    .section-title {
      font-size: 1.8em;
      font-weight: 700;
      text-align: center;
      margin-bottom: 30px;
      color: #1f2937;
    }
    
    .medicine-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 30px;
      margin-bottom: 40px;
    }
    
    .medicine-box {
      background: white;
      border-radius: 16px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.1);
      overflow: hidden;
      border: 1px solid #e5e7eb;
      transition: all 0.3s;
    }
    
    .medicine-box:hover {
      transform: translateY(-5px);
      box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .box-lid {
      height: 20px;
      background: linear-gradient(to bottom, #e5e7eb, #d1d5db);
      border-bottom: 2px solid #9ca3af;
    }
    
    .box-content {
      padding: 30px 20px;
      text-align: center;
    }
    
    .box-number {
      position: absolute;
      top: 30px;
      left: 20px;
      background: rgba(255,255,255,0.9);
      width: 35px;
      height: 35px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .box-icon {
      font-size: 3em;
      margin-bottom: 15px;
    }
    
    .medicine-name {
      font-weight: 600;
      color: #374151;
      margin-bottom: 15px;
      font-size: 1.1em;
    }
    
    .schedule-controls {
      background: #f9fafb;
      border-radius: 15px;
      padding: 20px;
      margin-top: 20px;
    }
    
    .schedule-label {
      display: block;
      text-align: center;
      margin-bottom: 15px;
      font-weight: 600;
      color: #374151;
      font-size: 0.9em;
    }
    
    .days-selector {
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
      justify-content: center;
      margin-bottom: 15px;
    }
    
    .day-btn {
      padding: 8px 12px;
      font-size: 0.85em;
      background: #e5e7eb;
      border: 1px solid #d1d5db;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
    }
    
    .day-btn:hover {
      background: #3b82f6;
      color: white;
      border-color: #3b82f6;
    }
    
    .day-btn.active {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border-color: #667eea;
    }
    
    .time-input-group {
      display: flex;
      gap: 10px;
      justify-content: center;
      align-items: center;
      margin-bottom: 15px;
    }
    
    .time-input-field {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 5px;
    }
    
    .time-input-field input {
      width: 60px;
      padding: 8px;
      text-align: center;
      border: 2px solid #e5e7eb;
      border-radius: 8px;
      font-weight: 700;
      font-size: 1em;
    }
    
    .time-input-field label {
      font-size: 0.8em;
      color: #6b7280;
    }
    
    .timer-display {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border-radius: 10px;
      padding: 15px;
      margin-top: 15px;
      font-weight: 700;
      display: none;
      text-align: center;
      box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
    }
    
    .timer-display.active {
      display: block;
    }
    
    .maintenance-section {
      margin-bottom: 30px;
    }
    
    .maintenance-buttons {
      display: flex;
      justify-content: center;
      gap: 20px;
      flex-wrap: wrap;
      margin-bottom: 15px;
    }
    
    .maintenance-note {
      text-align: center;
      color: #6b7280;
      font-size: 0.9em;
    }
    
    .result-box {
      background: #f9fafb;
      border-radius: 20px;
      padding: 25px;
      border: 1px solid #e5e7eb;
    }
    
    .result-title {
      font-weight: 600;
      color: #374151;
      margin-bottom: 10px;
      font-size: 1.1em;
    }
    
    .result-text {
      color: #6b7280;
    }
    
    input[type="number"] {
      -moz-appearance: textfield;
    }
    
    input[type="number"]::-webkit-inner-spin-button,
    input[type="number"]::-webkit-outer-spin-button {
      -webkit-appearance: none;
      margin: 0;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="dashboard-card">
      <!-- رأس الصفحة -->
      <div class="header">
        <div class="header-title">
          <div class="robot-icon">🤖</div>
          <div>
            <h1>الروبوت الذكي لتوزيع الأدوية</h1>
            <p class="subtitle">نظام إدارة الأدوية الآلي المتكامل</p>
          </div>
        </div>
        
        <a href="/patient" class="btn btn-green">
          <span>👤</span>
          <span>شاشة المريض</span>
        </a>
      </div>
      
      <div class="time-status">
        <div>
          <p style="color: #6b7280; font-size: 0.9em; margin-bottom: 10px;">الوقت الحالي</p>
          <div class="time-display">
            <div class="time-box">
              <span class="time-label">ساعة</span>
              <div class="time-value" id="hours">00</div>
            </div>
            <div class="time-box">
              <span class="time-label">دقيقة</span>
              <div class="time-value" id="minutes">00</div>
            </div>
            <div class="time-box">
              <span class="time-label">ثانية</span>
              <div class="time-value" id="seconds">00</div>
            </div>
          </div>
        </div>
        <div class="status-indicator status-ready" id="status">
          <span class="status-dot"></span>
          <span>جاهز للعمل</span>
        </div>
      </div>
      
      <!-- صناديق الأدوية -->
      <div style="margin-top: 40px;">
        <h2 class="section-title">صناديق الأدوية</h2>
        <div class="medicine-grid">
          <!-- الصندوق 1 -->
          <div class="medicine-box" style="position: relative;">
            <div class="box-lid"></div>
            <div class="box-content">
              <div class="box-number">1</div>
              <div class="box-icon" style="color: #3b82f6;">💊</div>
              <div class="medicine-name">أدوية القلب</div>
              <button onclick="openBox(1)" class="btn btn-blue" style="width: 100%;">فتح الآن</button>
              
              <div class="schedule-controls">
                <label class="schedule-label">ضبط موعد الدواء</label>
                
                <div style="margin-bottom: 15px;">
                  <label style="display: block; text-align: center; font-size: 0.8em; color: #6b7280; margin-bottom: 10px;">أيام الأسبوع:</label>
                  <div class="days-selector">
                    <button type="button" onclick="toggleDay(1, 0)" id="box1-day-0" class="day-btn">الأحد</button>
                    <button type="button" onclick="toggleDay(1, 1)" id="box1-day-1" class="day-btn">الإثنين</button>
                    <button type="button" onclick="toggleDay(1, 2)" id="box1-day-2" class="day-btn">الثلاثاء</button>
                    <button type="button" onclick="toggleDay(1, 3)" id="box1-day-3" class="day-btn">الأربعاء</button>
                    <button type="button" onclick="toggleDay(1, 4)" id="box1-day-4" class="day-btn">الخميس</button>
                    <button type="button" onclick="toggleDay(1, 5)" id="box1-day-5" class="day-btn">الجمعة</button>
                    <button type="button" onclick="toggleDay(1, 6)" id="box1-day-6" class="day-btn">السبت</button>
                  </div>
                </div>
                
                <div class="time-input-group">
                  <div class="time-input-field">
                    <input type="number" id="box1-hours" min="0" max="23" value="12">
                    <label>ساعة</label>
                  </div>
                  <span style="font-size: 1.5em; color: #9ca3af;">:</span>
                  <div class="time-input-field">
                    <input type="number" id="box1-minutes" min="0" max="59" value="0">
                    <label>دقيقة</label>
                  </div>
                </div>
                
                <button onclick="setTimer(1)" class="btn btn-orange" style="width: 100%;">تفعيل الجدولة</button>
                <div id="timer-display-1" class="timer-display">
                  الفتح التلقائي في: <span id="timer-countdown-1">00:00:00</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- الصندوق 2 -->
          <div class="medicine-box" style="position: relative;">
            <div class="box-lid"></div>
            <div class="box-content">
              <div class="box-number">2</div>
              <div class="box-icon" style="color: #10b981;">💊</div>
              <div class="medicine-name">المضادات الحيوية</div>
              <button onclick="openBox(2)" class="btn btn-green" style="width: 100%; background: #10b981;">فتح الآن</button>
              
              <div class="schedule-controls">
                <label class="schedule-label">ضبط موعد الدواء</label>
                
                <div style="margin-bottom: 15px;">
                  <label style="display: block; text-align: center; font-size: 0.8em; color: #6b7280; margin-bottom: 10px;">أيام الأسبوع:</label>
                  <div class="days-selector">
                    <button type="button" onclick="toggleDay(2, 0)" id="box2-day-0" class="day-btn">الأحد</button>
                    <button type="button" onclick="toggleDay(2, 1)" id="box2-day-1" class="day-btn">الإثنين</button>
                    <button type="button" onclick="toggleDay(2, 2)" id="box2-day-2" class="day-btn">الثلاثاء</button>
                    <button type="button" onclick="toggleDay(2, 3)" id="box2-day-3" class="day-btn">الأربعاء</button>
                    <button type="button" onclick="toggleDay(2, 4)" id="box2-day-4" class="day-btn">الخميس</button>
                    <button type="button" onclick="toggleDay(2, 5)" id="box2-day-5" class="day-btn">الجمعة</button>
                    <button type="button" onclick="toggleDay(2, 6)" id="box2-day-6" class="day-btn">السبت</button>
                  </div>
                </div>
                
                <div class="time-input-group">
                  <div class="time-input-field">
                    <input type="number" id="box2-hours" min="0" max="23" value="12">
                    <label>ساعة</label>
                  </div>
                  <span style="font-size: 1.5em; color: #9ca3af;">:</span>
                  <div class="time-input-field">
                    <input type="number" id="box2-minutes" min="0" max="59" value="0">
                    <label>دقيقة</label>
                  </div>
                </div>
                
                <button onclick="setTimer(2)" class="btn btn-orange" style="width: 100%;">تفعيل الجدولة</button>
                <div id="timer-display-2" class="timer-display">
                  الفتح التلقائي في: <span id="timer-countdown-2">00:00:00</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- عمليات الصيانة -->
      <div class="maintenance-section">
        <h2 class="section-title">عمليات الصيانة والتحميل</h2>
        <div class="maintenance-buttons">
          <button onclick="loadMode()" class="btn btn-cyan">
            <span>🧪</span>
            <span>تدوير للأنبوب</span>
          </button>
          <button onclick="goZero()" class="btn btn-purple">
            <span>🔄</span>
            <span>العودة للصفر</span>
          </button>
        </div>
        <p class="maintenance-note">استخدم هذه الأزرار لتحميل الدواء أو إعادة ضبط الجهاز</p>
      </div>
      
      <!-- نتيجة العملية -->
      <div class="result-box">
        <h3 class="result-title">حالة النظام:</h3>
        <p class="result-text" id="result">اختر إجراءً لبدء العمل...</p>
      </div>
    </div>
  </div>

  <script>
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

      fetch('/api/schedules', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          box: boxId,
          hour: hours,
          minute: minutes,
          enabled: true,
          days: selectedDays[boxId]
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
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({box: boxId})
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
    
    window.onload = function() {
      updateTime();
      setInterval(updateTime, 1000);
    };
  </script>
</body>
</html>
'''

# صفحة الإدارة - بدون إنترنت
HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>لوحة تحكم الروبوت الذكي لتوزيع الأدوية</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect fill='%233b82f6' rx='15' width='100' height='100'/><text x='50' y='68' font-size='50' text-anchor='middle' fill='white'>💊</text></svg>">
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
    }
    
    .icon-svg {
      width: 40px;
      height: 40px;
      fill: currentColor;
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
    
    .project-info {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 15px;
      padding: 15px 25px;
      color: white;
      margin-bottom: 20px;
      text-align: center;
    }
    
    .project-info h3 {
      font-size: 1.1em;
      margin-bottom: 8px;
      font-weight: 700;
    }
    
    .project-info p {
      font-size: 0.85em;
      margin: 3px 0;
      opacity: 0.95;
    }
    
    .project-info .students {
      margin: 5px 0;
      font-weight: 600;
    }
    
    .project-info .supervisor {
      margin-top: 5px;
      font-style: italic;
      opacity: 0.9;
    }
    
    .time-status {
      background: #dbeafe;
      border-radius: 12px;
      padding: 10px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 15px;
      margin-bottom: 20px;
    }
    
    .time-display {
      display: flex;
      gap: 8px;
      align-items: center;
    }
    
    .time-box {
      display: flex;
      align-items: center;
      gap: 5px;
    }
    
    .time-label {
      font-size: 0.75em;
      color: #6b7280;
    }
    
    .time-value {
      background: white;
      padding: 5px 10px;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      color: #1e40af;
      font-weight: 700;
      font-size: 1em;
      min-width: 30px;
      text-align: center;
    }
    
    .status-indicator {
      display: flex;
      align-items: center;
      padding: 6px 15px;
      border-radius: 20px;
      font-weight: 600;
      gap: 8px;
      font-size: 0.9em;
      white-space: nowrap;
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
    
    .btn-robot {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      position: relative;
      overflow: hidden;
    }
    
    .btn-robot:disabled {
      background: #9ca3af;
      cursor: not-allowed;
      opacity: 0.6;
    }
    
    .btn-robot.running {
      background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
      animation: robotPulse 1.5s infinite;
    }
    
    @keyframes robotPulse {
      0%, 100% { transform: scale(1); }
      50% { transform: scale(1.05); }
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
    
    /* تحسينات لشاشة 7 بوصة (800x480) */
    @media (max-width: 900px) {
      body {
        padding: 10px;
      }
      
      .dashboard-card {
        padding: 20px;
        border-radius: 15px;
      }
      
      .header {
        margin-bottom: 20px;
        gap: 15px;
      }
      
      .robot-icon {
        width: 50px;
        height: 50px;
        border-radius: 12px;
      }
      
      .icon-svg {
        width: 25px;
        height: 25px;
      }
      
      h1 {
        font-size: 1.3em;
      }
      
      .subtitle {
        font-size: 0.85em;
      }
      
      .btn {
        padding: 8px 16px;
        font-size: 0.85em;
      }
      
      .project-info {
        padding: 10px 15px;
      }
      
      .project-info h3 {
        font-size: 0.9em;
      }
      
      .project-info p {
        font-size: 0.75em;
      }
      
      .time-status {
        flex-direction: column;
        padding: 8px 15px;
        gap: 8px;
      }
      
      .time-display {
        gap: 5px;
      }
      
      .time-value {
        font-size: 0.9em;
        padding: 4px 8px;
        min-width: 25px;
      }
      
      .time-label {
        font-size: 0.7em;
      }
      
      .section-title {
        font-size: 1.3em;
        margin-bottom: 15px;
      }
      
      .medicine-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        margin-bottom: 15px;
      }
      
      .medicine-box {
        border-radius: 12px;
      }
      
      .box-content {
        padding: 15px 10px;
      }
      
      .box-icon svg {
        width: 40px;
        height: 40px;
      }
      
      .medicine-name {
        font-size: 1em;
        margin-bottom: 10px;
      }
      
      .schedule-controls {
        padding: 12px;
        margin-top: 12px;
      }
      
      .day-btn {
        padding: 5px 8px;
        font-size: 0.75em;
      }
      
      .time-input-field input {
        width: 50px;
        padding: 6px;
        font-size: 0.9em;
      }
      
      .timer-display {
        padding: 10px;
        font-size: 0.85em;
      }
      
      .maintenance-section {
        margin-bottom: 20px;
      }
      
      .result-box {
        padding: 15px;
      }
      
      .result-title {
        font-size: 1em;
      }
      
      .result-text {
        font-size: 0.9em;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="dashboard-card">
      <!-- رأس الصفحة -->
      <div class="header">
        <div class="header-title">
          <div class="robot-icon" style="color: #3b82f6;">
            <svg class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="4" y="8" width="16" height="12" rx="2"/>
              <path d="M8 12h8M8 16h4"/>
              <circle cx="8" cy="4" r="1"/>
              <circle cx="16" cy="4" r="1"/>
              <line x1="8" y1="5" x2="8" y2="8"/>
              <line x1="16" y1="5" x2="16" y2="8"/>
            </svg>
          </div>
          <div>
            <h1>الروبوت الذكي لتوزيع الأدوية</h1>
            <p class="subtitle">نظام إدارة الأدوية الآلي المتكامل</p>
          </div>
        </div>
        
        <a href="/statistics" class="btn btn-purple" style="margin-left: 10px;">
          <svg class="icon-svg" style="width: 20px; height: 20px;" viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
          </svg>
          <span>الإحصائيات</span>
        </a>
        <a href="/patient" class="btn btn-green">
          <svg class="icon-svg" style="width: 20px; height: 20px;" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
          </svg>
          <span>شاشة المريض</span>
        </a>
      </div>
      
      
      <div class="time-status">
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
        <div class="status-indicator status-ready" id="status">
          <span class="status-dot"></span>
          <span>جاهز للعمل</span>
        </div>
      </div>
      
      <!-- صناديق الأدوية -->
      <div style="margin-top: 40px;">
        <div class="medicine-grid">
          <!-- الصندوق 1 -->
          <div class="medicine-box" style="position: relative;">
            <div class="box-lid"></div>
            <div class="box-content">
              <div class="box-number">1</div>
              <div class="box-icon" style="color: #3b82f6;">
                <svg width="60" height="60" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M4.22 11.29l6.36-6.36c1.95-1.95 5.12-1.95 7.07 0 1.95 1.95 1.95 5.12 0 7.07l-6.36 6.36c-1.95 1.95-5.12 1.95-7.07 0-1.95-1.95-1.95-5.12 0-7.07z"/>
                  <path d="M15 9l-6 6" stroke="white" stroke-width="1.5"/>
                </svg>
              </div>
              <div class="medicine-name-input" style="margin-bottom: 10px;">
                <input type="text" id="box1-name" placeholder="اسم الدواء" value="الجرعة الأولى" 
                  style="width: 100%; padding: 8px; border: 2px solid #e5e7eb; border-radius: 8px; text-align: center; font-weight: 600;">
              </div>
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
              <div class="box-icon" style="color: #10b981;">
                <svg width="60" height="60" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M4.22 11.29l6.36-6.36c1.95-1.95 5.12-1.95 7.07 0 1.95 1.95 1.95 5.12 0 7.07l-6.36 6.36c-1.95 1.95-5.12 1.95-7.07 0-1.95-1.95-1.95-5.12 0-7.07z"/>
                  <path d="M15 9l-6 6" stroke="white" stroke-width="1.5"/>
                </svg>
              </div>
              <div class="medicine-name-input" style="margin-bottom: 10px;">
                <input type="text" id="box2-name" placeholder="اسم الدواء" value="الجرعة الثانية" 
                  style="width: 100%; padding: 8px; border: 2px solid #e5e7eb; border-radius: 8px; text-align: center; font-weight: 600;">
              </div>
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
          <button onclick="startRobot()" class="btn btn-robot" id="robotBtn">
            <svg class="icon-svg" style="width: 20px; height: 20px;" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zM4 7v2h16V7H4zm8 3c-1.1 0-2 .9-2 2v8h4v-8c0-1.1-.9-2-2-2zm-6 0c-1.1 0-2 .9-2 2v8h4v-8c0-1.1-.9-2-2-2zm12 0c-1.1 0-2 .9-2 2v8h4v-8c0-1.1-.9-2-2-2z"/>
            </svg>
            <span>تحريك الروبوت</span>
          </button>
          <button onclick="loadMode()" class="btn btn-cyan">
            <svg class="icon-svg" style="width: 20px; height: 20px;" viewBox="0 0 24 24" fill="currentColor">
              <path d="M7 2v7.24A6 6 0 1 0 13 15a5.94 5.94 0 0 0-.24-1.68L19 7.07V2zm4 13a2 2 0 1 1-4 0 2 2 0 0 1 4 0z"/>
            </svg>
            <span>إضافة الجرعات</span>
          </button>
          <button onclick="goZero()" class="btn btn-purple">
            <svg class="icon-svg" style="width: 20px; height: 20px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>
              <path d="M21 3v5h-5"/>
              <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>
            </svg>
            <span>معايرة الصندوق</span>
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
          <!-- معلومات المشروع -->
      <div class="project-info">
        <h3>مدرسة عبدالله بن علي المسند الثانوية للبنين الثانوية للبنين</h3>
        <p style="font-size: 0.95em; font-weight: 600; margin: 5px 0;">مشروع: الروبوت الذكي لتوزيع الأدوية</p>
        <p class="students">عمل الطلاب: محمد وليد عمارة • عبد الله خالد النعيمي</p>
        <p class="supervisor">تحت إشراف المدرب: هشام بن عبد الرحمن سالمي</p>
      </div>
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

      // إضافة اسم الدواء
      const medicineName = document.getElementById(`box${boxId}-name`).value;

      fetch('/api/schedules', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
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
    
    // التحكم في الروبوت
    let robotRunning = false;
    
    async function startRobot() {
      const btn = document.getElementById('robotBtn');
      
      if (!robotRunning) {
        // تشغيل الروبوت
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
        // إيقاف الروبوت
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
    
    window.onload = function() {
      updateTime();
      setInterval(updateTime, 1000);
      loadSchedules(); // تحميل الجداول المحفوظة
    };
  </script>
</body>
</html>
'''


# صفحة المريض - تصميم محسّن
PATIENT_HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>مواعيد الدواء - متابعة الأدوية</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect fill='%233b82f6' rx='15' width='100' height='100'/><text x='50' y='68' font-size='50' text-anchor='middle' fill='white'>💊</text></svg>">
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    body {
      background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
      color: #333;
      min-height: 100vh;
      padding: 20px;
      line-height: 1.6;
    }
    
    .container {
      max-width: 900px;
      margin: 0 auto;
    }
    
    header {
      text-align: center;
      margin-bottom: 40px;
      padding: 20px;
      background: linear-gradient(to right, #4b6cb7, #182848);
      color: white;
      border-radius: 15px;
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 15px;
    }
    
    .header-content {
      flex: 1;
      text-align: center;
    }
    
    h1 {
      font-size: 2.5rem;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 15px;
      color: white;
      font-weight: 700;
    }
    
    h1 svg {
      width: 40px;
      height: 40px;
      fill: #ffd166;
    }
    
    .subtitle {
      font-size: 1.2rem;
      opacity: 0.9;
      color: white;
    }
    
    .control-btn {
      background: white;
      color: #4b6cb7;
      padding: 12px 24px;
      border-radius: 50px;
      font-weight: 700;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 10px;
      transition: all 0.3s;
      border: none;
      cursor: pointer;
      font-size: 1rem;
      box-shadow: 0 3px 10px rgba(0,0,0,0.2);
    }
    
    .control-btn:hover {
      transform: scale(1.05);
      box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    .control-btn svg {
      width: 20px;
      height: 20px;
      fill: currentColor;
    }
    
    .medication-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 25px;
      margin-bottom: 40px;
    }
    
    .medication-card {
      background: white;
      border-radius: 15px;
      overflow: hidden;
      box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      position: relative;
    }
    
    .medication-card:hover {
      transform: translateY(-10px);
      box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
    }
    
    .medication-card.urgent {
      animation: pulse 1s infinite;
      border: 3px solid #ef4444;
    }
    
    @keyframes pulse {
      0%, 100% { transform: scale(1); }
      50% { transform: scale(1.02); }
    }
    
    .card-header {
      padding: 20px;
      color: white;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    
    .medication-1 .card-header {
      background: linear-gradient(to right, #11998e, #38ef7d);
    }
    
    .medication-2 .card-header {
      background: linear-gradient(to right, #4A00E0, #8E2DE2);
    }
    
    .medication-name {
      font-size: 1.8rem;
      font-weight: 700;
      color: white;
    }
    
    .medication-icon {
      font-size: 2.5rem;
      opacity: 0.9;
    }
    
    .medication-icon svg {
      width: 40px;
      height: 40px;
      fill: white;
    }
    
    .card-content {
      padding: 25px;
    }
    
    .time-display {
      text-align: center;
      margin-bottom: 20px;
      padding: 15px;
      background-color: #f8f9fa;
      border-radius: 10px;
      border: 2px dashed #dee2e6;
    }
    
    .current-time {
      font-size: 2.2rem;
      font-weight: 700;
      color: #182848;
      display: block;
      margin-bottom: 5px;
      direction: ltr;
      font-variant-numeric: tabular-nums;
    }
    
    .time-label {
      color: #6c757d;
      font-size: 1.1rem;
    }
    
    .next-dose {
      background: #fff9e6;
      padding: 15px;
      border-radius: 10px;
      border-right: 5px solid #ffc107;
      margin-top: 15px;
    }
    
    .next-dose h3 {
      color: #856404;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 1.2rem;
    }
    
    .next-dose h3 svg {
      width: 20px;
      height: 20px;
      fill: #ffc107;
    }
    
    .next-dose-time {
      font-size: 1.5rem;
      font-weight: 600;
      color: #182848;
      direction: ltr;
      text-align: center;
      margin: 10px 0;
      font-variant-numeric: tabular-nums;
    }
    
    .next-dose-time.warning {
      color: #f59e0b;
      font-size: 1.8rem;
    }
    
    .next-dose-time.danger {
      color: #ef4444;
      font-size: 2rem;
      animation: blink 1s infinite;
    }
    
    @keyframes blink {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.7; }
    }
    
    .dose-description {
      color: #666;
      text-align: center;
      margin-top: 10px;
      font-size: 0.95rem;
    }
    
    .instructions {
      margin-top: 20px;
      padding-top: 15px;
      border-top: 1px solid #eee;
      color: #666;
      font-size: 0.95rem;
    }
    
    .instructions svg {
      width: 16px;
      height: 16px;
      fill: #4b6cb7;
      margin-left: 5px;
      display: inline-block;
      vertical-align: middle;
    }
    
    .no-schedule {
      background: white;
      border-radius: 15px;
      padding: 80px;
      text-align: center;
      box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
    }
    
    .no-schedule-icon {
      font-size: 9rem;
      color: #d1d5db;
      margin-bottom: 24px;
    }
    
    .no-schedule-icon svg {
      width: 144px;
      height: 144px;
      fill: #d1d5db;
    }
    
    .no-schedule h2 {
      font-size: 2rem;
      font-weight: 700;
      color: #6b7280;
      margin-bottom: 16px;
    }
    
    .no-schedule p {
      font-size: 1.2rem;
      color: #9ca3af;
    }
    
    footer {
      text-align: center;
      margin-top: 40px;
      padding: 20px;
      color: #666;
      font-size: 0.9rem;
    }
    
    /* تحسينات لشاشة 7 بوصة (800×480) */
    @media (max-width: 900px) {
      body {
        padding: 10px;
      }
      
      header {
        padding: 15px;
        margin-bottom: 20px;
      }
      
      h1 {
        font-size: 1.3rem;
      }
      
      h1 svg {
        width: 25px;
        height: 25px;
      }
      
      .subtitle {
        font-size: 0.85rem;
      }
      
      .control-btn {
        padding: 8px 16px;
        font-size: 0.85rem;
      }
      
      .medication-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        margin-bottom: 15px;
      }
      
      .medication-card {
        border-radius: 12px;
      }
      
      .card-header {
        padding: 15px;
      }
      
      .medication-name {
        font-size: 1.3rem;
      }
      
      .medication-icon svg {
        width: 30px;
        height: 30px;
      }
      
      .card-content {
        padding: 15px;
      }
      
      .current-time {
        font-size: 1.5rem;
      }
      
      .next-dose-time {
        font-size: 1.2rem;
      }
      
      .next-dose-time.warning {
        font-size: 1.4rem;
      }
      
      .next-dose-time.danger {
        font-size: 1.6rem;
      }
      
      .no-schedule {
        padding: 40px 20px;
      }
      
      .no-schedule-icon svg {
        width: 80px;
        height: 80px;
      }
      
      .no-schedule h2 {
        font-size: 1.3rem;
      }
      
      .no-schedule p {
        font-size: 0.9rem;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="header-content">
        <h1>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4.22 11.29l6.36-6.36c1.95-1.95 5.12-1.95 7.07 0 1.95 1.95 1.95 5.12 0 7.07l-6.36 6.36c-1.95 1.95-5.12 1.95-7.07 0-1.95-1.95-1.95-5.12 0-7.07z"/>
            <path d="M15 9l-6 6" stroke="white" stroke-width="1.5"/>
          </svg>
          متابعة مواعيد الدواء
        </h1>
        <p class="subtitle">تذكر دوائك في الوقت المناسب لتحافظ على صحتك</p>
      </div>
      <a href="/" class="control-btn">
        <svg viewBox="0 0 24 24">
          <path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/>
        </svg>
        لوحة التحكم
      </a>
    </header>
    
    <div id="medicines-container" class="medication-grid">
      <!-- سيتم ملؤها ديناميكياً -->
    </div>
    
    <div id="no-schedule" class="no-schedule" style="display: none;">
      <div class="no-schedule-icon">
        <svg viewBox="0 0 24 24">
          <path d="M19 4h-1V2h-2v2H8V2H6v2H5c-1.11 0-1.99.9-1.99 2L3 20c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V10h14v10zM9 14H7v-2h2v2zm4 0h-2v-2h2v2zm4 0h-2v-2h2v2zm-8 4H7v-2h2v2zm4 0h-2v-2h2v2zm4 0h-2v-2h2v2z"/>
        </svg>
      </div>
      <h2>لا توجد مواعيد مجدولة</h2>
      <p>يرجى ضبط مواعيد الأدوية من لوحة التحكم</p>
    </div>
    
    <footer style="background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%); color: white; border-radius: 15px; padding: 20px; text-align: center; margin-top: 20px;">
      <div style="margin-bottom: 15px;">
        <p style="font-size: 0.9em; opacity: 0.9;">تابع مواعيد أدويتك بانتظام لضمان فعاليتها</p>
      </div>
      <div style="background: rgba(255,255,255,0.15); border-radius: 10px; padding: 15px; margin-top: 10px;">
        <p style="font-weight: 700; margin-bottom: 8px; font-size: 1em;">مدرسة عبدالله بن علي المسند الثانوية للبنين الثانوية للبنين</p>
        <p style="font-size: 0.85em; margin: 5px 0;">مشروع: الروبوت الذكي لتوزيع الأدوية</p>
        <p style="font-size: 0.8em; opacity: 0.9; margin: 5px 0;">عمل الطلاب: محمد وليد عمارة • عبد الله خالد النعيمي</p>
        <p style="font-size: 0.75em; opacity: 0.8; font-style: italic;">تحت إشراف المدرب: هشام بن عبد الرحمن سالمي</p>
      </div>
    </footer>
  </div>
  
  <script>
    let schedules = {
      1: { hour: null, minute: null, enabled: false, name: 'الدواء الأول', icon: '<svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor"><path d="M4.22 11.29l6.36-6.36c1.95-1.95 5.12-1.95 7.07 0 1.95 1.95 1.95 5.12 0 7.07l-6.36 6.36c-1.95 1.95-5.12 1.95-7.07 0-1.95-1.95-1.95-5.12 0-7.07z"/><path d="M15 9l-6 6" stroke="white" stroke-width="1.5"/></svg>', color: 'blue' },
      2: { hour: null, minute: null, enabled: false, name: 'الدواء الثاني', icon: '<svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor"><path d="M4.22 11.29l6.36-6.36c1.95-1.95 5.12-1.95 7.07 0 1.95 1.95 1.95 5.12 0 7.07l-6.36 6.36c-1.95 1.95-5.12 1.95-7.07 0-1.95-1.95-1.95-5.12 0-7.07z"/><path d="M15 9l-6 6" stroke="white" stroke-width="1.5"/></svg>', color: 'green' }
    };
    
    let selectedDays = { 1: [], 2: [] };
    let audioPlayed = { 1: false, 2: false };
    
    // جلب الجداول من السيرفر
    async function loadSchedules() {
      try {
        const response = await fetch('/api/schedules');
        const data = await response.json();
        
        for (let boxId in data) {
          if (data[boxId].enabled) {
            schedules[boxId].hour = data[boxId].hour;
            schedules[boxId].minute = data[boxId].minute;
            schedules[boxId].enabled = data[boxId].enabled;
            selectedDays[boxId] = data[boxId].days || [];
          }
        }
        
        updateDisplay();
      } catch (error) {
        console.error('Error loading schedules:', error);
      }
    }
    
    // صوت التنبيه المحسّن - نغمة قوية ومتكررة
    function playWarningSound() {
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      
      // دالة لتشغيل نغمة واحدة
      function playTone(frequency, startTime, duration, volume) {
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = frequency;
        oscillator.type = 'square'; // صوت أقوى من sine
        
        gainNode.gain.setValueAtTime(volume, startTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + duration);
        
        oscillator.start(startTime);
        oscillator.stop(startTime + duration);
      }
      
      const now = audioContext.currentTime;
      
      // نمط تنبيه قوي: 5 نغمات متصاعدة
      playTone(600, now, 0.15, 0.5);
      playTone(800, now + 0.2, 0.15, 0.5);
      playTone(1000, now + 0.4, 0.15, 0.6);
      playTone(800, now + 0.6, 0.15, 0.5);
      playTone(1000, now + 0.8, 0.3, 0.7);
      
      // تكرار التنبيه بعد ثانية
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
      
      // إذا فات الموعد اليوم، البحث عن الموعد التالي
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
      
      return diff > 0 ? diff : null;
    }
    
    // تحديث العرض
    function updateDisplay() {
      const container = document.getElementById('medicines-container');
      const noSchedule = document.getElementById('no-schedule');
      
      let hasActiveSchedule = false;
      container.innerHTML = '';
      
      for (let boxId in schedules) {
        if (!schedules[boxId].enabled) continue;
        
        hasActiveSchedule = true;
        const remaining = calculateTimeRemaining(boxId);
        
        if (remaining === null) continue;
        
        const days = Math.floor(remaining / 86400);
        const hours = Math.floor((remaining % 86400) / 3600);
        const minutes = Math.floor((remaining % 3600) / 60);
        const seconds = remaining % 60;
        
        // الوقت الحالي
        const now = new Date();
        const currentHours = String(now.getHours()).padStart(2, '0');
        const currentMinutes = String(now.getMinutes()).padStart(2, '0');
        const currentSeconds = String(now.getSeconds()).padStart(2, '0');
        const currentTime = `${currentHours}:${currentMinutes}:${currentSeconds}`;
        
        let countdownText = '';
        if (days > 0) {
          countdownText = `بعد ${days} يوم و ${hours} ساعة`;
        } else if (hours > 0) {
          countdownText = `بعد ${hours} ساعة و ${minutes} دقيقة`;
        } else if (minutes > 0) {
          countdownText = `بعد ${minutes} دقيقة و ${seconds} ثانية`;
        } else {
          countdownText = `بعد ${seconds} ثانية`;
        }
        
        let countdownClass = '';
        let cardClass = '';
        let doseDescription = 'تناول الدواء في الموعد المحدد مع كوب من الماء';
        
        // تحذير قبل 10 ثواني
        if (remaining <= 10 && remaining > 0) {
          countdownText = `⚠ حان موعد الدواء الآن!`;
          countdownClass = 'danger';
          cardClass = 'urgent medication-' + boxId;
          doseDescription = 'تنبيه: حان موعد تناول الدواء الآن!';
          
          if (!audioPlayed[boxId]) {
            playWarningSound();
            audioPlayed[boxId] = true;
          }
        } else if (remaining <= 60) {
          countdownClass = 'warning';
          doseDescription = 'تحضير: موعد الدواء خلال دقيقة واحدة';
          audioPlayed[boxId] = false;
        } else {
          audioPlayed[boxId] = false;
        }
        
        const medicationIcon = boxId == 1 
          ? '<svg width="40" height="40" viewBox="0 0 24 24" fill="white"><path d="M4.22 11.29l6.36-6.36c1.95-1.95 5.12-1.95 7.07 0 1.95 1.95 1.95 5.12 0 7.07l-6.36 6.36c-1.95 1.95-5.12 1.95-7.07 0-1.95-1.95-1.95-5.12 0-7.07z"/><path d="M15 9l-6 6" stroke="white" stroke-width="1.5"/></svg>'
          : '<svg width="40" height="40" viewBox="0 0 24 24" fill="white"><rect x="9" y="2" width="6" height="20" rx="2"/><rect x="2" y="9" width="20" height="6" rx="2"/></svg>';
        
        const card = `
          <div class="medication-card ${cardClass}">
            <div class="card-header">
              <div class="medication-name">${schedules[boxId].name}</div>
              <div class="medication-icon">${medicationIcon}</div>
            </div>
            <div class="card-content">
              <div class="time-display">
                <span class="time-label">الوقت الحالي</span>
                <span class="current-time">${currentTime}</span>
              </div>
              
              <div class="next-dose">
                <h3>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 6v6l4 2"/>
                  </svg>
                  موعد الجرعة التالية
                </h3>
                <div class="next-dose-time ${countdownClass}">${countdownText}</div>
                <p class="dose-description">${doseDescription}</p>
              </div>
              
              <div class="instructions">
                <p>
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
                  </svg>
                  تعليمات: يجب تناول هذا الدواء في المواعيد المحددة للحصول على أفضل النتائج العلاجية.
                </p>
                                                <!-- معلومات المشروع -->
              </div>
              </div>
            </div>


          </div>


        `;
        
        container.innerHTML += card;
      }
      
      if (!hasActiveSchedule) {
        container.style.display = 'none';
        noSchedule.style.display = 'block';
      } else {
        container.style.display = 'grid';
        noSchedule.style.display = 'none';
      }
    }
    
    // تحديث كل ثانية
    setInterval(updateDisplay, 1000);
    
    // تحديث الجداول كل 5 ثواني
    setInterval(loadSchedules, 5000);
    
    // تحميل أول مرة
    loadSchedules();
  </script>
</body>
</html>
'''


# =========================
#  كود السيرفر (Flask)
# =========================

from flask import Flask, request, jsonify, Response
import time
import serial
import serial.tools.list_ports

# استيراد وحدة قاعدة البيانات
from database import (
    init_database, get_all_schedules, save_schedule, 
    log_dose, get_dose_logs, get_dose_statistics, get_today_doses,
    get_setting, save_setting
)

try:
    # سيتم استخدامه على الراسبيري باي للتحكم في الأرجل
    import RPi.GPIO as GPIO
    HAS_GPIO = True
except ImportError:
    # هذا يسمح بتجربة الكود على جهاز عادي بدون الراسبيري باي
    GPIO = None
    HAS_GPIO = False


app = Flask(__name__)

# ===========================
# تعريف الأرجل والمتغيرات
# ===========================

# أرقام GPIO للسيرفو والأبواب
CAROUSEL = 18      # سيرفو الدوران (20kg)
GATE1 = 23         # باب الصندوق 1
GATE2 = 24         # باب الصندوق 2

# زوايا الصناديق (صندوقين فقط)
BOX_ANGLES = {
    1: 0,      # الصندوق الأول
    2: 90      # الصندوق الثاني
}

ZERO_ANGLE = 0         # نقطة الصفر المرجعية
HOME = 45              # وضع وسط آمن
GATE_OPEN = 70         # زاوية فتح الباب
GATE_CLOSE = 0         # زاوية غلق الباب
LOADING_ANGLE = 180    # زاوية أنبوب إدخال الدواء

# متغيرات PWM
pwm_carousel = None
pwm_gate1 = None
pwm_gate2 = None


def setup_gpio():
    """تهيئة أرجل GPIO والسيرفو."""
    global pwm_carousel, pwm_gate1, pwm_gate2
    
    if not HAS_GPIO:
        return

    GPIO.setmode(GPIO.BCM)

    # تهيئة الأرجل
    GPIO.setup(CAROUSEL, GPIO.OUT)
    GPIO.setup(GATE1, GPIO.OUT)
    GPIO.setup(GATE2, GPIO.OUT)

    # إنشاء كائنات PWM (50Hz للسيرفو)
    pwm_carousel = GPIO.PWM(CAROUSEL, 50)
    pwm_gate1 = GPIO.PWM(GATE1, 50)
    pwm_gate2 = GPIO.PWM(GATE2, 50)

    # بدء PWM
    pwm_carousel.start(0)
    pwm_gate1.start(0)
    pwm_gate2.start(0)


def move_servo(pwm, angle):
    """تحريك السيرفو إلى زاوية محددة (0-180 درجة)."""
    if not HAS_GPIO or pwm is None:
        return
    
    # تحويل الزاوية إلى duty cycle
    # للسيرفو: 0° = 2%, 90° = 7.5%, 180° = 12.5%
    duty = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)  # إيقاف PWM


def load_medicine():
    """تدوير العلبة إلى وضع إدخال الدواء (أنبوب التحميل)."""
    # تدوير العلبة إلى نقطة الأنبوب
    move_servo(pwm_carousel, LOADING_ANGLE)
    time.sleep(0.7)


def go_home_zero():
    """إرجاع العلبة إلى نقطة الصفر المرجعية."""
    move_servo(pwm_carousel, ZERO_ANGLE)
    time.sleep(0.6)


@app.route("/", methods=["GET"])
def index():
    """عرض واجهة التحكم."""
    return Response(HTML, mimetype="text/html; charset=utf-8")


@app.route("/patient", methods=["GET"])
def patient():
    """عرض شاشة المريض."""
    return Response(PATIENT_HTML, mimetype="text/html; charset=utf-8")


# صفحة الإحصائيات
STATISTICS_HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>إحصائيات النظام - الروبوت الذكي</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect fill='%233b82f6' rx='15' width='100' height='100'/><text x='50' y='68' font-size='50' text-anchor='middle' fill='white'>💊</text></svg>">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', Tahoma, sans-serif;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      min-height: 100vh;
      padding: 20px;
      color: white;
    }
    .container { max-width: 1000px; margin: 0 auto; }
    
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 30px;
      flex-wrap: wrap;
      gap: 15px;
    }
    
    h1 {
      font-size: 1.8em;
      display: flex;
      align-items: center;
      gap: 15px;
    }
    
    .btn {
      padding: 10px 20px;
      border: none;
      border-radius: 10px;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.3s;
    }
    
    .btn-back {
      background: rgba(255,255,255,0.1);
      color: white;
      border: 1px solid rgba(255,255,255,0.2);
    }
    
    .btn-back:hover {
      background: rgba(255,255,255,0.2);
    }
    
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 20px;
      margin-bottom: 30px;
    }
    
    .stat-card {
      background: rgba(255,255,255,0.1);
      border-radius: 15px;
      padding: 25px;
      text-align: center;
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255,255,255,0.1);
    }
    
    .stat-value {
      font-size: 3em;
      font-weight: 700;
      margin-bottom: 10px;
    }
    
    .stat-label {
      color: rgba(255,255,255,0.7);
      font-size: 0.95em;
    }
    
    .stat-card.blue .stat-value { color: #60a5fa; }
    .stat-card.green .stat-value { color: #34d399; }
    .stat-card.yellow .stat-value { color: #fbbf24; }
    .stat-card.purple .stat-value { color: #a78bfa; }
    
    .logs-section {
      background: rgba(255,255,255,0.05);
      border-radius: 15px;
      padding: 25px;
      border: 1px solid rgba(255,255,255,0.1);
    }
    
    .logs-title {
      font-size: 1.3em;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    
    .logs-table {
      width: 100%;
      border-collapse: collapse;
    }
    
    .logs-table th,
    .logs-table td {
      padding: 12px 15px;
      text-align: right;
      border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    .logs-table th {
      background: rgba(255,255,255,0.1);
      font-weight: 600;
    }
    
    .logs-table tr:hover {
      background: rgba(255,255,255,0.05);
    }
    
    .status-badge {
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 0.85em;
      font-weight: 600;
    }
    
    .status-success {
      background: rgba(52, 211, 153, 0.2);
      color: #34d399;
    }
    
    .status-dispensed {
      background: rgba(96, 165, 250, 0.2);
      color: #60a5fa;
    }
    
    .empty-state {
      text-align: center;
      padding: 40px;
      color: rgba(255,255,255,0.5);
    }
    
    @media (max-width: 600px) {
      body { padding: 10px; }
      h1 { font-size: 1.3em; }
      .stat-value { font-size: 2em; }
      .logs-table { font-size: 0.85em; }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>📊 إحصائيات النظام</h1>
      <a href="/" class="btn btn-back">
        <span>←</span>
        <span>العودة للوحة التحكم</span>
      </a>
    </div>
    
    <div class="stats-grid" id="stats-grid">
      <div class="stat-card blue">
        <div class="stat-value" id="total-doses">0</div>
        <div class="stat-label">إجمالي الجرعات</div>
      </div>
      <div class="stat-card green">
        <div class="stat-value" id="today-doses">0</div>
        <div class="stat-label">جرعات اليوم</div>
      </div>
      <div class="stat-card yellow">
        <div class="stat-value" id="success-rate">100%</div>
        <div class="stat-label">نسبة النجاح</div>
      </div>
      <div class="stat-card purple">
        <div class="stat-value" id="active-schedules">0</div>
        <div class="stat-label">جداول نشطة</div>
      </div>
    </div>
    
    <div class="logs-section">
      <h2 class="logs-title">� سجل الجرعات المصروفة</h2>
      <table class="logs-table">
        <thead>
          <tr>
            <th>التاريخ والوقت</th>
            <th>الصندوق</th>
            <th>الحالة</th>
          </tr>
        </thead>
        <tbody id="doses-body">
          <tr>
            <td colspan="3" class="empty-state">جاري التحميل...</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="logs-section" style="margin-top: 20px;">
      <h2 class="logs-title">⚙️ سجل تحديثات الجداول</h2>
      <table class="logs-table">
        <thead>
          <tr>
            <th>التاريخ والوقت</th>
            <th>الصندوق</th>
            <th>التفاصيل</th>
          </tr>
        </thead>
        <tbody id="updates-body">
          <tr>
            <td colspan="3" class="empty-state">جاري التحميل...</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  
  <script>
    async function loadStatistics() {
      try {
        const statsRes = await fetch('/api/statistics');
        const stats = await statsRes.json();
        
        document.getElementById('total-doses').innerText = stats.total_doses || 0;
        document.getElementById('today-doses').innerText = stats.today_doses || 0;
        document.getElementById('success-rate').innerText = (stats.success_rate || 100) + '%';
        
        const schedulesRes = await fetch('/api/schedules');
        const schedules = await schedulesRes.json();
        let activeCount = 0;
        for (let box in schedules) {
          if (schedules[box].enabled) activeCount++;
        }
        document.getElementById('active-schedules').innerText = activeCount;
        
      } catch (error) {
        console.error('Error loading statistics:', error);
      }
    }
    
    async function loadLogs() {
      try {
        const response = await fetch('/api/logs?limit=50');
        const logs = await response.json();
        
        // فصل الجرعات عن التحديثات
        const doses = logs.filter(log => log.action === 'dispensed');
        const updates = logs.filter(log => log.action === 'schedule_updated');
        
        // عرض الجرعات
        const dosesBody = document.getElementById('doses-body');
        if (doses.length === 0) {
          dosesBody.innerHTML = '<tr><td colspan="3" class="empty-state">لم يتم صرف أي جرعات بعد</td></tr>';
        } else {
          dosesBody.innerHTML = doses.slice(0, 15).map(log => {
            const date = new Date(log.timestamp);
            const dateStr = date.toLocaleDateString('ar-SA');
            const timeStr = date.toLocaleTimeString('ar-SA', {hour: '2-digit', minute: '2-digit'});
            
            return `
              <tr>
                <td>${dateStr} ${timeStr}</td>
                <td>الصندوق ${log.box_id}</td>
                <td><span class="status-badge status-dispensed">تم الصرف ✓</span></td>
              </tr>
            `;
          }).join('');
        }
        
        // عرض التحديثات
        const updatesBody = document.getElementById('updates-body');
        if (updates.length === 0) {
          updatesBody.innerHTML = '<tr><td colspan="3" class="empty-state">لا توجد تحديثات</td></tr>';
        } else {
          updatesBody.innerHTML = updates.slice(0, 10).map(log => {
            const date = new Date(log.timestamp);
            const dateStr = date.toLocaleDateString('ar-SA');
            const timeStr = date.toLocaleTimeString('ar-SA', {hour: '2-digit', minute: '2-digit'});
            
            return `
              <tr>
                <td>${dateStr} ${timeStr}</td>
                <td>الصندوق ${log.box_id}</td>
                <td><span class="status-badge status-success">${log.notes || 'تحديث الجدول'}</span></td>
              </tr>
            `;
          }).join('');
        }
        
      } catch (error) {
        console.error('Error loading logs:', error);
      }
    }
    
    loadStatistics();
    loadLogs();
    
    // تحديث كل 10 ثواني
    setInterval(loadStatistics, 10000);
    setInterval(loadLogs, 10000);
  </script>
</body>
</html>
'''


@app.route("/statistics", methods=["GET"])
def statistics():
    """عرض صفحة الإحصائيات."""
    return Response(STATISTICS_HTML, mimetype="text/html; charset=utf-8")


@app.route("/open_box", methods=["POST"])
def open_box():
    """فتح صندوق دواء وصرف الجرعة - يحرك الهاردوير الحقيقي."""
    try:
        data = request.get_json(silent=True) or {}
        box = int(data.get("box", 0))

        if box not in BOX_ANGLES:
            return jsonify({"status": f"✗ رقم الصندوق {box} غير صحيح"}), 400

        # اختيار الباب المناسب
        if box == 1:
            gate_pwm = pwm_gate1
        else:  # box == 2
            gate_pwm = pwm_gate2

        # 1️⃣ تدوير العلبة إلى زاوية الصندوق
        move_servo(pwm_carousel, BOX_ANGLES[box])
        time.sleep(0.6)

        # 2️⃣ فتح الباب
        move_servo(gate_pwm, GATE_OPEN)
        time.sleep(1.2)

        # 3️⃣ غلق الباب
        move_servo(gate_pwm, GATE_CLOSE)
        time.sleep(0.3)

        # 4️⃣ الرجوع للوضع الآمن ثم الصفر
        move_servo(pwm_carousel, HOME)
        time.sleep(0.4)
        move_servo(pwm_carousel, ZERO_ANGLE)
        time.sleep(0.4)

        # تسجيل الجرعة في قاعدة البيانات
        log_dose(box, 'dispensed', 'success', 'صرف جرعة تلقائي')
        return jsonify({"status": f"✓ تم صرف جرعة من الصندوق {box} بنجاح"})

    except Exception as e:
        return jsonify({"status": f"✗ خطأ في فتح الصندوق: {str(e)}"}), 500


@app.route("/load_mode", methods=["POST"])
def load_mode():
    """تدوير العلبة إلى وضع إدخال الدواء."""
    try:
        load_medicine()
        return jsonify({"status": "✓ تم تدوير العلبة لوضع إدخال الدواء"})
    except Exception as e:
        return jsonify({"status": f"✗ خطأ في وضع التحميل: {str(e)}"}), 500


@app.route("/go_zero", methods=["POST"])
def go_zero():
    """إرجاع العلبة إلى نقطة الصفر المرجعية."""
    try:
        go_home_zero()
        return jsonify({"status": "✓ تمت العودة إلى نقطة الصفر بنجاح"})
    except Exception as e:
        return jsonify({"status": f"✗ خطأ في العودة للصفر: {str(e)}"}), 500


# قاعدة البيانات - الجداول محفوظة بشكل دائم


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
        
        if box in [1, 2]:
            save_schedule(
                box_id=box,
                hour=data.get("hour"),
                minute=data.get("minute"),
                enabled=data.get("enabled", False),
                days=data.get("days", []),
                medicine_name=data.get("medicine_name")
            )
            # تسجيل الحدث
            log_dose(box, 'schedule_updated', 'success', 
                     f"تم تحديث الجدول: {data.get('hour')}:{data.get('minute')}")
            return jsonify({"status": "success", "message": "تم حفظ الجدول بنجاح"})
        return jsonify({"status": "error", "message": "رقم الصندوق غير صحيح"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


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


# ========== التحكم في الروبوت ==========
# محاولة الاتصال بـ Arduino
arduino_serial = None
try:
    # البحث عن Arduino في المنافذ المتاحة
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'Arduino' in port.description or 'CH340' in port.description or 'USB' in port.description:
            try:
                arduino_serial = serial.Serial(port.device, 9600, timeout=1)
                print(f"✓ تم الاتصال بـ Arduino على المنفذ: {port.device}")
                break
            except:
                continue
    
    if not arduino_serial:
        print("⚠️ لم يتم العثور على Arduino - سيتم العمل بدون روبوت")
except Exception as e:
    print(f"⚠️ خطأ في الاتصال بـ Arduino: {e}")


@app.route("/robot/start", methods=["POST"])
def start_robot():
    """تشغيل الروبوت للحركة الأمامية."""
    try:
        if arduino_serial and arduino_serial.is_open:
            arduino_serial.write(b"START\n")
            arduino_serial.flush()
            return jsonify({"status": "started", "message": "الروبوت يتحرك للأمام"})
        else:
            return jsonify({"status": "error", "message": "Arduino غير متصل"}), 503
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/robot/stop", methods=["POST"])
def stop_robot():
    """إيقاف الروبوت."""
    try:
        if arduino_serial and arduino_serial.is_open:
            arduino_serial.write(b"STOP\n")
            arduino_serial.flush()
            # قراءة الرد من Arduino
            response = arduino_serial.readline().decode('utf-8').strip()
            return jsonify({"status": "stopped", "message": "تم إيقاف الروبوت", "arduino_response": response})
        else:
            return jsonify({"status": "error", "message": "Arduino غير متصل"}), 503
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/robot/status", methods=["GET"])
def robot_status():
    """الحصول على حالة الروبوت."""
    try:
        if arduino_serial and arduino_serial.is_open:
            arduino_serial.write(b"STATUS\n")
            arduino_serial.flush()
            response = arduino_serial.readline().decode('utf-8').strip()
            return jsonify({"status": "ok", "arduino_status": response})
        else:
            return jsonify({"status": "disconnected", "message": "Arduino غير متصل"}), 503
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    # تهيئة قاعدة البيانات
    init_database()
    
    if HAS_GPIO:
        setup_gpio()
    
    print("=" * 50)
    print("🤖 نظام توزيع الأدوية الذكي")
    print("=" * 50)
    print(f"GPIO متاح: {HAS_GPIO}")
    print(f"العنوان: http://0.0.0.0:5000")
    print("اضغط Ctrl+C للإيقاف")
    print("=" * 50)
    
    # تشغيل السيرفر على كل الواجهات ليستقبل من أي جهاز في الشبكة
    try:
        app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\n⚠️ إيقاف البرنامج...")
        if HAS_GPIO and pwm_carousel:
            pwm_carousel.stop()
            pwm_gate1.stop()
            pwm_gate2.stop()
            GPIO.cleanup()
        print("✓ تم إيقاف النظام بنجاح")

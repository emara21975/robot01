/**
 * صفحة الإحصائيات - Statistics JavaScript
 */

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
                const timeStr = date.toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' });

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
                const timeStr = date.toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' });

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

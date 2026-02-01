# -*- coding: utf-8 -*-
"""
قاعدة بيانات SQLite لنظام توزيع الأدوية
تعمل بشكل ممتاز على Raspberry Pi
"""

import sqlite3
import json
from datetime import datetime
import os

# مسار قاعدة البيانات (في نفس مجلد التطبيق)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'medibox.db')


def get_connection():
    """إنشاء اتصال بقاعدة البيانات."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # للوصول للأعمدة بالاسم
    return conn


def init_database():
    """إنشاء جداول قاعدة البيانات."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # جدول جداول الأدوية
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            box_id INTEGER PRIMARY KEY,
            hour INTEGER,
            minute INTEGER,
            enabled INTEGER DEFAULT 0,
            days TEXT DEFAULT '[]',
            medicine_name TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # جدول سجل الجرعات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dose_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            box_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'success',
            notes TEXT DEFAULT ''
        )
    ''')
    
    # جدول الإعدادات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # التحقق من الأعمدة الجديدة وإضافتها (Migration)
    current_columns = []
    cursor.execute("PRAGMA table_info(schedules)")
    for col in cursor.fetchall():
        current_columns.append(col['name'])
    
    # 1. stock_count
    if 'stock_count' not in current_columns:
        print("⚡ جاري إضافة عمود stock_count...")
        cursor.execute("ALTER TABLE schedules ADD COLUMN stock_count INTEGER DEFAULT 0")
        
    # 2. dose_per_dispense
    if 'dose_per_dispense' not in current_columns:
        print("⚡ جاري إضافة عمود dose_per_dispense...")
        cursor.execute("ALTER TABLE schedules ADD COLUMN dose_per_dispense INTEGER DEFAULT 1")
        
    # 3. low_stock_threshold
    if 'low_stock_threshold' not in current_columns:
        print("⚡ جاري إضافة عمود low_stock_threshold...")
        cursor.execute("ALTER TABLE schedules ADD COLUMN low_stock_threshold INTEGER DEFAULT 5")
        
    # 4. pharmacy_url
    if 'pharmacy_url' not in current_columns:
        print("⚡ جاري إضافة عمود pharmacy_url...")
        cursor.execute("ALTER TABLE schedules ADD COLUMN pharmacy_url TEXT DEFAULT 'https://kuludonline.com/'")
    
    # إدخال بيانات افتراضية للصناديق
    for i in range(1, 5): # 4 صناديق
        cursor.execute('SELECT COUNT(*) FROM schedules WHERE box_id = ?', (i,))
        if cursor.fetchone()[0] == 0:
            print(f"➕ تهيئة بيانات الصندوق {i}...")
            cursor.execute('''
                INSERT INTO schedules (
                    box_id, hour, minute, enabled, days, medicine_name,
                    stock_count, dose_per_dispense, low_stock_threshold, pharmacy_url
                )
                VALUES (?, NULL, NULL, 0, '[]', ?, 0, 1, 5, 'https://kuludonline.com/')
            ''', (i, f'الجرعة {i}'))
    
    conn.commit()
    conn.close()
    print("✓ تم تهيئة قاعدة البيانات بنجاح")


# ===========================
# وظائف جداول الأدوية
# ===========================

def get_all_schedules():
    """الحصول على جميع جداول الأدوية."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM schedules')
    rows = cursor.fetchall()
    conn.close()
    
    result = {}
    for row in rows:
        result[row['box_id']] = {
            'hour': row['hour'],
            'minute': row['minute'],
            'enabled': bool(row['enabled']),
            'days': json.loads(row['days'] or '[]'),
            'medicine_name': row['medicine_name'],
            'stock_count': row['stock_count'],
            'dose_per_dispense': row['dose_per_dispense'],
            'low_stock_threshold': row['low_stock_threshold'],
            'pharmacy_url': row['pharmacy_url']
        }
    
    return result


def get_schedule(box_id):
    """الحصول على جدول صندوق معين."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM schedules WHERE box_id = ?', (box_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'hour': row['hour'],
            'minute': row['minute'],
            'enabled': bool(row['enabled']),
            'days': json.loads(row['days'] or '[]'),
            'medicine_name': row['medicine_name'],
            'stock_count': row['stock_count'],
            'dose_per_dispense': row['dose_per_dispense'],
            'low_stock_threshold': row['low_stock_threshold'],
            'pharmacy_url': row['pharmacy_url']
        }
    return None


def save_schedule(box_id, hour, minute, enabled, days, medicine_name=None, 
                  stock_count=None, dose_per_dispense=1, low_stock_threshold=5, pharmacy_url=None):
    """حفظ أو تحديث جدول صندوق."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # التحقق من وجود السجل
    cursor.execute('SELECT COUNT(*) FROM schedules WHERE box_id = ?', (box_id,))
    exists = cursor.fetchone()[0] > 0
    
    if exists:
        query = '''
            UPDATE schedules 
            SET hour = ?, minute = ?, enabled = ?, days = ?, updated_at = ?
        '''
        params = [hour, minute, 1 if enabled else 0, json.dumps(days), datetime.now().isoformat()]
        
        if medicine_name is not None:
            query += ", medicine_name = ?"
            params.append(medicine_name)
            
        if stock_count is not None:
            query += ", stock_count = ?"
            params.append(stock_count)
            
        if dose_per_dispense is not None:
            query += ", dose_per_dispense = ?"
            params.append(dose_per_dispense)
            
        if low_stock_threshold is not None:
            query += ", low_stock_threshold = ?"
            params.append(low_stock_threshold)
            
        if pharmacy_url is not None:
            query += ", pharmacy_url = ?"
            params.append(pharmacy_url)
            
        query += " WHERE box_id = ?"
        params.append(box_id)
        
        cursor.execute(query, tuple(params))
    else:
        cursor.execute('''
            INSERT INTO schedules (
                box_id, hour, minute, enabled, days, medicine_name,
                stock_count, dose_per_dispense, low_stock_threshold, pharmacy_url
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            box_id, hour, minute, 1 if enabled else 0, json.dumps(days), 
            medicine_name or f'الصندوق {box_id}',
            stock_count or 0, dose_per_dispense or 1, 
            low_stock_threshold or 5, pharmacy_url or 'https://kuludonline.com/'
        ))
    
    conn.commit()
    conn.close()
    return True


def disable_schedule(box_id):
    """تعطيل جدول صندوق."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE schedules SET enabled = 0, updated_at = ? WHERE box_id = ?
    ''', (datetime.now().isoformat(), box_id))
    
    conn.commit()
    conn.close()


# ===========================
# وظائف سجل الجرعات
# ===========================

def log_dose(box_id, action, status='success', notes=''):
    """تسجيل حدث جرعة."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO dose_logs (box_id, action, timestamp, status, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (box_id, action, datetime.now().isoformat(), status, notes))
    
    conn.commit()
    conn.close()


def get_dose_logs(box_id=None, limit=50):
    """الحصول على سجل الجرعات."""
    conn = get_connection()
    cursor = conn.cursor()
    
    if box_id:
        cursor.execute('''
            SELECT * FROM dose_logs WHERE box_id = ? ORDER BY timestamp DESC LIMIT ?
        ''', (box_id, limit))
    else:
        cursor.execute('''
            SELECT * FROM dose_logs ORDER BY timestamp DESC LIMIT ?
        ''', (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_today_doses():
    """الحصول على جرعات اليوم."""
    conn = get_connection()
    cursor = conn.cursor()
    
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT * FROM dose_logs WHERE timestamp LIKE ? ORDER BY timestamp DESC
    ''', (f'{today}%',))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_dose_statistics():
    """الحصول على إحصائيات الجرعات."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # إجمالي الجرعات (صرف فقط)
    cursor.execute('SELECT COUNT(*) FROM dose_logs WHERE action = "dispensed"')
    total = cursor.fetchone()[0]
    
    # جرعات اليوم
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT COUNT(*) FROM dose_logs 
        WHERE action = "dispensed" AND timestamp LIKE ?
    ''', (f'{today}%',))
    today_count = cursor.fetchone()[0]
    
    # جرعات ناجحة (من الجرعات المصروفة فقط)
    cursor.execute('SELECT COUNT(*) FROM dose_logs WHERE action = "dispensed" AND status = "success"')
    success = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_doses': total,
        'today_doses': today_count,
        'success_count': success,
        'success_rate': round((success / total * 100), 1) if total > 0 else 100
    }


# ===========================
# وظائف الإعدادات
# ===========================

def get_setting(key, default=None):
    """الحصول على قيمة إعداد."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
    row = cursor.fetchone()
    conn.close()
    
    return row['value'] if row else default


def save_setting(key, value):
    """حفظ إعداد."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO settings (key, value, updated_at)
        VALUES (?, ?, ?)
    ''', (key, value, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()


def get_all_settings():
    """الحصول على جميع الإعدادات."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT key, value FROM settings')
    rows = cursor.fetchall()
    conn.close()
    
    return {row['key']: row['value'] for row in rows}


# تهيئة قاعدة البيانات عند استيراد الملف
if __name__ == '__main__':
    init_database()
    print(f"مسار قاعدة البيانات: {DB_PATH}")
    
    # اختبار
    schedules = get_all_schedules()
    print(f"الجداول الحالية: {schedules}")

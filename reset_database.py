# -*- coding: utf-8 -*-
"""
سكريبت حذف جميع البيانات وإعادة التهيئة
Reset Database - Clear all data and start fresh
"""

import os
import sqlite3
from pathlib import Path

def reset_databases():
    """حذف جميع البيانات وإعادة إنشاء قواعد البيانات الفارغة."""
    
    print("=" * 60)
    print("🗑️  بدء عملية حذف البيانات وإعادة التهيئة")
    print("=" * 60)
    
    # 1. حذف قاعدة البيانات الرئيسية (medibox.db)
    medibox_db = "medibox.db"
    if os.path.exists(medibox_db):
        try:
            os.remove(medibox_db)
            print(f"✅ تم حذف {medibox_db}")
        except Exception as e:
            print(f"❌ خطأ في حذف {medibox_db}: {e}")
    else:
        print(f"⚠️  {medibox_db} غير موجود")
    
    # 2. حذف قاعدة بيانات السجلات (audit.db)
    audit_db = "audit.db"
    if os.path.exists(audit_db):
        try:
            os.remove(audit_db)
            print(f"✅ تم حذف {audit_db}")
        except Exception as e:
            print(f"❌ خطأ في حذف {audit_db}: {e}")
    else:
        print(f"⚠️  {audit_db} غير موجود")
    
    # 3. حذف قاعدة بيانات الوجوه (face_db.json)
    face_db = Path("robot/camera/face_db.json")
    if face_db.exists():
        try:
            os.remove(face_db)
            print(f"✅ تم حذف {face_db}")
        except Exception as e:
            print(f"❌ خطأ في حذف {face_db}: {e}")
    else:
        print(f"⚠️  {face_db} غير موجود")
    
    # 4. حذف صور الوجوه المسجلة
    faces_dir = Path("robot/camera/faces")
    if faces_dir.exists():
        try:
            import shutil
            shutil.rmtree(faces_dir)
            print(f"✅ تم حذف مجلد الوجوه {faces_dir}")
        except Exception as e:
            print(f"❌ خطأ في حذف {faces_dir}: {e}")
    else:
        print(f"⚠️  مجلد الوجوه غير موجود")
    
    print("\n" + "=" * 60)
    print("🔄 إعادة تهيئة قواعد البيانات...")
    print("=" * 60)
    
    # 5. إعادة إنشاء قواعد البيانات الفارغة
    try:
        from database import init_database
        init_database()
        print("✅ تم إعادة تهيئة قاعدة بيانات medibox.db")
    except Exception as e:
        print(f"❌ خطأ في إعادة التهيئة: {e}")
    
    # 6. إعادة إنشاء قاعدة بيانات السجلات
    try:
        from robot.audit_log import init_audit_db
        init_audit_db()
        print("✅ تم إعادة تهيئة قاعدة بيانات audit.db")
    except Exception as e:
        print(f"⚠️  تعذر إعادة تهيئة audit.db: {e}")
    
    # 7. إعادة إنشاء مجلد الوجوه
    try:
        faces_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ تم إنشاء مجلد الوجوه {faces_dir}")
    except Exception as e:
        print(f"⚠️  تعذر إنشاء مجلد الوجوه: {e}")
    
    print("\n" + "=" * 60)
    print("✅ تمت عملية إعادة التهيئة بنجاح!")
    print("=" * 60)
    print("\n📌 ملاحظات:")
    print("   • تم حذف جميع الجداول والمواعيد")
    print("   • تم حذف جميع سجلات الصرف")
    print("   • تم حذف جميع الوجوه المسجلة")
    print("   • يمكنك الآن البدء بتسجيل مواعيد جديدة")
    print("   • لا تنسَ تسجيل الوجوه مرة أخرى إذا كان النظام مفعّلاً")
    print("\n")


if __name__ == "__main__":
    # تأكيد من المستخدم
    print("\n⚠️  تحذير: هذا السكريبت سيحذف جميع البيانات!")
    print("   • جميع المواعيد المسجلة")
    print("   • جميع سجلات الصرف")
    print("   • جميع الوجوه المسجلة")
    print("   • الإعدادات")
    print("\n")
    
    confirm = input("هل أنت متأكد من المتابعة؟ اكتب 'نعم' للتأكيد: ")
    
    if confirm.strip().lower() in ['نعم', 'yes', 'y']:
        reset_databases()
    else:
        print("❌ تم إلغاء العملية")

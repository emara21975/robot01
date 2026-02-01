#!/bin/bash

# Robot System Cleanup & Restart Script
# -----------------------------------

echo "🧹 Starting Cleanup..."

# 1. Clean Python Cache (__pycache__ and .pyc)
echo "   - Removing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete

# 2. Clean Flask/System Cache
echo "   - Removing temporary caches..."
rm -rf cache
rm -rf flask_cache
rm -rf flask_session
rm -rf /tmp/flask_session/* 2>/dev/null

# 3. Clean Camera/AI Temp Files
echo "   - Removing camera/AI temp files..."
rm -rf /tmp/*.jpg 2>/dev/null
rm -rf robot/camera/tmp/* 2>/dev/null

echo "✅ Cleanup Complete."

# 4. Restart Logic (Optional - if run manually)
# If called from Python, Python will handle the restart.
# If run manually, uncomment below:
# echo "🔄 Restarting Service..."
# sudo systemctl restart robot.service

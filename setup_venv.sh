#!/bin/bash

echo "🚀 Re-creating Virtual Environment with System Site Packages..."

# Deactivate if running
deactivate 2>/dev/null

# Remove old venv
echo "🗑️  Removing old venv..."
rm -rf venv

# Create new venv with system packages access (Critical for Picamera2)
echo "✨ Creating new venv..."
python3 -m venv venv --system-site-packages

# Activate
source venv/bin/activate

# Upgrade pip (good practice)
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "📦 Installing requirements..."
    pip install -r requirements.txt
else
    echo "⚠️  requirements.txt not found!"
fi

echo "✅ Done! Environment is ready."
echo "👉 To activate: source venv/bin/activate"

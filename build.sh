#!/bin/bash
set -e

echo "🔧 Installing Python 3.11 dependencies..."
python --version

echo "📦 Upgrading pip and build tools..."
pip install --upgrade pip setuptools wheel

echo "📚 Installing requirements..."
pip install -r requirements.txt

echo "✅ Build complete!"

# Setup Guide

## Quick Start

### 1. System Requirements
- Python 3.7 or higher
- MongoDB 4.0 or higher
- Webcam
- 4GB RAM minimum (8GB recommended)
- GPU optional (for faster training)

### 2. Install MongoDB

**Ubuntu/Debian:**
```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

**macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Windows:**
Download from [MongoDB Official Site](https://www.mongodb.com/try/download/community)

### 3. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Download Pre-trained Models

The FaceNet model should be placed in `PreTrained_model/facenet_keras.h5`

Download from: [FaceNet Keras](https://github.com/nyoki-mtl/keras-facenet)

### 5. Verify Installation

```bash
# Test MongoDB connection
python3 -c "import pymongo; client = pymongo.MongoClient(); print('MongoDB OK')"

# Test OpenCV
python3 -c "import cv2; print('OpenCV OK')"

# Test TensorFlow
python3 -c "import tensorflow as tf; print('TensorFlow OK')"
```

### 6. Initialize Database

The database will be automatically created when you enroll the first student.

### 7. Run the Application

**Desktop GUI:**
```bash
python3 UI.py
```

**Web Interface:**
```bash
python3 app_web.py
# Open browser: http://localhost:5000
```

**API Server:**
```bash
python3 api.py
# API available at: http://localhost:5000/api
```

## Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running: `sudo systemctl status mongodb`
- Check connection string in config.py

### Camera Not Working
- Check camera permissions
- Try different camera index in config.py
- Test with: `python3 -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"`

### Model Not Loading
- Ensure facenet_keras.h5 is in PreTrained_model/
- Check file permissions
- Verify TensorFlow installation

### Import Errors
- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

## Development Mode

For development with auto-reload:
```bash
export FLASK_ENV=development
python3 app_web.py
```

## Production Deployment

For production use:
1. Set `API_DEBUG = False` in config.py
2. Use a production WSGI server (gunicorn, uwsgi)
3. Set up proper authentication
4. Use environment variables for sensitive data
5. Configure MongoDB with authentication
6. Set up HTTPS/SSL

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app_web:app
```

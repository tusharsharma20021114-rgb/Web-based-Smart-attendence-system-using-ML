"""
Main Flask Application for Smart Attendance System
Author: Tushar Sharma
"""

from flask import Flask, render_template, request, jsonify, Response, session
from flask_cors import CORS
import os
import cv2
import numpy as np
from datetime import datetime
import pandas as pd
import pymongo
import secrets
import json
from werkzeug.utils import secure_filename
import base64

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'temp_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MongoDB connection
try:
    client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
    client.server_info()
    db = client["students"]
    MONGO_AVAILABLE = True
except:
    MONGO_AVAILABLE = False
    db = None

# Load models on startup
MODELS_LOADED = False
recognition_model = None
embedding_model = None
face_detector = None

def load_models():
    global recognition_model, embedding_model, face_detector, MODELS_LOADED
    try:
        from keras.models import load_model
        from embedding import emb
        from FaceDetection.face_detection import face
        
        recognition_model = load_model('Model/Face_recognition.MODEL')
        embedding_model = emb()
        face_detector = face()
        MODELS_LOADED = True
        print("✅ Models loaded successfully")
    except Exception as e:
        print(f"⚠️  Models not loaded: {e}")
        MODELS_LOADED = False

# Routes
@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/enroll')
def enroll_page():
    """Student enrollment page"""
    return render_template('enroll.html')

@app.route('/attendance')
def attendance_page():
    """Attendance marking page"""
    return render_template('attendance.html')

@app.route('/records')
def records_page():
    """View attendance records"""
    return render_template('records.html')

# API Endpoints
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': MODELS_LOADED,
        'mongodb_connected': MONGO_AVAILABLE
    })

@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all enrolled students"""
    try:
        if os.path.exists("Students_Enrollment.csv"):
            df = pd.read_csv("Students_Enrollment.csv")
            students = df.to_dict('records')
        else:
            students = []
        
        return jsonify({
            'success': True,
            'count': len(students),
            'students': students
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/students/enroll', methods=['POST'])
def enroll_student():
    """Enroll a new student"""
    try:
        data = request.json
        name = data.get('name')
        roll_no = data.get('roll_number')
        
        if not name or not roll_no:
            return jsonify({'success': False, 'error': 'Name and roll number required'}), 400
        
        # Add to MongoDB
        if MONGO_AVAILABLE:
            mydict = {"Name": name, "Roll_number": roll_no, "Attendance": 0}
            db.Hindi.insert_one(mydict.copy())
            db.English.insert_one(mydict.copy())
        
        # Add to CSV
        if os.path.exists("Students_Enrollment.csv"):
            df = pd.read_csv("Students_Enrollment.csv")
        else:
            df = pd.DataFrame(columns=['Name', 'Roll Number'])
        
        df = df.append({'Name': name, 'Roll Number': roll_no}, ignore_index=True)
        df.to_csv("Students_Enrollment.csv", index=False)
        
        # Create directory
        path = f"people/{roll_no}{name}"
        os.makedirs(path, exist_ok=True)
        
        return jsonify({
            'success': True,
            'message': 'Student enrolled successfully',
            'student': {'name': name, 'roll_number': roll_no}
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/students/save-image', methods=['POST'])
def save_student_image():
    """Save student training image"""
    try:
        data = request.json
        roll_no = data.get('roll_number')
        name = data.get('name')
        image_data = data.get('image')
        image_count = data.get('count', 1)
        
        if not all([roll_no, name, image_data]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Save image
        path = f"people/{roll_no}{name}"
        os.makedirs(path, exist_ok=True)
        cv2.imwrite(f"{path}/{image_count}.jpg", img)
        
        return jsonify({
            'success': True,
            'message': f'Image {image_count} saved',
            'count': image_count
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/attendance/<subject>', methods=['GET'])
def get_attendance(subject):
    """Get attendance for a specific subject"""
    try:
        if not MONGO_AVAILABLE:
            return jsonify({'success': False, 'error': 'MongoDB not available'}), 503
        
        collection = db.Hindi if subject.lower() == 'hindi' else db.English
        records = list(collection.find({}, {'_id': 0}))
        
        return jsonify({
            'success': True,
            'subject': subject,
            'count': len(records),
            'records': records
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/attendance/mark', methods=['POST'])
def mark_attendance():
    """Mark attendance from uploaded image"""
    try:
        if not MODELS_LOADED:
            load_models()
            if not MODELS_LOADED:
                return jsonify({'success': False, 'error': 'Models not loaded'}), 500
        
        data = request.json
        image_data = data.get('image')
        subject = data.get('subject', 'english')
        
        if not image_data:
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        # Decode image
        image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Detect and recognize
        det, coor = face_detector.detectFace(frame)
        
        if not det or len(det) == 0:
            return jsonify({'success': False, 'error': 'No face detected'}), 400
        
        recognized_students = []
        
        for detected in det:
            detected_resized = cv2.resize(detected, (160, 160))
            detected_resized = detected_resized.astype('float') / 255.0
            detected_resized = np.expand_dims(detected_resized, axis=0)
            
            feed = embedding_model.calculate(detected_resized)
            feed = np.expand_dims(feed, axis=0)
            prediction = recognition_model.predict(feed)[0]
            
            result = int(np.argmax(prediction))
            confidence = float(np.max(prediction))
            
            if confidence > 0.85:
                people_list = sorted(os.listdir('people'))
                students = {int(p[0])-1: p[1:] for p in people_list}
                
                if result in students:
                    student_name = students[result]
                    recognized_students.append({
                        'name': student_name,
                        'confidence': confidence,
                        'roll_number': result + 1
                    })
        
        return jsonify({
            'success': True,
            'recognized': len(recognized_students) > 0,
            'students': recognized_students
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Get attendance statistics"""
    try:
        stats = {}
        
        if MONGO_AVAILABLE:
            for subject in ['Hindi', 'English']:
                records = list(db[subject].find({}, {'_id': 0}))
                total = len(records)
                avg = sum(r.get('Attendance', 0) for r in records) / total if total > 0 else 0
                
                stats[subject.lower()] = {
                    'total_students': total,
                    'average_attendance': round(avg, 2)
                }
        else:
            stats = {'hindi': {'total_students': 0, 'average_attendance': 0},
                    'english': {'total_students': 0, 'average_attendance': 0}}
        
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/train', methods=['POST'])
def train_model():
    """Trigger model training"""
    try:
        from Model_train import Model_Training
        from threading import Thread
        
        Thread(target=Model_Training).start()
        
        return jsonify({
            'success': True,
            'message': 'Model training started in background'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Smart Attendance System Starting...")
    print("📡 Access at: http://localhost:5000")
    load_models()
    app.run(debug=True, host='0.0.0.0', port=5000)

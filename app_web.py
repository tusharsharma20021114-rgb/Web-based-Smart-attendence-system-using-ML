"""
Web Application with Flask Backend
Author: Tushar Sharma
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import cv2
import numpy as np
from datetime import datetime
import pandas as pd
import pymongo
from keras.models import load_model
from embedding import emb
from FaceDetection.face_detection import face
import base64
import io
from PIL import Image
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
CORS(app)

# MongoDB connection
try:
    client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
    client.server_info()
    db = client["students"]
    MONGO_AVAILABLE = True
except:
    MONGO_AVAILABLE = False
    print("⚠️  MongoDB not available - running in limited mode")

# Load models
try:
    recognition_model = load_model('Model/Face_recognition.MODEL')
    embedding_model = emb()
    face_detector = face()
    MODELS_LOADED = True
except:
    recognition_model = None
    embedding_model = None
    face_detector = None
    MODELS_LOADED = False
    print("⚠️  Models not loaded - train the model first")

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')

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
        df = pd.read_csv("Students_Enrollment.csv")
        students = df.to_dict('records')
        return jsonify({
            'success': True,
            'count': len(students),
            'students': students
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/students', methods=['POST'])
def enroll_student():
    """Enroll a new student"""
    try:
        data = request.json
        name = data.get('name')
        roll_no = data.get('roll_number')
        
        if not name or not roll_no:
            return jsonify({'success': False, 'error': 'Name and roll number required'}), 400
        
        if MONGO_AVAILABLE:
            mydict = {"Name": name, "Roll_number": roll_no, "Attendance": 0}
            db.Hindi.insert_one(mydict)
            db.English.insert_one(mydict)
        
        df = pd.read_csv("Students_Enrollment.csv")
        df = df.append({'Name': name, 'Roll Number': roll_no}, ignore_index=True)
        df.to_csv("Students_Enrollment.csv", index=False)
        
        path = f"people/{roll_no}{name}"
        os.makedirs(path, exist_ok=True)
        
        return jsonify({'success': True, 'message': 'Student enrolled successfully'})
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
        
        return jsonify({'success': True, 'subject': subject, 'records': records})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Get attendance statistics"""
    try:
        stats = {}
        for subject in ['Hindi', 'English']:
            if MONGO_AVAILABLE:
                records = list(db[subject].find({}, {'_id': 0}))
            else:
                records = []
            
            total = len(records)
            avg = sum(r.get('Attendance', 0) for r in records) / total if total > 0 else 0
            
            stats[subject.lower()] = {
                'total_students': total,
                'average_attendance': round(avg, 2)
            }
        
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Smart Attendance Web App Starting...")
    print("📡 Access at: http://localhost:5000")
    print("📚 API Docs: http://localhost:5000/api/health")
    app.run(debug=True, host='0.0.0.0', port=5000)


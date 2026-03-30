"""
Flask REST API for Smart Attendance System
Author: Ushar Sharma
"""

from flask import Flask, request, jsonify, send_file
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

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["students"]

# Load models
try:
    recognition_model = load_model('Model/Face_recognition.MODEL')
    embedding_model = emb()
    face_detector = face()
except:
    recognition_model = None
    embedding_model = None
    face_detector = None

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': recognition_model is not None
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
        
        # Add to MongoDB
        mydict = {"Name": name, "Roll_number": roll_no, "Attendance": 0}
        db.Hindi.insert_one(mydict)
        db.English.insert_one(mydict)
        
        # Add to CSV
        df = pd.read_csv("Students_Enrollment.csv")
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

@app.route('/api/attendance/<subject>', methods=['GET'])
def get_attendance(subject):
    """Get attendance for a specific subject"""
    try:
        if subject.lower() == 'hindi':
            collection = db.Hindi
            csv_path = "Hindi_attendance/Hindi_Attendance.csv"
        elif subject.lower() == 'english':
            collection = db.English
            csv_path = "English_attendance/English_Attendance.csv"
        else:
            return jsonify({'success': False, 'error': 'Invalid subject'}), 400
        
        records = list(collection.find({}, {'_id': 0}))
        
        return jsonify({
            'success': True,
            'subject': subject,
            'count': len(records),
            'records': records
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/attendance/<subject>/export', methods=['GET'])
def export_attendance(subject):
    """Export attendance as CSV"""
    try:
        if subject.lower() == 'hindi':
            csv_path = "Hindi_attendance/Hindi_Attendance.csv"
        elif subject.lower() == 'english':
            csv_path = "English_attendance/English_Attendance.csv"
        else:
            return jsonify({'success': False, 'error': 'Invalid subject'}), 400
        
        if os.path.exists(csv_path):
            return send_file(csv_path, as_attachment=True)
        else:
            return jsonify({'success': False, 'error': 'No attendance records found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/recognize', methods=['POST'])
def recognize_face():
    """Recognize face from uploaded image"""
    try:
        if not recognition_model or not embedding_model or not face_detector:
            return jsonify({'success': False, 'error': 'Models not loaded'}), 500
        
        # Get image from request
        data = request.json
        image_data = data.get('image')  # Base64 encoded image
        subject = data.get('subject', '2')  # Default to English
        
        if not image_data:
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
        image = Image.open(io.BytesIO(image_bytes))
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Detect face
        det, coor = face_detector.detectFace(frame)
        
        if not det:
            return jsonify({'success': False, 'error': 'No face detected'}), 400
        
        # Get embeddings and predict
        detected = cv2.resize(det[0], (160, 160))
        detected = detected.astype('float') / 255.0
        detected = np.expand_dims(detected, axis=0)
        feed = embedding_model.calculate(detected)
        feed = np.expand_dims(feed, axis=0)
        prediction = recognition_model.predict(feed)[0]
        
        result = int(np.argmax(prediction))
        confidence = float(np.max(prediction))
        
        # Get student info
        people_list = sorted(os.listdir('people'))
        students = {int(p[0])-1: p[1:] for p in people_list}
        
        if confidence > 0.85 and result in students:
            student_name = students[result]
            return jsonify({
                'success': True,
                'recognized': True,
                'student': student_name,
                'confidence': confidence,
                'roll_number': result + 1
            })
        else:
            return jsonify({
                'success': True,
                'recognized': False,
                'confidence': confidence
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Get attendance statistics"""
    try:
        stats = {}
        
        for subject in ['Hindi', 'English']:
            collection = db[subject]
            records = list(collection.find({}, {'_id': 0}))
            
            total_students = len(records)
            total_attendance = sum(r.get('Attendance', 0) for r in records)
            avg_attendance = total_attendance / total_students if total_students > 0 else 0
            
            stats[subject.lower()] = {
                'total_students': total_students,
                'total_attendance': total_attendance,
                'average_attendance': round(avg_attendance, 2)
            }
        
        return jsonify({
            'success': True,
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    """Get all available subjects"""
    return jsonify({
        'success': True,
        'subjects': ['Hindi', 'English']
    })

if __name__ == '__main__':
    print("🚀 Smart Attendance API Server Starting...")
    print("📡 API Documentation: http://localhost:5000/api/health")
    app.run(debug=True, host='0.0.0.0', port=5000)

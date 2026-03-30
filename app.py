"""
Smart Attendance System - Complete Web Application
Author: Tushar Sharma
Features: User Authentication, Student Registration, Attendance Marking
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
import cv2
import numpy as np
from datetime import datetime
import pandas as pd
import pymongo
import secrets
import base64
from functools import wraps

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

# MongoDB connection
try:
    MONGO_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client["students"]
    users_db = db["users"]
    MONGO_AVAILABLE = True
    print("✅ MongoDB connected")
except Exception as e:
    MONGO_AVAILABLE = False
    db = None
    users_db = None
    print(f"⚠️  MongoDB not available: {e}")

# Initialize default admin on startup
def init_admin():
    if MONGO_AVAILABLE:
        try:
            if users_db.count_documents({'email': 'admin@admin.com'}) == 0:
                admin = {
                    'name': 'Admin',
                    'email': 'admin@admin.com',
                    'password': generate_password_hash('admin123'),
                    'role': 'admin',
                    'created_at': datetime.now()
                }
                users_db.insert_one(admin)
                print("✅ Default admin created: admin@admin.com / admin123")
        except Exception as e:
            print(f"⚠️  Admin creation error: {e}")

# Initialize on startup
init_admin()

# Try to load models on startup
try:
    load_models()
except Exception as e:
    print(f"⚠️  Initial model load failed: {e}")

# Load models
MODELS_LOADED = False
recognition_model = None
embedding_model = None
face_detector = None

def load_models():
    global recognition_model, embedding_model, face_detector, MODELS_LOADED
    try:
        # Check if pretrained model exists
        if not os.path.exists('PreTrained_model/facenet_keras.h5'):
            print("⚠️  Pretrained model (facenet_keras.h5) not found")
            return False
        
        # Check if face cascade exists
        if not os.path.exists('FaceDetection/faces.xml'):
            print("⚠️  Face cascade (faces.xml) not found")
            return False
        
        from keras.models import load_model
        from embedding import emb
        from FaceDetection.face_detection import face
        
        # Load embedding model and face detector
        embedding_model = emb()
        face_detector = face()
        print("✅ Embedding model and face detector loaded")
        
        # Load recognition model if it exists
        if os.path.exists('Model/Face_recognition.MODEL'):
            recognition_model = load_model('Model/Face_recognition.MODEL')
            MODELS_LOADED = True
            print("✅ Recognition model loaded")
        else:
            print("⚠️  Recognition model not found - train first")
            MODELS_LOADED = False
        
        return True
    except Exception as e:
        print(f"⚠️  Model loading error: {e}")
        return False

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user = session.get('user_name', 'User')
    role = session.get('user_role', 'student')
    return render_template('dashboard.html', user=user, role=role)

@app.route('/enroll')
@login_required
def enroll_page():
    return render_template('enroll.html')

@app.route('/attendance')
@login_required
def attendance_page():
    return render_template('attendance.html')

@app.route('/records')
@login_required
def records_page():
    role = session.get('user_role', 'student')
    return render_template('records.html', role=role)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# API - Authentication
@app.route('/api/auth/register', methods=['POST'])
def api_register():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        roll_number = data.get('roll_number')
        role = data.get('role', 'student')
        
        if not all([name, email, password]):
            return jsonify({'success': False, 'error': 'All fields required'}), 400
        
        if not MONGO_AVAILABLE:
            return jsonify({'success': False, 'error': 'Database not available'}), 503
        
        # Check if user exists
        if users_db.find_one({'email': email}):
            return jsonify({'success': False, 'error': 'Email already registered'}), 400
        
        # Create user
        user = {
            'name': name,
            'email': email,
            'password': generate_password_hash(password),
            'roll_number': roll_number,
            'role': role,
            'created_at': datetime.now()
        }
        users_db.insert_one(user)
        
        # If student, also enroll in attendance system
        if role == 'student' and roll_number:
            mydict = {"Name": name, "Roll_number": roll_number, "Attendance": 0}
            db.Hindi.insert_one(mydict.copy())
            db.English.insert_one(mydict.copy())
            
            # Add to CSV
            if os.path.exists("Students_Enrollment.csv"):
                df = pd.read_csv("Students_Enrollment.csv")
            else:
                df = pd.DataFrame(columns=['Name', 'Roll Number'])
            
            new_row = pd.DataFrame([{'Name': name, 'Roll Number': roll_number}])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv("Students_Enrollment.csv", index=False)
            
            # Create directory
            os.makedirs(f"people/{roll_number}{name}", exist_ok=True)
        
        return jsonify({'success': True, 'message': 'Registration successful'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not MONGO_AVAILABLE:
            return jsonify({'success': False, 'error': 'Database not available'}), 503
        
        user = users_db.find_one({'email': email})
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            session['user_role'] = user.get('role', 'student')
            session['roll_number'] = user.get('roll_number')
            
            return jsonify({
                'success': True,
                'user': {
                    'name': user['name'],
                    'email': user['email'],
                    'role': user.get('role', 'student')
                }
            })
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# API - Students
@app.route('/api/students', methods=['GET'])
@login_required
def get_students():
    try:
        if os.path.exists("Students_Enrollment.csv"):
            df = pd.read_csv("Students_Enrollment.csv")
            students = df.to_dict('records')
        else:
            students = []
        return jsonify({'success': True, 'count': len(students), 'students': students})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/students/save-images', methods=['POST'])
@login_required
def save_student_images():
    try:
        data = request.json
        images = data.get('images', [])
        roll_number = session.get('roll_number')
        name = session.get('user_name')
        
        if not roll_number:
            return jsonify({'success': False, 'error': 'Roll number not found'}), 400
        
        path = f"people/{roll_number}{name}"
        os.makedirs(path, exist_ok=True)
        
        for idx, img_data in enumerate(images, 1):
            image_bytes = base64.b64decode(img_data.split(',')[1] if ',' in img_data else img_data)
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv2.imwrite(f"{path}/{idx}.jpg", img)
        
        return jsonify({'success': True, 'message': f'{len(images)} images saved'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# API - Attendance
@app.route('/api/attendance/<subject>', methods=['GET'])
@login_required
def get_attendance(subject):
    try:
        if not MONGO_AVAILABLE:
            return jsonify({'success': False, 'error': 'Database not available'}), 503
        
        collection = db.Hindi if subject.lower() == 'hindi' else db.English
        
        # If student, show only their record
        if session.get('user_role') == 'student':
            roll_number = session.get('roll_number')
            records = list(collection.find({'Roll_number': roll_number}, {'_id': 0}))
        else:
            records = list(collection.find({}, {'_id': 0}))
        
        return jsonify({'success': True, 'subject': subject, 'records': records})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/attendance/mark', methods=['POST'])
@login_required
def mark_attendance():
    global MODELS_LOADED, recognition_model, embedding_model, face_detector
    
    try:
        # Try to load models if not loaded
        if not MODELS_LOADED:
            print("Attempting to load models...")
            load_models()
            
        if not MODELS_LOADED or not recognition_model:
            return jsonify({
                'success': False, 
                'error': 'Recognition model not available. Admin needs to train the model first.',
                'action_required': 'train_model'
            }), 503
        
        if not embedding_model or not face_detector:
            return jsonify({
                'success': False,
                'error': 'Required models not loaded. Check if pretrained files exist.',
                'action_required': 'check_files'
            }), 503
        
        data = request.json
        image_data = data.get('image')
        subject = data.get('subject', 'english')
        
        if not image_data:
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        # Decode image
        image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Detect faces
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
                if people_list:
                    students = {int(p[0])-1: p[1:] for p in people_list}
                    
                    if result in students:
                        student_name = students[result]
                        roll_num = result + 1
                        
                        # Update attendance in MongoDB
                        if MONGO_AVAILABLE:
                            collection = db.Hindi if subject == 'hindi' else db.English
                            collection.update_one(
                                {"Roll_number": str(roll_num)},
                                {"$inc": {"Attendance": 1}}
                            )
                        
                        recognized_students.append({
                            'name': student_name,
                            'confidence': confidence,
                            'roll_number': roll_num
                        })
        
        return jsonify({
            'success': True,
            'recognized': len(recognized_students) > 0,
            'students': recognized_students
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
@login_required
def get_statistics():
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
@login_required
def train_model():
    try:
        # Check if user is admin
        if session.get('user_role') != 'admin':
            return jsonify({'success': False, 'error': 'Admin access required'}), 403
        
        from Model_train import Model_Training
        from threading import Thread
        
        Thread(target=Model_Training).start()
        
        return jsonify({'success': True, 'message': 'Model training started'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download-models', methods=['POST'])
@login_required
def download_models_endpoint():
    try:
        # Check if user is admin
        if session.get('user_role') != 'admin':
            return jsonify({'success': False, 'error': 'Admin access required'}), 403
        
        from download_models import ensure_models
        from threading import Thread
        
        def download_task():
            try:
                result = ensure_models()
                if result:
                    load_models()
                    print("✅ Models downloaded and loaded")
            except Exception as e:
                print(f"❌ Download error: {e}")
        
        Thread(target=download_task).start()
        
        return jsonify({'success': True, 'message': 'Model download started. Check back in 1-2 minutes.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    model_status = {
        'recognition_loaded': MODELS_LOADED,
        'embedding_loaded': embedding_model is not None,
        'face_detector_loaded': face_detector is not None,
        'pretrained_exists': os.path.exists('PreTrained_model/facenet_keras.h5'),
        'recognition_model_exists': os.path.exists('Model/Face_recognition.MODEL'),
        'face_cascade_exists': os.path.exists('FaceDetection/faces.xml')
    }
    
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'mongodb_connected': MONGO_AVAILABLE,
        'models': model_status
    })

if __name__ == '__main__':
    print("🚀 Smart Attendance System Starting...")
    print("📡 Web App: http://localhost:5000")
    
    # Create default admin if not exists
    if MONGO_AVAILABLE:
        try:
            if users_db.count_documents({'email': 'admin@admin.com'}) == 0:
                admin = {
                    'name': 'Admin',
                    'email': 'admin@admin.com',
                    'password': generate_password_hash('admin123'),
                    'role': 'admin',
                    'created_at': datetime.now()
                }
                users_db.insert_one(admin)
                print("✅ Default admin created: admin@admin.com / admin123")
            else:
                print("✅ Admin account exists")
        except Exception as e:
            print(f"⚠️  Admin creation error: {e}")
    else:
        print("⚠️  MongoDB not connected - cannot create admin")
    
    load_models()
    app.run(debug=True, host='0.0.0.0', port=5000)

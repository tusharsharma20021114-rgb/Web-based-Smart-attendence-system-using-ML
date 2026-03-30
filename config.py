"""
Configuration file for Smart Attendance System
Author: Ushar Sharma
"""

import os

class Config:
    # Application Settings
    APP_NAME = "Smart Attendance System"
    VERSION = "2.0.0"
    AUTHOR = "Ushar Sharma"
    
    # MongoDB Settings
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DB_NAME = 'students'
    MONGO_TIMEOUT = 2000
    
    # Model Settings
    MODEL_PATH = 'Model/Face_recognition.MODEL'
    PRETRAINED_MODEL_PATH = 'PreTrained_model/facenet_keras.h5'
    FACE_CASCADE_PATH = 'FaceDetection/faces.xml'
    
    # Training Parameters
    LEARNING_RATE = 0.01
    EPOCHS = 400
    BATCH_SIZE = 16
    
    # Recognition Settings
    CONFIDENCE_THRESHOLD = 0.85
    IMAGE_SIZE = (160, 160)
    ATTENDANCE_THRESHOLD = 30  # Number of frames before marking attendance
    
    # Camera Settings
    CAMERA_INDEX = 0
    CAPTURE_IMAGES_COUNT = 30
    
    # File Paths
    STUDENT_ENROLLMENT_CSV = 'Students_Enrollment.csv'
    PEOPLE_DIR = 'people'
    HINDI_ATTENDANCE_DIR = 'Hindi_attendance'
    ENGLISH_ATTENDANCE_DIR = 'English_attendance'
    
    # API Settings
    API_HOST = '0.0.0.0'
    API_PORT = 5000
    API_DEBUG = True
    
    # UI Colors
    COLORS = {
        'primary': '#8a2e7f',
        'secondary': '#507d2a',
        'accent': '#00aeff',
        'dark': '#262523',
        'light': '#ffffff',
        'success': '#28a745',
        'danger': '#dc3545',
        'warning': '#ffc107'
    }
    
    # Subjects
    SUBJECTS = ['Hindi', 'English']

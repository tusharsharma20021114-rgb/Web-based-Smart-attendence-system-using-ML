# How It Works

## Complete System Flow

### 1. User Registration & Authentication

**Student Registration:**
```
Student visits /register
→ Enters name, email, roll number, password
→ System creates user account in MongoDB
→ Automatically enrolls in Hindi & English subjects
→ Creates directory: people/{roll_number}{name}/
→ Redirects to login
```

**Login:**
```
User visits /login
→ Enters email & password
→ System verifies credentials
→ Creates session
→ Redirects to dashboard
```

### 2. Training Image Capture

**Process:**
```
Student logs in
→ Goes to /enroll page
→ Clicks "Start Camera"
→ Browser requests camera permission
→ Clicks "Capture Images"
→ System captures 30 images (one every 300ms)
→ Each image sent to API as base64
→ Server decodes and saves to people/{roll}{name}/
→ Progress bar shows completion
```

**Technical:**
- JavaScript `getUserMedia()` API for camera
- Canvas API to capture frames
- Base64 encoding for transmission
- OpenCV saves as JPEG files

### 3. Model Training

**Trigger:**
```
Admin clicks "Train Model"
→ API endpoint /api/train called
→ Background thread starts training
→ Model_train.py executes
```

**Training Process:**
```
1. Read Students_Enrollment.csv → Get number of classes
2. Load all images from people/ directory
3. Resize images to 160x160
4. Extract FaceNet embeddings (128-dim vectors)
5. Train neural network:
   - Input: 128 neurons
   - Hidden: 64 → 32 → 16 neurons (LeakyReLU)
   - Output: n_classes (Softmax)
6. Save model to Model/Face_recognition.MODEL
```

**Time:** ~30-40 seconds for small datasets

### 4. Attendance Marking

**Real-time Recognition:**
```
Student goes to /attendance
→ Selects subject (Hindi/English)
→ Clicks "Start Recognition"
→ Camera starts
→ Every 2 seconds:
   ├─ Capture frame from video
   ├─ Send to API as base64
   ├─ Server decodes image
   ├─ Detect face using Haar Cascade
   ├─ Extract face region
   ├─ Resize to 160x160
   ├─ Get FaceNet embedding
   ├─ Predict using trained model
   ├─ If confidence > 0.85:
   │  ├─ Identify student
   │  ├─ Update MongoDB attendance
   │  └─ Return student info
   └─ Display result on screen
```

**Attendance Update:**
```
MongoDB.{Subject}.update_one(
    {"Roll_number": roll_num},
    {"$inc": {"Attendance": 1}}
)
```

### 5. Viewing Records

**Data Flow:**
```
User goes to /records
→ Selects subject tab
→ API fetches from MongoDB
→ If student role: show only their record
→ If admin role: show all records
→ Display in table with:
   - Roll number
   - Name
   - Attendance count
   - Percentage
→ Export button downloads CSV
```

## Technical Architecture

### Frontend (Browser)
```
HTML Templates (Jinja2)
├─ login.html - Authentication
├─ register.html - Student registration
├─ dashboard.html - Statistics & quick actions
├─ enroll.html - Image capture
├─ attendance.html - Face recognition
└─ records.html - View data

CSS (static/css/style.css)
└─ Modern responsive design

JavaScript (static/js/main.js + inline)
├─ Camera access (getUserMedia)
├─ API calls (fetch)
├─ Real-time updates
└─ Notifications
```

### Backend (Flask)
```
app.py - Main application
├─ Authentication routes
│  ├─ /login, /register, /logout
│  └─ Session management
├─ Page routes
│  ├─ /dashboard, /enroll
│  ├─ /attendance, /records
│  └─ @login_required decorator
└─ API routes
   ├─ /api/auth/* - Login/register
   ├─ /api/students/* - Student management
   ├─ /api/attendance/* - Attendance operations
   ├─ /api/stats - Statistics
   └─ /api/train - Model training
```

### Database (MongoDB)
```
Database: students
├─ Collection: users
│  └─ {name, email, password_hash, roll_number, role}
├─ Collection: Hindi
│  └─ {Name, Roll_number, Attendance}
└─ Collection: English
   └─ {Name, Roll_number, Attendance}
```

### Machine Learning Pipeline
```
1. Face Detection
   └─ Haar Cascade Classifier (faces.xml)

2. Face Embedding
   └─ FaceNet (facenet_keras.h5)
   └─ Output: 128-dimensional vector

3. Classification
   └─ Custom Neural Network
   └─ Input: 128 → Hidden: 64,32,16 → Output: n_classes
   └─ Trained on student embeddings

4. Recognition
   └─ Confidence threshold: 0.85
   └─ Real-time prediction
```

## Security Features

- Password hashing with werkzeug
- Session-based authentication
- Role-based access control
- CORS enabled for API
- Input validation
- SQL injection prevention (NoSQL)

## Data Flow Diagram

```
Student Registration
→ MongoDB users collection
→ MongoDB Hindi/English collections
→ Students_Enrollment.csv
→ people/{roll}{name}/ directory

Image Capture
→ Browser camera
→ Canvas capture
→ Base64 encode
→ API endpoint
→ Decode & save as JPEG

Model Training
→ Load images from people/
→ FaceNet embeddings
→ Train neural network
→ Save model file

Attendance Marking
→ Camera frame
→ Face detection
→ Face embedding
→ Model prediction
→ MongoDB update
→ Real-time display
```

## Performance Considerations

- **Image Capture**: 300ms interval (10 seconds for 30 images)
- **Recognition**: 2-second intervals (prevents overload)
- **Model Training**: 30-40 seconds (depends on student count)
- **API Response**: <500ms for most endpoints
- **Database Queries**: Indexed for fast retrieval

## Browser Compatibility

- ✅ Chrome/Edge (Recommended)
- ✅ Firefox
- ✅ Safari (iOS 11+)
- ⚠️ Requires HTTPS for camera access (except localhost)

## Mobile Support

- ✅ Responsive design
- ✅ Touch-friendly buttons
- ✅ Camera access on mobile browsers
- ✅ Works on iOS and Android

---

**Built with modern web technologies for seamless user experience!**

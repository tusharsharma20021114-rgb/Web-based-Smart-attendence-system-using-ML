# **Web-based Smart Attendance System Using Machine Learning**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13-orange.svg)](https://www.tensorflow.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3-green.svg)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Latest-green.svg)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent, automated attendance system leveraging facial recognition technology to eliminate manual attendance tracking. Built with Python, OpenCV, and deep learning, this system achieves approximately 85% accuracy under optimal lighting conditions.

**Author:** Tushar Sharma  
**Repository:** [tusharsharma20021114-rgb/Web-based-Smart-attendence-system-using-ML](https://github.com/tusharsharma20021114-rgb/Web-based-Smart-attendence-system-using-ML)

---

## **✨ Features**

- 🎯 Real-time face detection and recognition using OpenCV and Haar Cascade
- 🧠 Deep learning model with FaceNet embeddings for accurate face recognition
- 💾 MongoDB integration for persistent data storage
- 📚 Multi-subject support (easily extensible)
- 📸 Automated student enrollment with image capture
- 📊 CSV export functionality for attendance records
- 🖥️ Multiple UI options: Desktop GUI (Tkinter) and Web Interface (Flask)
- 🌐 RESTful API for third-party integrations
- 📈 Progress tracking for model training
- 🎨 Modern, responsive design with enhanced styling
- 📉 Real-time statistics dashboard

## **🛠️ Technology Stack**

- **Backend:** Python 3.x, Flask
- **Computer Vision:** OpenCV, Haar Cascade Classifier
- **Deep Learning:** Keras/TensorFlow, FaceNet
- **Database:** MongoDB, Pymongo
- **Frontend:** HTML5, CSS3, JavaScript
- **Desktop GUI:** Tkinter
- **Data Processing:** Pandas, NumPy
- **API:** Flask-CORS

## **📋 Prerequisites**

**System Requirements:**
- Python 3.7 or higher
- MongoDB 4.0+ (running on localhost:27017)
- Webcam
- 4GB RAM minimum (8GB recommended)

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

For GPU acceleration:
```bash
pip install -r Requirements/GPU_Req.txt
```

## **🚀 Installation & Setup**

### Local Development

1. **Clone the repository:**
```bash
git clone https://github.com/tusharsharma20021114-rgb/Web-based-Smart-attendence-system-using-ML.git
cd Web-based-Smart-attendence-system-using-ML
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Start MongoDB:**
```bash
sudo systemctl start mongodb
# OR
mongod
```

4. **Run the web application:**
```bash
python3 app.py
# Access at http://localhost:5000
```

### Alternative Interfaces

**Desktop GUI (Original):**
```bash
python3 UI.py
```

**Modern Desktop GUI:**
```bash
python3 UI_modern.py
```

**REST API Only:**
```bash
python3 api.py
```

### Cloud Deployment

Deploy to Render, Railway, or Heroku with one click!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

**Quick Deploy to Render:**
1. Fork this repository
2. Create account on [render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Deploy automatically!

Your app will be live at: `https://your-app-name.onrender.com`

## **📖 Usage Guide**

### Web Application (Recommended)

1. **Access Dashboard**
   - Navigate to http://localhost:5000
   - View real-time statistics
   - Quick access to all features

2. **Enroll Students** (`/enroll`)
   - Enter roll number and name
   - Click "Save Student"
   - Click "Start Camera" to begin image capture
   - Click "Capture Images" to take 30 training photos
   - Images saved automatically

3. **Train Model** (from Dashboard)
   - Click "Train Model" action card
   - Wait 30-40 seconds for training
   - Model saves automatically

4. **Mark Attendance** (`/attendance`)
   - Select subject (Hindi/English)
   - Click "Start Recognition"
   - System recognizes faces in real-time
   - Recognized students appear in the list
   - Click "Save Attendance" to confirm

5. **View Records** (`/records`)
   - Switch between Hindi/English tabs
   - Search and filter records
   - Sort by any column
   - Export to CSV

## **🏗️ Project Structure**

```
├── app.py                     # Main Flask web application ⭐
├── api.py                     # REST API server (standalone)
├── config.py                  # Configuration settings
├── UI.py                      # Original Tkinter GUI
├── UI_modern.py              # Modern styled Tkinter GUI
├── Generate_Dataset.py        # Student enrollment & image capture
├── Model_train.py            # Model training script
├── Recognizer.py             # Face recognition & attendance
├── embedding.py              # FaceNet embedding extraction
├── templates/                # HTML templates
│   ├── base.html            # Base template with navbar
│   ├── dashboard.html       # Main dashboard
│   ├── enroll.html          # Student enrollment page
│   ├── attendance.html      # Attendance marking page
│   └── records.html         # View records page
├── static/                   # Frontend assets
│   ├── css/style.css        # Modern CSS styling
│   └── js/main.js           # JavaScript utilities
├── FaceDetection/            # Face detection module
├── Model/                    # Trained models
├── Model_architecture/       # Neural network architecture
├── MongoDB/                  # Database operations
├── PreTrained_model/        # FaceNet pre-trained model
├── people/                  # Student image datasets
├── *_attendance/            # Attendance records (CSV)
├── Procfile                 # Heroku deployment
├── render.yaml              # Render deployment
├── vercel.json              # Vercel deployment
└── requirements.txt         # Python dependencies
```

## **🧠 Model Architecture**

**Neural Network Design:**
```
Input Layer:    128 neurons (FaceNet embeddings)
Hidden Layer 1: 64 neurons + LeakyReLU
Hidden Layer 2: 32 neurons + LeakyReLU  
Hidden Layer 3: 16 neurons + LeakyReLU
Output Layer:   n_classes + Softmax
```

**Training Configuration:**
- Optimizer: Adam (lr=0.01)
- Epochs: 400
- Batch Size: 16
- Loss: Categorical Crossentropy

**Recognition Pipeline:**
1. Face Detection → Haar Cascade
2. Face Extraction → Resize to 160x160
3. Embedding Generation → FaceNet (128-dim)
4. Classification → Custom Neural Network
5. Confidence Check → Threshold 0.85
6. Attendance Update → MongoDB + CSV

## **🌐 API Endpoints**

### Base URL: `http://localhost:5000/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/students` | Get all students |
| POST | `/students` | Enroll new student |
| GET | `/attendance/{subject}` | Get attendance records |
| GET | `/attendance/{subject}/export` | Export as CSV |
| GET | `/stats` | Get statistics |
| GET | `/subjects` | List all subjects |

Full documentation: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## **🎯 Key Features Explained**

### Face Detection
- OpenCV Haar Cascade classifier for real-time detection
- Multi-face detection support
- Optimized for various lighting conditions

### Face Recognition
- Pre-trained FaceNet model (128-dimensional embeddings)
- Custom classifier for student identification
- 85% confidence threshold
- Duplicate prevention per session

### Database Management
- MongoDB with separate collections per subject
- Automatic CSV backup
- Real-time updates
- Easy data export

## **⚠️ Limitations & Known Issues**

- Accuracy depends on lighting conditions
- Sequential roll number enrollment required
- Currently supports 2 subjects (extensible)
- No model regularization (suitable for small datasets)

## **🔮 Future Enhancements**

**Completed:**
- ✅ Web-based interface
- ✅ REST API integration
- ✅ Modern UI styling
- ✅ Real-time dashboard

**Planned:**
- 📱 Mobile app integration
- 📧 Email notifications
- 📊 Advanced analytics with charts
- 🔐 Authentication & authorization
- 🌍 Multi-language support
- 📅 Date-range reports
- 🖼️ Student photo gallery
- 📤 Excel export
- 🎨 Theme customization

## **📚 Documentation**

- [API Documentation](API_DOCUMENTATION.md) - Complete REST API reference
- [Setup Guide](SETUP.md) - Detailed installation instructions
- [Deployment Guide](DEPLOYMENT.md) - Cloud deployment instructions ⭐
- [Contributing Guidelines](CONTRIBUTING.md) - How to contribute

## **🤝 Contributing**

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add: AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## **📄 License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## **👨‍💻 Author**

**Tushar Sharma**  
GitHub: [@tusharsharma20021114-rgb](https://github.com/tusharsharma20021114-rgb)  
Repository: [Web-based-Smart-attendence-system-using-ML](https://github.com/tusharsharma20021114-rgb/Web-based-Smart-attendence-system-using-ML)

## **🙏 Acknowledgments**

- FaceNet model for face embeddings
- OpenCV community for computer vision tools
- MongoDB for database solutions
- Flask framework for web development
- TensorFlow/Keras for deep learning

## **💬 Support**

If you find this project helpful, please ⭐ star the repository!

For issues and questions: [GitHub Issues](https://github.com/tusharsharma20021114-rgb/Web-based-Smart-attendence-system-using-ML/issues)

---

**Built with ❤️ by Tushar Sharma | Demonstrating ML & Computer Vision in Real-world Applications**

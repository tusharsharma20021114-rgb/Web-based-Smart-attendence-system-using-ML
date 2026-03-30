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

- 🔐 **User Authentication** - Secure login and registration system
- 👤 **Student Self-Registration** - Students can create accounts and enroll themselves
- 📸 **Webcam Integration** - Capture training images directly from browser
- 🎯 **Real-time Face Recognition** - Mark attendance using AI-powered face detection
- 🧠 **Deep Learning Model** - FaceNet embeddings with custom neural network
- � **MongoDB Database** - Persistent storage for users and attendance
- � **Multi-Subject Support** t- Hindi and English (easily extensible)
- 📊 **Statistics Dashboard** - Real-time attendance analytics
- � **CSV Export** - Download attendance records
- 🎨 **Modern UI** - Responsive design with smooth animations
- 🌐 **REST API** - Complete API for all operations
- 👨‍� **Role-Based Access** - Admin and student roles with different permissions

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

### Run Locally (5 Minutes)

1. **Clone & Install:**
```bash
git clone https://github.com/tusharsharma20021114-rgb/Web-based-Smart-attendence-system-using-ML.git
cd Web-based-Smart-attendence-system-using-ML
pip install -r requirements.txt
```

2. **Start MongoDB:**
```bash
sudo systemctl start mongodb
```

3. **Run App:**
```bash
python3 app.py
```

4. **Access:** http://localhost:5000
   - Login: `admin@admin.com` / `admin123`

### 🌐 Deploy LIVE Online (FREE)

**Want your app accessible from anywhere? Deploy it in 10 minutes!**

📖 **Complete Guide:** [DEPLOY_LIVE.md](DEPLOY_LIVE.md)

**Quick Deploy to Render:**
1. Setup MongoDB Atlas (free)
2. Go to render.com
3. Connect your GitHub repo
4. Add MongoDB connection string
5. Deploy!

**Your app will be live at:** `https://your-app.onrender.com`

Anyone can access it, register, and use the system! 🎉

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

### For Students

1. **Register Account**
   - Go to http://localhost:5000
   - Click "Register as Student"
   - Enter your name, email, roll number, and password
   - Click "Register"

2. **Upload Training Images**
   - Login with your credentials
   - Go to "Upload Images" page
   - Click "Start Camera"
   - Click "Capture Images" (30 images will be taken automatically)
   - Images saved to your profile

3. **Mark Attendance**
   - Go to "Mark Attendance" page
   - Select subject (Hindi/English)
   - Click "Start Recognition"
   - Look at the camera
   - Attendance marked automatically when face is recognized!

4. **View Your Records**
   - Go to "Records" page
   - See your attendance for all subjects
   - Track your attendance percentage

### For Admin

1. **Login**
   - Email: `admin@admin.com`
   - Password: `admin123`

2. **Train Model**
   - After students upload images
   - Click "Train Model" from dashboard
   - Wait 30-40 seconds
   - Model ready for recognition!

3. **View All Records**
   - Access all student attendance
   - Export to CSV
   - View statistics

### API Usage

All features accessible via REST API:

```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@admin.com","password":"admin123"}'

# Get students
curl http://localhost:5000/api/students

# Get attendance
curl http://localhost:5000/api/attendance/hindi

# Get statistics
curl http://localhost:5000/api/stats
```

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference.

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

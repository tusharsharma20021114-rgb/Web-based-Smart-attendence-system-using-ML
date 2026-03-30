# 🚀 Quick Start Guide

## Complete Web Application with Authentication

### Local Setup (5 Minutes)

**Step 1: Clone & Install**
```bash
git clone https://github.com/tusharsharma20021114-rgb/Web-based-Smart-attendence-system-using-ML.git
cd Web-based-Smart-attendence-system-using-ML
pip install -r requirements.txt
```

**Step 2: Start MongoDB**
```bash
sudo systemctl start mongodb
```

**Step 3: Run Application**
```bash
python3 app.py
```

**Step 4: Access Web App**
Open browser: **http://localhost:5000**

**Step 5: Login**
- Email: `admin@admin.com`
- Password: `admin123`

## 🌐 Deploy Online (Free - 10 Minutes)

### Deploy to Render

1. **Setup MongoDB Atlas** (2 min)
   - Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
   - Create free account
   - Create free cluster
   - Click "Connect" → "Connect your application"
   - Copy connection string
   - Replace `<password>` with your password
   - Whitelist all IPs: Network Access → Add IP → 0.0.0.0/0

2. **Deploy to Render** (5 min)
   - Go to [render.com](https://render.com)
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Connect your repository
   - Settings:
     - Name: `smart-attendance`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
   - Add Environment Variable:
     - Key: `MONGO_URI`
     - Value: Your MongoDB Atlas connection string
   - Click "Create Web Service"

3. **Wait for deployment** (3 min)
   - Render builds and deploys automatically
   - You'll get a URL like: `https://smart-attendance.onrender.com`

4. **Access your live app!** 🎉
   - Open the URL
   - Login with admin credentials
   - Start using!

## 📱 How It Works

### For Students:
1. **Register** → Create account with roll number
2. **Upload Images** → Capture 30 face images via webcam
3. **Mark Attendance** → Use face recognition to mark attendance
4. **View Records** → Check your attendance anytime

### For Admin:
1. **Login** → Use admin credentials
2. **Train Model** → After students upload images
3. **View All Records** → See all student attendance
4. **Export Data** → Download CSV reports

## ⚡ Key Features

✅ Students register themselves  
✅ Webcam captures training images  
✅ AI recognizes faces automatically  
✅ Attendance marked in real-time  
✅ Works on phone, tablet, desktop  
✅ Secure authentication  
✅ MongoDB cloud database  
✅ Export to CSV  

## 🆘 Troubleshooting

**Camera not working?**
- Use HTTPS (required for camera access)
- Allow camera permissions in browser
- Use Chrome or Edge browser

**MongoDB connection failed?**
- Check if MongoDB is running
- Verify connection string
- Check network access in Atlas

**Models not loading?**
- Train the model first (admin only)
- Ensure students have uploaded images
- Check if facenet_keras.h5 exists

## 📞 Need Help?

Open an issue: [GitHub Issues](https://github.com/tusharsharma20021114-rgb/Web-based-Smart-attendence-system-using-ML/issues)

**Your app is ready to deploy! 🚀**

# Deployment Guide

## Web Application Deployment

This guide covers deploying the Smart Attendance System to various cloud platforms.

## 🚀 Quick Deploy Options

### Option 1: Render (Recommended)

1. **Create account** at [render.com](https://render.com)

2. **Create MongoDB Atlas** (free tier):
   - Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
   - Create free cluster
   - Get connection string
   - Whitelist all IPs (0.0.0.0/0)

3. **Deploy on Render**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Settings:
     - Name: `smart-attendance-system`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
   - Add Environment Variable:
     - Key: `MONGO_URI`
     - Value: Your MongoDB Atlas connection string
   - Click "Create Web Service"

4. **Access your app**: `https://smart-attendance-system.onrender.com`

### Option 2: Railway

1. **Create account** at [railway.app](https://railway.app)

2. **Deploy**:
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python and deploys
   - Add MongoDB plugin from Railway marketplace

3. **Configure**:
   - Add environment variables if needed
   - Railway provides automatic HTTPS

### Option 3: Heroku

1. **Install Heroku CLI**:
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Login and create app**:
```bash
heroku login
heroku create smart-attendance-system
```

3. **Add MongoDB**:
```bash
heroku addons:create mongolab:sandbox
```

4. **Deploy**:
```bash
git push heroku main
heroku open
```

### Option 4: Local Network Deployment

For deployment on local network (accessible by other devices):

```bash
# Install dependencies
pip install -r requirements.txt

# Run with public access
python3 app.py
```

Access from other devices: `http://YOUR_LOCAL_IP:5000`

## 📋 Pre-Deployment Checklist

- [ ] MongoDB connection string configured
- [ ] Pre-trained models uploaded (facenet_keras.h5)
- [ ] Haar Cascade XML file present
- [ ] Environment variables set
- [ ] Dependencies in requirements.txt
- [ ] Debug mode disabled for production

## 🔧 Configuration

### Environment Variables

Create `.env` file:
```env
MONGO_URI=mongodb://localhost:27017/
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

### Production Settings

In `config.py`, set:
```python
API_DEBUG = False
```

## 🌐 GitHub Pages (Static Demo)

For a static demo without backend:

1. Create `docs/` folder
2. Copy `templates/` and `static/` to `docs/`
3. Rename `dashboard.html` to `index.html`
4. Enable GitHub Pages in repository settings
5. Select `docs/` folder as source

**Note**: This will be a frontend-only demo without actual face recognition.

## 🐳 Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

Build and run:
```bash
docker build -t smart-attendance .
docker run -p 5000:5000 smart-attendance
```

## ⚠️ Important Notes

### Camera Access
- HTTPS required for camera access in browsers
- Use ngrok for local testing with HTTPS
- Most cloud platforms provide automatic HTTPS

### Model Files
- Large model files (>100MB) cannot be pushed to GitHub
- Use Git LFS or download separately
- Store in cloud storage (S3, Google Cloud Storage)

### MongoDB
- Don't use localhost in production
- Use MongoDB Atlas (free tier available)
- Enable authentication
- Whitelist deployment server IPs

### Performance
- Use gunicorn with multiple workers
- Enable caching for static files
- Consider CDN for assets
- Optimize model loading

## 🔒 Security Recommendations

1. **Add authentication** before deploying publicly
2. **Use environment variables** for sensitive data
3. **Enable CORS** only for trusted domains
4. **Validate all inputs** on server side
5. **Use HTTPS** in production
6. **Rate limit** API endpoints
7. **Sanitize file uploads**

## 📊 Monitoring

Add monitoring tools:
- Sentry for error tracking
- New Relic for performance
- LogDNA for logs
- UptimeRobot for uptime monitoring

## 🆘 Troubleshooting

**Issue**: Models not loading
- **Solution**: Ensure model files are present and paths are correct

**Issue**: MongoDB connection failed
- **Solution**: Check connection string and network access

**Issue**: Camera not working
- **Solution**: Ensure HTTPS is enabled

**Issue**: High memory usage
- **Solution**: Reduce worker count, optimize model loading

## 📞 Support

For deployment issues, open an issue on GitHub:
https://github.com/tusharsharma20021114-rgb/Web-based-Smart-attendence-system-using-ML/issues

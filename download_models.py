"""
Download pretrained models on first startup
Author: Tushar Sharma
"""

import os
import urllib.request
import sys

def download_file(url, destination):
    """Download file with progress"""
    print(f"Downloading {destination}...")
    
    def progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent = min(downloaded * 100 / total_size, 100)
        sys.stdout.write(f"\rProgress: {percent:.1f}%")
        sys.stdout.flush()
    
    try:
        urllib.request.urlretrieve(url, destination, progress)
        print(f"\n✅ Downloaded {destination}")
        return True
    except Exception as e:
        print(f"\n❌ Error downloading: {e}")
        return False

def ensure_models():
    """Ensure all required model files exist"""
    
    # Create directories
    os.makedirs('PreTrained_model', exist_ok=True)
    os.makedirs('Model', exist_ok=True)
    os.makedirs('FaceDetection', exist_ok=True)
    
    # FaceNet model (89MB)
    facenet_path = 'PreTrained_model/facenet_keras.h5'
    if not os.path.exists(facenet_path):
        print("FaceNet model not found. Downloading...")
        # Using a public mirror of the FaceNet Keras model
        url = "https://github.com/nyoki-mtl/keras-facenet/releases/download/v0.2/facenet_keras.h5"
        if not download_file(url, facenet_path):
            print("⚠️  Failed to download FaceNet model")
            print("Please download manually from:")
            print("https://drive.google.com/uc?export=download&id=1PZ_6Zsy1Vb0s0JmjEmVd8FS99zoMCiN1")
            return False
    else:
        print(f"✅ FaceNet model exists: {facenet_path}")
    
    # Face cascade (should be in repo)
    cascade_path = 'FaceDetection/faces.xml'
    if not os.path.exists(cascade_path):
        print("⚠️  Face cascade not found")
        # Try to use OpenCV's built-in cascade
        import cv2
        cascade_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        if os.path.exists(cascade_file):
            import shutil
            shutil.copy(cascade_file, cascade_path)
            print(f"✅ Copied face cascade from OpenCV")
        else:
            print("❌ Face cascade not available")
            return False
    else:
        print(f"✅ Face cascade exists: {cascade_path}")
    
    return True

if __name__ == '__main__':
    print("🔧 Checking model files...")
    if ensure_models():
        print("✅ All models ready!")
        sys.exit(0)
    else:
        print("❌ Model setup failed")
        sys.exit(1)

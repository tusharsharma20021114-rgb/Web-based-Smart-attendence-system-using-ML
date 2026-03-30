"""
FaceNet Embedding Extractor
Author: Tushar Sharma
Description: Extract 128-dimensional face embeddings using pre-trained FaceNet
"""

from keras.models import load_model
import warnings
warnings.filterwarnings("ignore")

class emb:
    def __init__(self):
        self.model=load_model('PreTrained_model/facenet_keras.h5')
        
    def calculate(self,img):
        return self.model.predict(img)[0]

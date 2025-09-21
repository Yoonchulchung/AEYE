import tensorflow as tf
import numpy as np
import cv2


class AEYE_Inference():
    
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError("AEYE_Inference is not initialized yet")
        return cls._instance
    
    def __init__(self, weight_path, dataset_name):
        
        self.weight_path = weight_path
        self.dataset_name = dataset_name
        
        self.model = tf.keras.models.load_model(weight_path)

        if dataset_name=='Srinivasan2014':
            self.classes=['AMD', 'DME','NORMAL']
        else:
            self.classes = ['CNV', 'DME','DRUSEN','NORMAL']
        
    
    def inference(self, img):
        img = _image_preprocessing(img)

        predictions = self.model.predict(img)
        predicted_class = np.argmax(predictions, axis=-1)

        return predicted_class
        

def _image_preprocessing(img):
    img = cv2.resize(img,(224,224))
    img = np.reshape(img,[1,224,224,3])
    img = 1.0*img/255

    return img
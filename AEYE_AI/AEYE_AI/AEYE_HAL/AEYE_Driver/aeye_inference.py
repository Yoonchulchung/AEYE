import tensorflow as tf
import numpy as np
import cv2
import requests

url_log='http://127.0.0.1:2000/mw/status'

# status == active or error
def print_log(status, message) :
    data = {
        'whoami' : 'AI Inference',
        'status' : status, 
        'message' : message
        }
    requests.post(url_log, data=data)


def aeye_inference(img_path : str, weight_path : str, dataset_name : str):

    #tf.compat.v1.disable_v2_behavior()

    model = tf.keras.models.load_model(weight_path)
    print_log('active', "Succeed to load model.")

    if dataset_name=='Srinivasan2014':
        classes=['AMD', 'DME','NORMAL']
    else:
        classes = ['CNV', 'DME','DRUSEN','NORMAL']

    # convert image size to 224 x 224
    processsed_img = image_preprocessing(img_path)

    print_log('active', "Intiate Prediction")
    predictions = model.predict(img_path)

    predicted_class = np.argmax(predictions, axis=-1)

    print_log('active', "Predicted class : {}".format(predicted_class))
    return predicted_class

def image_preprocessing(img):
    img = cv2.imread(img)
    img = cv2.resize(img,(224,224))
    img = np.reshape(img,[1,224,224,3])
    img = 1.0*img/255

    return img
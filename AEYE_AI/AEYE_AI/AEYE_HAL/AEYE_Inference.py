from flask import jsonify, request, Blueprint
from werkzeug.utils import secure_filename
from datetime import datetime
from colorama import Fore, Back, Style
import tempfile
import os
from AEYE_HAL.AEYE_Driver import aeye_inference as inference

hal_ai_inference = Blueprint('AEYE_HAL_AI_Inference', __name__)



import logging
logging.basicConfig(level=logging.INFO)

def print_log(status, whoami, api, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    if status == "active" :
        logging.info("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to: " + Fore.BLUE + "[ " + api + " ]\n" +  Fore.RESET +
              Fore.GREEN + "[active] " + Fore.RESET + "message: [ " + Fore.GREEN + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        logging.info("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to:" + Fore.BLUE + "[ " + api + " ]\n" +  Fore.RESET +
              Fore.RED + "[error] " + Fore.RESET + "message: [ " + Fore.RED + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
        

UPLOAD_FOLDER = 'tmp_chunk'

inference_hal = 'OpticNet HAL - Inference'
@hal_ai_inference.route('/hal/ai-inference/', methods = ['POST'])
def aeye_ai_inference() :
    whoami      = request.form.get('whoami')

    # Read Data From local
    
    # Read Weight file
    weight_file_name='Srinivasan2014.h5'
    weight_file_path=os.path.join(UPLOAD_FOLDER, weight_file_name)  
    
    img_file_name='CNV-1569-1.jpeg'
    img_file_path=os.path.join(UPLOAD_FOLDER, img_file_name)

    print_log('active', whoami, inference_hal, 'Initiate AI Inference')  
    response = aeye_ai_inference_reqeuest(whoami, img_file_path, weight_file_path)

    print_log('active', whoami, inference_hal, 'Succeed AI Inference, response : {}'
                                                                                .format(response))  
    return response, 200



def check_valid_data(whoami, image_file, weight_file):
    
    if whoami: 
        if weight_file:
            if image_file:
                return 200
            else:
                print_log('error', whoami, inference_hal, ' Not Received Image File: {}'
                                                                                    .format(image_file))
                return 400
        else: 
            print_log('error', whoami, inference_hal, ' Not Received Weight File: {}'.format(weight_file))
            return 400
    else:
        print_log('error', whoami, inference_hal, ' Not Received whoami: {}'.format(whoami))
        return 400


def aeye_ai_inference_reqeuest(whoami, image_file_path, weight_file_path):
    
    if image_file_path:

        if weight_file_path:
            
            response = inference.aeye_inference(image_file_path, weight_file_path, 'Srinivasan2014')
            return response

        else:
            print_log('error', whoami, inference_hal, 'No Image file path')
            return jsonify({"error": "Invalid operation"}), 400

    else:
        print_log('error', whoami, inference_hal, 'No Weight file path.')
        return jsonify({"error": "Invalid operation"}), 400


def aeye_create_buffer(whoami, image_file, weight_file):
    with tempfile.NamedTemporaryFile(delete=False) as temp_image_file:
        temp_image_file.write(image_file.read())
        temp_image_file_path = temp_image_file.name

    with tempfile.NamedTemporaryFile(delete=False) as temp_weight_file :
        temp_weight_file.write(weight_file.read())
        temp_weight_file_path = temp_weight_file.name
        
    
    if temp_image_file_path and temp_weight_file_path:
        print_log('active', whoami, inference_hal, "Created Temporary Path : {}, {}"
                                            .format(temp_image_file_path, temp_weight_file_path))
    else:
        print_log('error', whoami, inference_hal, "Failed to Create Temporary Path : {}, {}"
                                            .format(temp_image_file_path, temp_weight_file_path))
    

    return temp_image_file_path, temp_weight_file_path

def aeye_delete_buffer(whoami, file_name, tmp_file_path):
    try:
        os.remove(tmp_file_path)
        print_log('active', whoami, inference_hal, "Deleted Temporary File : {}"
                                                                    .format(file_name))
    except OSError as e:
        print("Error: {}".format(e.strerror))
        print_log('active', whoami, inference_hal, "Deleted Temporary File : {}"
                                                                    .format(file_name))
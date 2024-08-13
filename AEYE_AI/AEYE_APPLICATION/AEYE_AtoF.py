from flask import jsonify, request, Blueprint
from colorama import Fore, Back, Style
from werkzeug.utils import secure_filename
from datetime import datetime
import requests
import io
import os
import hashlib

api_AtoF = Blueprint('application_layer_AtoF', __name__)

UPLOAD_FOLDER = 'tmp_chunk'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


import logging
logging.basicConfig(level=logging.INFO)

def print_log(status, whoami, api, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    if status == "active" :
        logging.info("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to: " + Fore.BLUE + "[ " + api + " ]\n" +  Fore.RESET +
              Fore.GREEN + "[OpticNet - active] " + Fore.RESET + "message: [ " + Fore.GREEN + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        logging.info("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to:" + Fore.BLUE + "[ " + api + " ]\n" +  Fore.RESET +
              Fore.RED + "[OpticNet - error] " + Fore.RESET + "message: [ " + Fore.RED + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")

i_am_AtoF='AEYE OpticNet API AtoF'

@api_AtoF.route('/api/data-assemble/', methods = ['POST'])
def aeye_ai_upload_file_in_chunk():

    whoami            = request.form.get('whoami')
    message           = request.form.get('message')
    file_name         = request.form.get('file_name')
    total_chunk_index = int(request.form.get('total_chunk_index'))
    total_chunk_hash  = request.form.get('total_chunk_hash')
    
    # Assemble File
    valid_data=valid(whoami, message, file_name, total_chunk_index, total_chunk_hash)
    
    if valid_data:
        with open(os.path.join(UPLOAD_FOLDER, file_name), 'wb') as final_file:
            for i in range(total_chunk_index):
                chunk_file_path = os.path.join(UPLOAD_FOLDER, "{}.part{}".format(file_name, i))
                with open(chunk_file_path, 'rb') as chunk_file:
                    final_file.write(chunk_file.read())
                os.remove(chunk_file_path)
        
        # Check File is not missed
        with open(os.path.join(UPLOAD_FOLDER, file_name), 'rb') as final_file:
            if calculate_hash(final_file.read()) != total_chunk_hash:
                message='File hash mismatch'
                data={
                    'whoami' : i_am_AtoF,
                    'message': message
                }
                return jsonify(data), 400
        
        data={
            'whoami' : i_am_AtoF,
            'message': "succed to assemble file"
        }
        return jsonify(data), 200
    else:
        data={
            'whoami' : i_am_AtoF,
            'message': "received invalid data"
        }
        return jsonify(data), 400    
    
    
def calculate_hash(data)->hashlib:
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()

def valid(whoami : str, message : str, file_name : str, totatl_chunk_index : int, total_chunk_hash)->bool:
    
    if whoami:
        if message:
            if file_name:
                if totatl_chunk_index:
                    if total_chunk_hash:
                        return True
                    else:
                        return False
                else:
                    return False
            return False
        return False
    return False
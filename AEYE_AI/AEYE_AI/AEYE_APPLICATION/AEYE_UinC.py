from flask import jsonify, request, Blueprint
from colorama import Fore, Back, Style
from werkzeug.utils import secure_filename
from datetime import datetime
import requests
import io
import os
import hashlib

api_UinC = Blueprint('application_layer_UinC', __name__)

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
              Fore.GREEN + "[active] " + Fore.RESET + "message: [ " + Fore.GREEN + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        logging.info("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to:" + Fore.BLUE + "[ " + api + " ]\n" +  Fore.RESET +
              Fore.RED + "[error] " + Fore.RESET + "message: [ " + Fore.RED + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")

i_am_uinc='AEYE OpticNet API UinC'

@api_UinC.route('/api/upload-file-chunk/', methods = ['POST'])
def aeye_ai_upload_file_in_chunk() :

    whoami      = request.form.get('whoami')
    message     = request.form.get('message')
    chunk_hash  = request.form.get('chunk_hash')
    chunk_index = int(request.form.get('chunk_index'))
    
    file        = request.files.get('file')
    
    # validate chunk hash
    chunk_data = file.read()
    if calculate_hash(chunk_data) != chunk_hash:
        print_message='chunk has is mismatch'
        print_log('error', i_am_uinc, i_am_uinc, print_message)
        data = {
            'whoami' : i_am_uinc,
            'message': chunk_data
        }
        return jsonify(data), 400
    
    # save chunk
    chunk_file_path=os.path.join(UPLOAD_FOLDER, '{}.part{}'.format(file.filename, chunk_index))
    with open(chunk_file_path, 'wb') as chunk_file:
        chunk_file.write(chunk_data)
    
    message='chunk upload succeed'
    data={
        'whoami' : i_am_uinc,
        'message': message
    }
    return jsonify(data), 200


def calculate_hash(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()


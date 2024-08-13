from flask import jsonify, request, Blueprint
from colorama import Fore, Back, Style
from werkzeug.utils import secure_filename
from datetime import datetime
import requests
import io
import os

api_UCTC = Blueprint('application_layer_UCTC', __name__)

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
   

i_am_uctc = 'OpticNet - API UCTC'

@api_UCTC.route('/api/start-upload-file/', methods = ['POST'])
def aeye_upload_check_tcp_connection() :

    whoami    = request.form.get('whoami')
    message   = request.form.get('message')
    file_name = request.form.get('file_name')
    file_size = request.form.get('file_size')
    file_hash = request.form.get('file_hash')

    if whoami:
        if message:
            if file_name:
                if file_size:
                    if file_hash:
                    
                        print_log('active', whoami, i_am_uctc, "{} received valid from {}".format(whoami, i_am_uctc))
                        whoami ='AEYE OpticNet API UCTC'
                        message='AEYE OpticNet is alive' 
                        data={
                            'whoami' : whoami,
                            'message': message
                        }
                        return jsonify(data), 200
                    else:
                        print_log('error', whoami, i_am_uctc, "{} missed to send file_hash. ".format(whoami))
                        whoami ='AEYE OpticNet API UCTC'
                        message='AEYE OpticNet is alive, but failed to send file_hash' 
                        data={
                            'whoami' : whoami,
                            'message': message
                        }
                        return jsonify(data), 400
                else:
                    print_log('error', whoami, i_am_uctc, "{} missed to send file_size.".format(whoami))
                    whoami ='AEYE OpticNet API UCTC'
                    message='AEYE OpticNet is alive, but failed to send file_size' 
                    data={
                        'whoami' : whoami,
                        'message': message
                    }
                    return jsonify(data), 400
            else:
                print_log('error', whoami, i_am_uctc, "{} missed to send file_name.".format(whoami))
                whoami ='AEYE OpticNet API UCTC'
                message='AEYE OpticNet is alive, but failed to send file_name' 
                data={
                        'whoami' : whoami,
                        'message': message
                    }
                return jsonify(data), 400
        else:
            print_log('error', whoami, i_am_uctc, "{} missed to send message.".format(whoami))
            whoami ='AEYE OpticNet API UCTC'
            message='AEYE OpticNet is alive, but failed to send message' 
            data={
                    'whoami' : whoami,
                    'message': message
                }
            return jsonify(data), 400    
    else:
        print_log('error', whoami, i_am_uctc, "{} missed to send whoami. recieved : {}".format(whoami, request.data))
        whoami ='AEYE OpticNet API UCTC'
        message='AEYE OpticNet is alive, but failed to send whoami' 
        data={
                'whoami' : whoami,
                'message': message
            }
        return jsonify(data), 400   
    

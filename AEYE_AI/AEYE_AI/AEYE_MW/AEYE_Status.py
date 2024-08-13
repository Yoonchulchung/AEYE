from flask import jsonify, request, Blueprint
from datetime import datetime
from colorama import Fore, Back, Style

mw_status = Blueprint('AEYE_MW_Status', __name__)
i_am_mw_status = 'OpticNet MW - Status'

import logging
logging.basicConfig(level=logging.INFO)

def print_log(status, whoami, mw, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    if status == "active" :
        logging.info("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to: " + Fore.BLUE + "[ " + mw + " ]\n" +  Fore.RESET +
              Fore.GREEN + "[active] " + Fore.RESET + "message: [ " + Fore.GREEN + str(message) +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        logging.info("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to:" + Fore.BLUE + "[ " + mw + " ]\n" +  Fore.RESET +
              Fore.RED + "[error] " + Fore.RESET + "message: [ " + Fore.RED + str(message) +" ]" + Fore.RESET +
              "\n-----------------------------------------")
        
@mw_status.route('/mw/status', methods = ['POST'])
def aeye_mw_status() :

    i_am_client    = request.form.get('whoami')
    status_client  = request.form.get('status')
    message_client = request.form.get('message')

    print_log('active', i_am_client, i_am_mw_status, message_client)

    return jsonify({'Status' :"good"}), 200



def check_valid_data(whoami, status, message) :

    if whoami :
        if status:
            if message :
                return 200
            else :
                print_log('error', whoami, mw_status, "Failed to Receive message")
                return 400
        else:
            print_log('error', whoami, mw_status, "Failed to Receive status")
            return 400
    else:
        print_log('error', 'Client', mw_status, "Failed to Receive whoami")
        return 400

from flask import jsonify, request, Blueprint
from datetime import datetime
from colorama import Fore, Back, Style

hal_ai_status = Blueprint('AEYE_HAL_AI_Status', __name__)
i_am_hal_status = 'OpticNet HAL - Status'

def print_log(status, whoami, message, hal) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if status == "active" :
        print("\n-----------------------------------------\n"   + 
              current_time + " " + whoami + " Request to : " + Fore.BLUE + "[ " + hal + " ]\n" +  Fore.RESET +
              Fore.GREEN + "[active] " + Fore.RESET + "message: [ " + Fore.GREEN + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        print("\n-----------------------------------------\n"   + 
              current_time + " " + whoami + "Request to : " + Fore.BLUE + "[ " + hal + " ]\n" +  Fore.RESET +
              Fore.RED + "[error] " + Fore.RESET + "message: [ " + Fore.RED + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
        
@hal_ai_status.route('/hal/ai-status', methods = ['POST'])
def hal_ai_status() :

    i_am_client  = request.form.get('whoami')
    status_client  = request.form.get('status')
    message_client = request.form.get('message')

    validate = check_valid_data(i_am_client, status_client, message_client)

    if validate == 200:
        print_log('active', i_am_client, message_client, i_am_hal_status)
        return 200
    else:
        return 400




def check_valid_data(whoami, status, message) :

    if whoami :
        if status:
            if message :
                return 200
            else :
                print_log('error', whoami, "Failed to Receive message", i_am_hal_status)
                return 400
        else:
            print_log('error', whoami, "Failed to Receive status", i_am_hal_status)
            return 400
    else:
        print_log('error', 'Client', "Failed to Receive whoami", i_am_hal_status)
        return 400

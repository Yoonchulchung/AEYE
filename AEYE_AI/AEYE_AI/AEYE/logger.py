from datetime import datetime
from colorama import Fore, Back, Style

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
        
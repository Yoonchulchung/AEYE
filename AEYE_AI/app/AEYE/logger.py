from datetime import datetime
from colorama import Fore, Back, Style

import logging
logging.basicConfig(level=logging.INFO)


import logging

logger = logging.getLogger("AEYE")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter("[AEYE %(asctime)s] %(message)s")
console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)
    
    
def AEYE_log(*message: str):
    msg = " ".join(str(m) for m in message)
    logger.info(msg)
    
# def print_log(status) :
#     now = datetime.now()
#     current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
#     if status == "active" :
#         logging.info("\n-----------------------------------------\n"   + 
#               current_time + " [ " + whoami + " ] send to: " + Fore.BLUE + "[ " + mw + " ]\n" +  Fore.RESET +
#               Fore.GREEN + "[active] " + Fore.RESET + "message: [ " + Fore.GREEN + str(message) +" ]" + Fore.RESET +
#               "\n-----------------------------------------")
#     elif status == "error" :
#         logging.info("\n-----------------------------------------\n"   + 
#               current_time + " [ " + whoami + " ] send to:" + Fore.BLUE + "[ " + mw + " ]\n" +  Fore.RESET +
#               Fore.RED + "[error] " + Fore.RESET + "message: [ " + Fore.RED + str(message) +" ]" + Fore.RESET +
#               "\n-----------------------------------------")
        
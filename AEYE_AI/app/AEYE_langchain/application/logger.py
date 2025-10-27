import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("AEYE_LC")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter("[AEYE_LC %(asctime)s] %(message)s")
console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)
    
    
def AEYE_LC_log(*message: str):
    msg = " ".join(str(m) for m in message)
    logger.info(msg)
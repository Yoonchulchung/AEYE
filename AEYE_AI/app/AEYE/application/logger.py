import logging

logging.basicConfig(level=logging.INFO)

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
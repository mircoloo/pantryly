from bcrypt import checkpw, hashpw, gensalt
from app.core.config import config
import logging
logger = logging.getLogger(__name__)

class HashHelper(object):
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        logger.info(f"{plain_password=} {hashed_password=} {checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))}")
        if checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8")):
            return True
        return False
    
    @staticmethod
    def get_password_hash(plain_password: str):
        return hashpw(plain_password.encode("utf-8"),
                      gensalt()).decode("utf-8")
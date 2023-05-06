from . import langllamaSetup, chatTempl, openaiSetup
import logging
logger = logging.getLogger(__name__)

def setup_chatgpt():
    print("ChatGPT set up")

import secrets

class SecretKeyGenerator:
    @staticmethod
    def generate_secret_key():
        return secrets.token_hex(32)
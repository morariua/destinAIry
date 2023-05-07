import logging
logger = logging.getLogger(__name__)

import secrets
class SecretKeyGenerator:
    @staticmethod
    def generate_secret_key():
        return secrets.token_hex(32)
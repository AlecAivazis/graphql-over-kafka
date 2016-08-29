# external imports
import jwt
# local imports
from .token_encryption_algorithm import token_encryption_algorithm

def generate_session_token(secret_key, **payload):
    """
        This function generates a session token signed by the secret key which
        can be used to extract the user credentials in a verifiable way.
    """
    return jwt.encode(payload, secret_key, algorithm=token_encryption_algorithm()).decode('utf-8')
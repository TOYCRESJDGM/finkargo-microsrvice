import base64
import pytz
from jose import jwt, JWTError
from typing import Annotated
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from src.utils.logger import logger

from src.utils.settings import (JWT_KEY, JWT_ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

secret = JWT_KEY.encode()  # Password Encode Secret Key Before Password Encrypt
salt_key = b"finkargo"*8

def get_fenec():
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32, salt=salt_key, iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret))
    return Fernet(key)

def encrypt_password(password):
    f = get_fenec()
    token = f.encrypt(bytes(password, encoding='utf-8'))
    return token.decode()

def decrypt_password(tek):
    f = get_fenec()
    return f.decrypt(bytes(tek, encoding='utf-8')).decode()

def create_acces_token(id: str, name: int, expires: timedelta):
    encode = { "sub": str(id), "username": name }
    expires_time = datetime.now(pytz.utc) + expires
    encode.update({'exp': expires_time})
    return jwt.encode(encode, JWT_KEY, algorithm=JWT_ALGORITHM)

def decode_token(token):
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=JWT_ALGORITHM)
        return payload
    except JWTError as e:
        error_type = type(e).__name__
        error_description = str(e)
        logger.error(f"Error durante la decodificación del token: {error_type} - {error_description}")
        return None

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = decode_token(token)
        username: str = payload.get('username')
        user_id: int = payload.get('sub')
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail='Autenticated neded') 
        return { 'username' : username, 'id': user_id}
    except Exception:
        raise HTTPException(status_code=401, detail='Autenticated error')


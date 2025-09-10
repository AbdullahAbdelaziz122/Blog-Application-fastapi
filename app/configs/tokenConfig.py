from pydantic_settings import BaseSettings
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Optional
from .. import schemas

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

setting = Settings()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a JWT access token.

    Args:
        data (dict): The payload data to encode into the token.
        expires_delta (Optional[timedelta]): Optional expiration time delta for the token.

    Returns:
        str: The encoded JWT access token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)

    
    to_encode.update({'exp': int(expire.timestamp())})

    encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
    
    return encoded_jwt




def verifyToken(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
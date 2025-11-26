import uuid
from http.client import HTTPException

import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from .config import settings



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_uuid():
    return str(uuid.uuid4())

def hash_password(password: str) -> str:
    # Bcrypt solo acepta los primeros 72 bytes
    pw_bytes = password.encode("utf-8")
    if len(pw_bytes) > 72:
        pw_bytes = pw_bytes[:72]

    # Ahora pw_bytes es seguro
    truncated_pw = pw_bytes.decode("utf-8", errors="ignore")
    return pwd_context.hash(truncated_pw)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pw_bytes = plain_password.encode("utf-8")
    if len(pw_bytes) > 72:
        pw_bytes = pw_bytes[:72]

    truncated_pw = pw_bytes.decode("utf-8", errors="ignore")
    return pwd_context.verify(truncated_pw, hashed_password)

def verify_token(token: str):
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token ha expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from .utils import decode_token
from .database import SessionLocal
from .models import User


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
        authorization: str = Header(default=None),
        db: Session = Depends(get_db)
):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    try:
        scheme, token = authorization.split()
    except:
        raise HTTPException(status_code=401, detail="Invalid auth header format")

    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid token scheme")

    payload = decode_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("sub")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

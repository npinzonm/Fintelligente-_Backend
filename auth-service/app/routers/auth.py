import app
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas, utils

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    exists = db.query(models.User).filter(models.User.email == user.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        id=utils.generate_uuid(),
        name=user.name,
        email=user.email,
        password_hash=utils.hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


@router.post("/login")
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()

    if not user or not utils.verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Token compatible con get_current_user
    token = utils.create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }




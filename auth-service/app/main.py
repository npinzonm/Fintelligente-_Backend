from fastapi import FastAPI, Depends
from .routers import auth
from .database import Base, engine
from .dependencies import get_current_user
from .models import User

app = FastAPI(
    title="Fintelligente - Auth Service",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

@app.get("/me")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }

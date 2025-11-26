import httpx
from fastapi import HTTPException, Header

AUTH_URL = "https://auth-service.onrender.com/me"

async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    async with httpx.AsyncClient() as client:
        resp = await client.get(AUTH_URL, headers={"Authorization": authorization})

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="Invalid token")

    return resp.json()  # {id, name, email}
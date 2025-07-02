from fastapi import HTTPException, Security, WebSocket
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

security = HTTPBearer()

# Hàm xác thực JWT cho REST API
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id, "token": credentials.credentials}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Hàm xác thực JWT cho WebSocket
async def get_current_user_ws(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return {"user_id": user_id, "token": token}
    except JWTError:
        return None

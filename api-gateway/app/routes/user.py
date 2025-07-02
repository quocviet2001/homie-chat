from fastapi import APIRouter, Depends, HTTPException
from app.middlewares.auth import get_current_user
import httpx
import os

router = APIRouter(prefix="/users", tags=["Users"])

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")

# Hàm chuyển tiếp yêu cầu đến User Service
async def forward_request(method: str, path: str, **kwargs):
    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(f"{USER_SERVICE_URL}/{path}", **kwargs)
            elif method == "POST":
                response = await client.post(f"{USER_SERVICE_URL}/{path}", **kwargs)
            elif method == "PUT":
                response = await client.put(f"{USER_SERVICE_URL}/{path}", **kwargs)
            elif method == "DELETE":
                response = await client.delete(f"{USER_SERVICE_URL}/{path}", **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.text
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# = Các API =

@router.post("/register")
async def register(data: dict):
    return await forward_request("POST", "register", json=data)

@router.post("/login")
async def login(data: dict):
    return await forward_request("POST", "login", json=data)

@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    return await forward_request(
        "POST", "logout",
        headers={"Authorization": f"Bearer {current_user['token']}"}
    )

@router.get("/")
async def get_user(current_user: dict = Depends(get_current_user)):
    return await forward_request(
        "GET", "user",
        headers={"Authorization": f"Bearer {current_user['token']}"}
    )

@router.put("/")
async def update_user(data: dict, current_user: dict = Depends(get_current_user)):
    return await forward_request(
        "PUT", "user",
        json=data,
        headers={"Authorization": f"Bearer {current_user['token']}"}
    )

@router.get("/friends")
async def get_friends(current_user: dict = Depends(get_current_user)):
    return await forward_request(
        "GET", "friends",
        headers={"Authorization": f"Bearer {current_user['token']}"}
    )

@router.get("/friends/search")
async def search_friends(query: str, current_user: dict = Depends(get_current_user)):
    return await forward_request(
        "GET", "friends/search",
        params={"query": query},
        headers={"Authorization": f"Bearer {current_user['token']}"}
    )

@router.post("/friend-requests")
async def send_friend_request(data: dict, current_user: dict = Depends(get_current_user)):
    return await forward_request(
        "POST", "friend-requests",
        json=data,
        headers={"Authorization": f"Bearer {current_user['token']}"}
    )

@router.get("/friend-requests")
async def get_friend_requests(current_user: dict = Depends(get_current_user)):
    return await forward_request(
        "GET", "friend-requests",
        headers={"Authorization": f"Bearer {current_user['token']}"}
    )

@router.put("/friend-requests")
async def respond_friend_request(data: dict, current_user: dict = Depends(get_current_user)):
    return await forward_request(
        "PUT", "friend-requests",
        json=data,
        headers={"Authorization": f"Bearer {current_user['token']}"}
    )
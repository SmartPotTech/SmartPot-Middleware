from fastapi import FastAPI, Request
import requests

app = FastAPI()

SPRING_BOOT_API_URL = "https://api-smartpot.onrender.com"
LOGIN_URL = f"{SPRING_BOOT_API_URL}/auth/login"
DATA_URL = f"{SPRING_BOOT_API_URL}/User/All"

@app.post("/login")
async def login(request: Request):
    credentials = await request.json()
    response = requests.post(LOGIN_URL, json=credentials)
    if response.status_code == 200:
        token = response.json()["token"]
        return {"token": token}
    else:
        return {"error": "Authentication failed"}, 401

@app.get("/get_data")
async def get_data(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        return {"error": "No token provided"}, 403
    headers = {"Authorization": token}
    response = requests.get(DATA_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve data"}, response.status_code

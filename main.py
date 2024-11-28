from fastapi import FastAPI, Request
import requests
import json
from pydantic import BaseModel
app = FastAPI()

SPRING_BOOT_API_URL = "http://api-smartpot.onrender.com"
LOGIN_URL = f"{SPRING_BOOT_API_URL}/auth/login"
DATA_URL = f"{SPRING_BOOT_API_URL}/User/All"

# Modelo de las credenciales
class LoginCredentials(BaseModel):
    email: str
    password: str

@app.post("/login")
async def login(credentials: LoginCredentials):
    payload = json.dumps({
        "email": "juan.perez@example.com",
        "password": "Contraseña1"
    })
    headers = {
        'User-Agent': 'SmartPot-Middleware/1.0.0 (https://smartpot-middleware.onrender.com)',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", LOGIN_URL, headers=headers, data=payload)
    return response.text

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

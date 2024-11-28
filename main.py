from fastapi import FastAPI, Request
import requests
import json
from pydantic import BaseModel

app = FastAPI()

SPRING_BOOT_API_URL = "http://api-smartpot.onrender.com"
LOGIN_URL = f"{SPRING_BOOT_API_URL}/auth/login"
DATA_URL = f"{SPRING_BOOT_API_URL}/User/All"


# Definir un modelo para las credenciales que recibirá el endpoint
class LoginCredentials(BaseModel):
    email: str
    password: str


@app.post("/login")
async def login(credentials: LoginCredentials):
    # Convertir las credenciales en el formato adecuado para la petición
    payload = json.dumps({
        "email": credentials.email,
        "password": credentials.password
    })

    headers = {
        'User-Agent': 'SmartPot-Middleware/1.0.0 (https://smartpot-middleware.onrender.com)',
        'Content-Type': 'application/json'
    }

    # Realizar la solicitud al servicio de login con las credenciales proporcionadas
    response = requests.post(LOGIN_URL, headers=headers, data=payload)

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

from fastapi import FastAPI, Request
import requests
import xmltodict
from fastapi.responses import JSONResponse

current_jwt = None

app = FastAPI()

API_URL = "https://api-smartpot.onrender.com/"

@app.post("/login")
async def login(request: Request):
    """
    Recibe las credenciales en formato XML, hace la solicitud a la API
    para obtener el JWT y lo guarda para sesiones posteriores.
    """
    global current_jwt

    body = await request.body()
    try:
        data = xmltodict.parse(body)
        credentials = data.get('credentials', {})

        username = credentials.get('username')
        password = credentials.get('password')

        if not username or not password:
            return JSONResponse(status_code=400, content={"message": "Missing credentials"})

        auth_url = f"{API_URL}auth/login"
        auth_payload = {
            "username": username,
            "password": password
        }
        auth_response = requests.post(auth_url, json=auth_payload)

        if auth_response.status_code != 200:
            return JSONResponse(status_code=auth_response.status_code, content={"message": "Authentication failed"})

        current_jwt = auth_response.json().get("token")

        if not current_jwt:
            return JSONResponse(status_code=400, content={"message": "JWT not found in the response"})

        return JSONResponse(status_code=200, content={"message": "JWT obtained successfully", "token": current_jwt})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error parsing credentials or fetching JWT", "error": str(e)})

@app.get("/users")
async def get_all_users():
    """
    Hace una solicitud GET a la API con el JWT almacenado para obtener los usuarios.
    """
    global current_jwt

    if not current_jwt:
        return JSONResponse(status_code=400, content={"message": "JWT not available"})

    headers = {
        "Authorization": f"Bearer {current_jwt}"
    }

    try:
        users_url = f"{API_URL}Users/All"
        response = requests.get(users_url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return JSONResponse(status_code=response.status_code, content={"message": "Failed to fetch users", "error": response.text})

    except requests.RequestException as e:
        return JSONResponse(status_code=500, content={"message": "Error fetching users", "error": str(e)})


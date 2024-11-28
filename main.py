import requests
import xmltodict
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
app = FastAPI()

API_URL = "https://api-smartpot.onrender.com/"

@app.post("/login")
async def login(request: Request):
    """
    Recibe las credenciales en formato XML, hace la solicitud a la API
    para obtener el JWT y lo guarda para sesiones posteriores.
    """

    body = await request.body()
    try:
        data = xmltodict.parse(body)
        credentials = data.get('credentials', {})

        email = credentials.get('email')
        password = credentials.get('password')

        if not email or not password:
            return JSONResponse(status_code=400, content={"message": "Missing credentials"})

        auth_url = f"{API_URL}auth/login"
        auth_payload = {
            "email": email,
            "password": password
        }
        auth_response = requests.post(auth_url, json=auth_payload)

        if auth_response.status_code != 200:
            return JSONResponse(status_code=auth_response.status_code, content={"message": "Authentication failed"})

        current_jwt = auth_response.text

        if not current_jwt:
            return JSONResponse(status_code=400, content={"message": "JWT not found in the response"})

        return JSONResponse(status_code=200, content={"message": "Login successful", "token": current_jwt})

    except Exception as e:
        return JSONResponse(status_code=500,
                            content={"message": "Error parsing credentials or fetching JWT. "+str(e)})

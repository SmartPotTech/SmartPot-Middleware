import requests
import xml.etree.ElementTree as Et
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

API_URL = "https://api-smartpot.onrender.com/"


def validate_jwt_format(token):
    """Valida que el JWT tenga el formato correcto."""
    parts = token.split('.')
    if len(parts) == 3:
        print("Formato JWT válido")
        return True
    else:
        print("Formato JWT inválido")
        return False


@app.post("/login")
async def login(request: Request):
    """
    Recibe las credenciales en formato XML, hace la solicitud a la API
    para obtener el JWT.
    """
    try:
        body = await request.body()
        data = Et.fromstring(body.decode('utf-8'))

        email = data.findtext('email')
        password = data.findtext('password')

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

        if not validate_jwt_format(current_jwt):
            return JSONResponse(status_code=400, content={"message": "Incorrect JWT in the response. " + current_jwt})

        return JSONResponse(status_code=200, content={"message": "Login successful", "token": current_jwt})

    except Et.ParseError as e:
        return JSONResponse(status_code=400, content={"message": "Error parsing XML: " + str(e)})
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={"message": "Error parsing credentials or fetching JWT. " + str(e)})

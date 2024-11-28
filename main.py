from fastapi import FastAPI, Request
import requests
import xml.etree.ElementTree as Et

app = FastAPI()

SPRING_BOOT_API_URL = "http://api-smartpot.onrender.com"
LOGIN_URL = f"{SPRING_BOOT_API_URL}/auth/login"
DATA_URL = f"{SPRING_BOOT_API_URL}/User/All"


# Endpoint de login
@app.post("/login")
async def login(request: Request):
    # Leemos el cuerpo de la solicitud (XML) como texto
    xml_data = await request.body()

    # Parseamos el XML para convertirlo en un diccionario
    try:
        root = Et.fromstring(xml_data.decode('utf-8'))  # Decodificamos el byte string
        email = root.find('email').text
        password = root.find('password').text

        # Aquí puedes hacer la validación de las credenciales si es necesario
        payload = {
            "email": email,
            "password": password
        }

        # Realizamos la solicitud a LOGIN_URL
        headers = {
            'User-Agent': 'SmartPot-Middleware/1.0.0 (https://smartpot-middleware.onrender.com)',
            'Content-Type': 'application/json',  # Si la API de destino espera JSON
        }

        response = requests.post(LOGIN_URL, headers=headers, json=payload)

        # Regresamos la respuesta como texto
        return response.text

    except Et.ParseError as e:
        return {"error": "Invalid XML", "details": str(e)}

@app.get("/User/All")
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

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

def parse_xml_data(body):
    """Convierte el XML de los datos a un diccionario."""
    try:
        # Parseamos el cuerpo del XML
        data = Et.fromstring(body.decode('utf-8'))

        # Extraemos las medidas del registro
        record_data = {
            "temperature": float(data.findtext('record/temperature', 0)),
            "humidity_air": float(data.findtext('record/humidity_air', 0)),
            "brightness": float(data.findtext('record/brightness', 0)),
            "ph": float(data.findtext('record/ph', 0)),
            "tds": float(data.findtext('record/tds', 0)),
            "humidity_soil": float(data.findtext('record/humidity_soil', 0)),
            "crop_id": data.findtext('crop', ''),
            "token": data.findtext('token', '')
        }

        return record_data
    except Et.ParseError as e:
        raise ValueError(f"Error parsing XML: {str(e)}")


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

@app.post("/create_record")
async def create_record(request: Request):
    """
    Recibe los datos del registro de sensor en formato XML y los envía a la API.
    """
    try:
        body = await request.body()
        record_data = parse_xml_data(body)

        jwt_token = record_data.get('token')
        if not jwt_token or not validate_jwt_format(jwt_token):
            return JSONResponse(status_code=400, content={"message": "Invalid or missing JWT token"})

        measures = {
            "atmosphere": str(record_data["temperature"]),
            "brightness": str(record_data["brightness"]),
            "temperature": str(record_data["temperature"]),
            "ph": str(record_data["ph"]),
            "tds": str(record_data["tds"]),
            "humidity": str(record_data["humidity_air"])
        }

        data = {
            "measures": measures,
            "crop": record_data["crop_id"]
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {jwt_token}'
        }

        record_url = f"{API_URL}Records/Create"

        response = requests.post(record_url, json=data, headers=headers)

        if response.status_code == 201:
            return JSONResponse(status_code=201, content={"message": "Record created successfully", "data": response.json()})
        else:
            return JSONResponse(status_code=response.status_code, content={"message": "Error creating record", "details": response.text})

    except ValueError as ve:
        return JSONResponse(status_code=400, content={"message": str(ve)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Internal server error: " + str(e)})


import xml.etree.ElementTree as Et
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
from app.auth import validate_jwt
from app.utils import parse_xml_data
from app.api import login_api,create_record_api

app = FastAPI()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@app.post("/login")
async def manage_login(request: Request):
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

        auth_response = await login_api(email, password)

        if auth_response.status_code != 200:
            return JSONResponse(status_code=auth_response.status_code, content={"message": "Authentication failed"})

        current_jwt = auth_response.text

        if not current_jwt:
            return JSONResponse(status_code=400, content={"message": "JWT not found in the response"})

        if not validate_jwt(current_jwt):
            return JSONResponse(status_code=400, content={"message": "Incorrect JWT in the response. " + current_jwt})

        return JSONResponse(status_code=200, content={"message": "Login successful", "token": current_jwt})

    except Et.ParseError as e:
        return JSONResponse(status_code=400, content={"message": "Error parsing XML: " + str(e)})
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={"message": "Error parsing credentials or fetching JWT. " + str(e)})

@app.post("/create_record")
async def manage_create_record(request: Request):
    """
    Recibe los datos del registro de sensor en formato XML y los envía a la API.
    """
    try:
        body = await request.body()
        record_data = parse_xml_data(body)

        jwt_token = record_data.get('token')
        if not jwt_token or not validate_jwt(jwt_token):
            return JSONResponse(status_code=400, content={"message": "Invalid or missing JWT token"})

        response = await create_record_api(jwt_token, record_data)

        if response.status_code == 201:
            return JSONResponse(status_code=201, content={"message": "Record created successfully", "data": response.json()})
        else:
            return JSONResponse(status_code=response.status_code, content={"message": "Error creating record", "details": response.text})

    except ValueError as ve:
        return JSONResponse(status_code=400, content={"message": str(ve)})
    except Exception as e:
        logging.exception("Internal server error encountered during record creation.")
        return JSONResponse(status_code=500, content={"message": "Internal server error"})


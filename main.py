import json
import requests
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, Optional

# Variable global para almacenar el JWT
jwt_token: Optional[str] = None

# URL de la API externa
API_URL = "https://api-smartpot.onrender.com/"

# Endpoints de la API
LOGIN_ENDPOINT = "auth/login"
USERS_ENDPOINT = "Users/All"

# Inicialización de FastAPI
app = FastAPI()


# Función para realizar login y obtener el JWT
def obtener_jwt(usuario: str, contrasena: str) -> Optional[str]:
    login_url = f"{API_URL}{LOGIN_ENDPOINT}"
    payload = {
        "username": usuario,
        "password": contrasena
    }

    try:
        response = requests.post(login_url, json=payload)
        response.raise_for_status()  # Lanza una excepción si la respuesta es un error
        return response.json().get("jwt", "")
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud de login: {e}")
        return None


# Función para interactuar con la API de usuarios usando el JWT
def obtener_usuarios() -> Dict:
    if jwt_token is None:
        raise Exception("No hay JWT disponible.")

    usuarios_url = f"{API_URL}{USERS_ENDPOINT}"
    headers = {"Authorization": f"Bearer {jwt_token}"}

    try:
        response = requests.get(usuarios_url, headers=headers)
        response.raise_for_status()
        return response.json()  # Retorna los datos de los usuarios
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener usuarios: {e}")
        return {}


# WebSocket para recibir credenciales del IoT
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            # Recibir los datos de las credenciales del IoT
            data = await websocket.receive_text()

            try:
                credentials = json.loads(data)

                if "usuario" in credentials and "contrasena" in credentials:
                    usuario = credentials["usuario"]
                    contrasena = credentials["contrasena"]

                    # Obtener el JWT desde la API
                    global jwt_token
                    jwt_token = obtener_jwt(usuario, contrasena)

                    if jwt_token:
                        await websocket.send_text("Autenticación exitosa, JWT recibido.")
                    else:
                        await websocket.send_text("Error al obtener el JWT.")
                else:
                    await websocket.send_text("Datos inválidos: 'usuario' y 'contrasena' son requeridos.")

            except json.JSONDecodeError:
                await websocket.send_text("Error: datos JSON mal formateados.")

            # Lógica adicional para recibir instrucciones y realizar más solicitudes
            if jwt_token:
                usuarios = obtener_usuarios()
                await websocket.send_text(json.dumps(usuarios))

    except WebSocketDisconnect:
        print("El dispositivo IoT se desconectó.")

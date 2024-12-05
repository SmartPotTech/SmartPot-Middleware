import httpx
from app.settings import API_URL


async def fetch_data_from_api(url: str, payload: dict, headers: dict = None):
    """Función auxiliar para hacer solicitudes POST a la API externa."""
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        return response


async def login_api(email: str, password: str) -> httpx.Response:
    """Realiza la autenticación en la API externa y obtiene un JWT."""
    auth_url = f"{API_URL}auth/login"
    auth_payload = {
        "email": email,
        "password": password
    }

    response = await fetch_data_from_api(auth_url, auth_payload)
    return response


async def create_record_api(jwt_token: str, record_data: dict) -> httpx.Response:
    """Crea un registro de sensor en la API externa utilizando el JWT para autenticarse."""

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

    response = await fetch_data_from_api(record_url, data, headers)
    return response

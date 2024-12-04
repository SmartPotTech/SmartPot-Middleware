import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

if not API_URL:
    raise ValueError("La variable de entorno API_URL no está definida.")
if not SECRET_KEY:
    raise ValueError("La variable de entorno SECRET_KEY no está definida.")

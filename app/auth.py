import jwt
from jwt.exceptions import JWTException
from settings import SECRET_KEY

def validate_jwt(token):
    """Valida que el JWT tenga el formato correcto."""
    parts = token.split('.')
    if len(parts) == 3:
        print("Formato JWT válido")
        return True
    else:
        print("Formato JWT inválido")
        return False

'''
def validate_jwt(token: str) -> bool:
    """Valida el JWT verificando su firma y formato usando pyjwt."""
    try:
        decoded_token = jwt.jwt.e(token, SECRET_KEY, algorithms=["HS256"])
        print("JWT válido y decodificado:", decoded_token)
        return True
    except JWTException as e:
        print(f"Error en la validación del JWT: {str(e)}")
        return False
'''

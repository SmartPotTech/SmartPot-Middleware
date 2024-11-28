from fastapi import FastAPI, WebSocket, WebSocketDisconnect
app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Aceptar la conexión WebSocket

    try:
        while True:
            message = await websocket.receive_text()  # Recibir mensaje del cliente

            if message.lower() == "hola":
                await websocket.send_text("¡Hola, cómo estás?")  # Responder con saludo
            else:
                await websocket.send_text("Mensaje no reconocido.")
    except WebSocketDisconnect:
        print("Cliente desconectado.")

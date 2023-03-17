import models
from typing import List
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, Depends
from fastapi.responses import HTMLResponse
import json
import core.config as conf
import auth as auth_endpoint
from database import init_models, get_session
import asyncio
from fastapi_jwt_auth import AuthJWT


app = FastAPI()

app.include_router(auth_endpoint.router, tags=['Auth'], prefix='/auth')

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now();
            var token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJyZXQ3MDIwQGdtYWlsLmNvbSIsImlhdCI6MTY3OTA4ODYxNiwibmJmIjoxNjc5MDg4NjE2LCJqdGkiOiJmZGQ4MWY0Ny05NjI3LTQxMDUtYmUwMS05MzFhY2MyNjNlZTEiLCJleHAiOjE2NzkwODk1MTYsInR5cGUiOiJhY2Nlc3MiLCJmcmVzaCI6dHJ1ZX0.bMyTYXFaGftuis72ZNznw0A4_aJiUEdrkiam6_9OcJM";
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8080/ws/${client_id}?token=${token}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

class WebSocketParser:
    def __init__(self):
        pass


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int, token: str = Query(...), Authorize: AuthJWT = Depends()):
    print(token)
    Authorize.jwt_required("websocket", token=token)
    await manager.connect(websocket)
    try:
        while True:
            try:
                data = await websocket.receive_json()
                print(data)
                for i in range(10):
                    await manager.send_personal_message(f"Answer from server", websocket)
            except json.decoder.JSONDecodeError:
               await manager.send_personal_message(f"Unprocessable message", websocket)
            #await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Client disconnected")

        #await manager.broadcast(f"Client #{client_id} left the chat")

if __name__ == "__main__":
    # asyncio.run(init_models())
    uvicorn.run("server:app", port=conf.HTTP_PORT, host=conf.HTTP_HOST, reload=True, headers=[("server", "By @ret7020")])

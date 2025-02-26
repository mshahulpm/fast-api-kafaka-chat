from fastapi import FastAPI, WebSocket
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import json
import os

load_dotenv()

from connection_manager import ConnectionManager
from interface.index import ChatMessage

# from kafka.KafkaClient import KafkaClient


# Dictionary to store connected WebSocket clients
connected_users = {}
# queue_client = KafkaClient()
# conn_manager = ConnectionManager(queue_client)
conn_manager = ConnectionManager()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # can alter with time
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return FileResponse("index.html")


@app.post("/data")
def create_data(data: dict):
    return {"received": data}


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await conn_manager.connect(user_id, websocket)
    try:
        while True:
            data: ChatMessage = json.loads(await websocket.receive_text())
            await conn_manager.broadcast(data)
    except WebSocketDisconnect:
        conn_manager.disconnect(user_id)
        # await conn_manager.broadcast()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

# Run the server with Uvicorn
# Command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

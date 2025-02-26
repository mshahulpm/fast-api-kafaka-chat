from fastapi import WebSocket
from typing import Dict
import json
import threading

from interface.index import ChatMessage
from interface.QueueClient import QueueClient


class ConnectionManager:
    def __init__(self, queue_client: QueueClient = None):
        self.active_connections: Dict[str, WebSocket] = (
            {}
        )  # Stores user_id -> WebSocket
        # self._queue_client = queue_client
        # consumer_thread = threading.Thread(target=self._start_consumer, daemon=True)
        # consumer_thread.start()

    # def _start_consumer(self):
    #     """Starts Kafka consumer to listen for messages in the background."""
    #     self._queue_client.subscribe_to_queue(["group_chat"], self._queue_handler)

    # async def _queue_handler(self, msg: str, message_key: str):
    #     message: ChatMessage = json.loads(msg)
    #     await self.broadcast(message)

    async def connect(self, user_id: str, websocket: WebSocket):
        """Accepts the WebSocket connection and stores it by user_id."""
        await websocket.accept()
        self.active_connections[user_id] = websocket  # Store connection with user_id

    def disconnect(self, user_id: str):
        """Removes a user from the active connections dictionary."""
        self.active_connections.pop(user_id, None)  # Avoids KeyError

    async def send_personal_message(self, recipient_id: int, message: ChatMessage):
        """Sends a personal message to a specific user if they're connected."""
        websocket = self.active_connections.get(recipient_id)
        if websocket:
            await websocket.send_text(
                json.dumps(message)
            )  # Convert ChatMessage to JSON

    async def broadcast(self, message: ChatMessage):
        """Broadcasts a message to all connected users except the sender."""
        if message["recipient"] != "group":
            await self.send_personal_message(message["recipient"], message)
        else:
            for user_id, websocket in self.active_connections.items():
                if user_id != message["sender_id"]:  # Skip the sender
                    await websocket.send_text(json.dumps(message))  # Send JSON message

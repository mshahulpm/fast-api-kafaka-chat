from typing import TypedDict, Literal


class ChatMessage(TypedDict):
    type: Literal["chat"]
    sender_id: int
    sender_name: str
    recipient: str  # Can be "group" or a specific user
    message: str

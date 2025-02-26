from abc import ABC, abstractmethod
from typing import Callable


class QueueClient(ABC):

    @abstractmethod
    def publish_message(self, queue_name: str, message_key: str, message: str):
        pass

    def subscribe_to_queue(
        self, queue_names: list[str], message_handler: Callable[[str], None]
    ):
        """Subscribes to a queue and processes messages using the provided handler."""
        pass

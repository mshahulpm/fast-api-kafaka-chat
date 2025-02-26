from confluent_kafka import Producer, Consumer

from interface.QueueClient import QueueClient
from constants.index import KAFKA_CONFIG


class KafkaClient(QueueClient):
    def __init__(self):
        super().__init__()
        print(KAFKA_CONFIG)
        self._producer = Producer(KAFKA_CONFIG)
        self._consumer = Consumer(
            {**KAFKA_CONFIG, "group.id": "group-1", "auto.offset.reset": "earliest"}
        )

    def publish_message(self, topic, key, message):
        self._producer.produce(topic, key, message)

    def subscribe_to_queue(self, topics, message_handler):
        self._consumer.subscribe(topics)
        while True:
            msg = self._consumer.poll(1.0)
            if msg is not None and msg.error() is None:
                key = msg.key().decode("utf-8")
                message = msg.value().decode("utf-8")
                message_handler(message, key)

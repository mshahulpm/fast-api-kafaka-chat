import os

KAFKA_CONFIG = {
    "bootstrap.servers": os.getenv("bootstrap.servers"),
    "security.protocol": os.getenv("security.protocol"),
    "sasl.mechanisms": os.getenv("sasl.mechanisms"),
    "sasl.username": os.getenv("sasl.username"),
    "sasl.password": os.getenv("sasl.password"),
    "session.timeout.ms": os.getenv("session.timeout.ms"),
    "client.id": os.getenv("client.id"),
}

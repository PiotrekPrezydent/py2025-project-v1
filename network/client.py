import socket
import json
from network.config import load_config
import os

class NetworkClient:
    def __init__(self, config_path="../configs/client_config.yaml"):
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), config_path))
        config = load_config(config_path)
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 12345)
        self.timeout = config.get("timeout", 5.0)
        self.retries = config.get("retries", 3)
        self.sock = None

    def connect(self):
        self.sock = socket.create_connection((self.host, self.port), timeout=self.timeout)

    def send(self, data: dict) -> bool:
        message = json.dumps(data) + '\n'
        attempt = 0
        while attempt < self.retries:
            try:
                self.sock.sendall(message.encode('utf-8'))
                ack = b""
                while not ack.endswith(b'\n'):
                    chunk = self.sock.recv(1024)
                    if not chunk:
                        break
                    ack += chunk
                if ack.strip() == b"ACK":
                    return True
            except Exception as e:
                print(f"Error sending data: {e}")
            attempt += 1
        return False

    def close(self):
        if self.sock:
            self.sock.close()

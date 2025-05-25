import socket
import threading
import json
import sys
from network.config import load_config
import os
import logging

class NetworkServer:
    def __init__(self, config_path="../../configs/server_config.yaml"):
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), config_path))
        config = load_config(config_path)
        self.port = config.get("port", 12345)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(1.0)  # timeout 1 sekunda na accept
        self.logger = logging.getLogger('NetworkServer')
        self.logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(ch)
        self.running = False

    def start(self):
        try:
            self.sock.bind(("0.0.0.0", self.port))
            self.sock.listen()
            self.running = True
            self.logger.info(f"Serwer nasłuchuje na porcie {self.port}")

            while self.running:
                try:
                    client_socket, addr = self.sock.accept()
                    threading.Thread(target=self._handle_client, args=(client_socket, addr), daemon=True).start()
                except socket.timeout:
                    # Timeout do ponownego sprawdzenia flagi running
                    continue
        except KeyboardInterrupt:
            self.logger.info("Przerwano działanie serwera (Ctrl+C)")
        except Exception as e:
            self.logger.error(f"Błąd serwera: {e}")
        finally:
            self.sock.close()
            self.logger.info("Serwer zatrzymany")

    def stop(self):
        self.running = False

    def _handle_client(self, client_socket, addr):
        with client_socket:
            try:
                data = b""
                while not data.endswith(b"\n"):
                    part = client_socket.recv(1024)
                    if not part:
                        if not data:
                            self.logger.warning(f"Połączenie z {addr} zamknięte bez danych.")
                        else:
                            self.logger.warning(f"Połączenie z {addr} zakończone w trakcie przesyłania danych.")
                        return  # zakończ wątek klienta

                    data += part

                try:
                    message = json.loads(data.decode())
                except json.JSONDecodeError as e:
                    self.logger.error(f"Nieprawidłowy JSON od {addr}: {e}")
                    return

                print(f"[RECEIVED from {addr}]:")
                for k, v in message.items():
                    print(f"  {k}: {v}")

                client_socket.sendall(b"ACK\n")

            except Exception as e:
                self.logger.error(f"[ERROR] Błąd klienta {addr}: {e}")


import json
from .temperature_sensor import TemperatureSensor
from .humidity_sensor import HumiditySensor
from .pressure_sensor import PressureSensor
from .light_sensor import LightSensor
import datetime
from typing import Optional
from network.client import NetworkClient
from logger.logger import Logger

class SensorManager:
    SENSOR_TYPES = {
        "temperature": TemperatureSensor,
        "humidity": HumiditySensor,
        "pressure": PressureSensor,
        "light": LightSensor
    }

    def __init__(self, config_path: str, client: Optional[NetworkClient] = None):
        self.sensors = []
        self.client = client
        self.load_config(config_path)

    def load_config(self, path):
        with open(path, 'r', encoding="utf-8") as f:
            config = json.load(f)
        for sensor_data in config:
            sensor_type = sensor_data.get("type", "").lower()
            sensor_class = self.SENSOR_TYPES.get(sensor_type)
            if sensor_class:
                sensor = sensor_class(
                    sensor_id=sensor_data["id"],
                    name=sensor_data["name"],
                    unit=sensor_data["unit"],
                    min_value=sensor_data["min_value"],
                    max_value=sensor_data["max_value"],
                    frequency=sensor_data["frequency"],
                )
                self.sensors.append(sensor)
            else:
                print(f"Nieznany typ czujnika: {sensor_type}")

    def register_callbacks(self, logger: Logger):
        for sensor in self.sensors:
            sensor.register_callback(
                lambda timestamp, sensor_id, sensor_name, value, unit, logger=logger: 
                    logger.log_reading(timestamp, sensor_id,sensor_name, value, unit)
            )

    def start_all(self):
        for sensor in self.sensors:
            sensor.start()
            self._send("start_sensor", sensor.sensor_id, {"status": "started"})

    def stop_all(self):
        for sensor in self.sensors:
            sensor.stop()
            self._send("stop_sensor", sensor.sensor_id, {"status": "stopped"})

    def get_all_sensors(self):
        return self.sensors

    def get_sensor(self, sensor_id):
        for sensor in self.sensors:
            if sensor.sensor_id == sensor_id:
                return sensor
        return None

    def stop_sensor(self, sensor_id):
        for sensor in self.sensors:
            if sensor.sensor_id == sensor_id:
                sensor.stop()
                self._send("stop_sensor", sensor_id, {"status": "stopped"})
                break

    def start_sensor(self, sensor_id):
        for sensor in self.sensors:
            if sensor.sensor_id == sensor_id:
                sensor.start()
                self._send("start_sensor", sensor_id, {"status": "started"})
                break

    def log_sensor(self, sensor_id):
        for sensor in self.sensors:
            if sensor.sensor_id == sensor_id:
                message = str(sensor)
                print(message)
                self._send("log_sensor", sensor_id, {"data": message})

    def log_all_sensors(self):
        for sensor in self.sensors:
            message = str(sensor)
            print(message)
            self._send("log_sensor", sensor.sensor_id, {"data": message})

    def _send(self, action: str, sensor_id: Optional[str] = None, extra: Optional[dict] = None):
        if not self.client:
            return  # Nie wysyłamy, jeśli nie podano klienta

        message = {
            "type": "sensor_action",
            "timestamp": datetime.datetime.now().isoformat(),
            "action": action
        }
        if sensor_id:
            message["sensor_id"] = sensor_id
        if extra:
            message.update(extra)

        try:
            self.client.send(message)
        except Exception as e:
            print(f"❗ Błąd podczas wysyłania wiadomości: {e}")

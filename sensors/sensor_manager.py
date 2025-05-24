import json
from .temperature_sensor import TemperatureSensor
from .humidity_sensor import HumiditySensor
from .pressure_sensor import PressureSensor
from .light_sensor import LightSensor
import asyncio

class SensorManager:
    SENSOR_TYPES = {
        "temperature": TemperatureSensor,
        "humidity": HumiditySensor,
        "pressure": PressureSensor,
        "light": LightSensor
    }

    def __init__(self, config_path):
        self.sensors = []
        self.load_config(config_path)

    def load_config(self, path):
        with open(path, 'r',encoding="utf-8") as f:
            config = json.load(f)
        for sensor_data in config:
            sensor_type = sensor_data.get("type").lower()
            sensor_class = self.SENSOR_TYPES.get(sensor_type)
            if sensor_class:
                sensor = sensor_class(
                    sensor_id=sensor_data["id"],
                    name=sensor_data["name"],
                    unit=sensor_data["unit"],
                    min_value=sensor_data["min_value"],
                    max_value=sensor_data["max_value"],
                    frequency=sensor_data.get("frequency", 1)
                )
                self.sensors.append(sensor)
            else:
                print(f"Nieznany typ czujnika: {sensor_type}")

    def start_all(self):
        for sensor in self.sensors:
            sensor.start()

    def stop_all(self):
        for sensor in self.sensors:
            sensor.stop()

    def stop_sensor(self, sensor_id):
        for sensor in self.sensors:
            if sensor.sensor_id == sensor_id:
                sensor.stop()
                break

    def start_sensor(self, sensor_id):
        for sensor in self.sensors:
            if sensor.sensor_id == sensor_id:
                sensor.start()
                break

    def print_all_readings(self):
        for sensor in self.sensors:
            try:
                value = sensor.read_value()
                print(f"[{sensor.name}] {value} {sensor.unit}")
            except Exception as e:
                print(f"[{sensor.name}] Błąd: {e}")

    def log_sensors_data(self):
        logs = []
        for sensor in self.sensors:
            try:
                value = sensor.read_value()
                log_entry = {
                    "sensor_id": sensor.sensor_id,
                    "name": sensor.name,
                    "value": value,
                    "unit": sensor.unit
                }
                print(f"[{sensor.name}] {value} {sensor.unit}")
                logs.append(log_entry)
            except Exception as e:
                error_entry = {
                    "sensor_id": sensor.sensor_id,
                    "name": sensor.name,
                    "error": str(e)
                }
                print(f"Nie można odczytać {sensor.name}: {e}")
                logs.append(error_entry)
        return logs

    async def log_all_readings(self, interval=1):
        while True:
            print("\n--- Odczyty sensorów ---")
            for sensor in self.sensors:
                if sensor.active:
                    try:
                        value = sensor.read_value()
                        print(f"[{sensor.name}] {value} {sensor.unit}")
                    except Exception as e:
                        print(f"[{sensor.name}] Błąd: {e}")
            await asyncio.sleep(interval)
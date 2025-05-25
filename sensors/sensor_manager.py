import json
from .temperature_sensor import TemperatureSensor
from .humidity_sensor import HumiditySensor
from .pressure_sensor import PressureSensor
from .light_sensor import LightSensor
import datetime

class SensorManager:
    SENSOR_TYPES = {
        "temperature": TemperatureSensor,
        "humidity": HumiditySensor,
        "pressure": PressureSensor,
        "light": LightSensor
    }

    def __init__(self, config_path, logger=None):
        self.sensors = []
        self.logger = logger  # zapisujemy instancję loggera
        self.load_config(config_path)

    def load_config(self, path):
        with open(path, 'r', encoding="utf-8") as f:
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
                    frequency=sensor_data["frequency"],
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
                break

    def start_sensor(self, sensor_id):
        for sensor in self.sensors:
            if sensor.sensor_id == sensor_id:
                sensor.start()
                break

    def log_sensor(self, sensor_id):
        for sensor in self.sensors:
            if sensor.sensor_id == sensor_id:
                message = str(sensor)
                if self.logger:
                    self.logger.info(message)
                else:
                    print(message)
                break

    def log_all_sensors(self):
        for sensor in self.sensors:
            message = str(sensor)
            #print(message)
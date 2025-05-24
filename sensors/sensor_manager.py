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
        self._sensor_tasks = {}
        self._stop_event = asyncio.Event()

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
    def get_sensor_reading_by_id(self, sensor_id):
        for sensor in self.sensors:
            if sensor.sensor_id == sensor_id:
                return sensor.get_status()
        return None
    
    def get_all_readings(self):
        return [sensor.get_status() for sensor in self.sensors]
    
    def start_refresh_loop(self):
        self._stop_event.clear()
        for sensor in self.sensors:
            if sensor.sensor_id not in self._sensor_tasks or self._sensor_tasks[sensor.sensor_id].done():
                task = asyncio.create_task(self._sensor_loop(sensor))
                self._sensor_tasks[sensor.sensor_id] = task

    async def _sensor_loop(self, sensor):
        while not self._stop_event.is_set():
            if sensor.active:
                try:
                    sensor.read_value()
                except Exception:
                    pass
            await asyncio.sleep(sensor.frequency)

    async def stop_refresh_loop(self):
        self._stop_event.set()
        await asyncio.gather(*self._sensor_tasks.values(), return_exceptions=True)
        self._sensor_tasks.clear()

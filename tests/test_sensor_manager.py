import unittest
from unittest.mock import MagicMock, patch, mock_open
from sensors.sensor_manager import SensorManager
from sensors.temperature_sensor import TemperatureSensor
from sensors.humidity_sensor import HumiditySensor
import json

SAMPLE_CONFIG = json.dumps([
    {
        "id": 1,
        "name": "Temp1",
        "type": "temperature",
        "unit": "C",
        "min_value": -10,
        "max_value": 40,
        "frequency": 2
    },
    {
        "id": 2,
        "name": "Humidity1",
        "type": "humidity",
        "unit": "%",
        "min_value": 20,
        "max_value": 90,
        "frequency": 3
    }
])

class TestSensorManager(unittest.TestCase):
    def setUp(self):
        self.test_config = [
            {
                "id": "1",
                "type": "temperature",
                "name": "Czujnik temperatury",
                "unit": "°C",
                "min_value": -10,
                "max_value": 40,
                "frequency": 0.1
            },
            {
                "id": "2",
                "type": "humidity",
                "name": "Czujnik wilgotności",
                "unit": "%",
                "min_value": 10,
                "max_value": 90,
                "frequency": 0.2
            }
        ]
        self.config_path = "tests/temp_test_config.json"
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.test_config, f)

        self.manager = SensorManager(self.config_path)

    def test_load_config_loads_sensors(self):
        self.assertEqual(len(self.manager.sensors), 2)
        self.assertIsInstance(self.manager.sensors[0], TemperatureSensor)
        self.assertIsInstance(self.manager.sensors[1], HumiditySensor)

    def test_start_all_starts_all_sensors(self):
        for sensor in self.manager.sensors:
            sensor.start = MagicMock()
        self.manager.start_all()
        for sensor in self.manager.sensors:
            sensor.start.assert_called_once()

    def test_stop_all_stops_all_sensors(self):
        for sensor in self.manager.sensors:
            sensor.stop = MagicMock()
        self.manager.stop_all()
        for sensor in self.manager.sensors:
            sensor.stop.assert_called_once()

    def test_start_sensor_starts_specific_sensor(self):
        sensor = self.manager.sensors[0]
        sensor.start = MagicMock()
        self.manager.start_sensor(sensor.sensor_id)
        sensor.start.assert_called_once()

    def test_stop_sensor_stops_specific_sensor(self):
        sensor = self.manager.sensors[1]
        sensor.stop = MagicMock()
        self.manager.stop_sensor(sensor.sensor_id)
        sensor.stop.assert_called_once()

if __name__ == "__main__":
    unittest.main()

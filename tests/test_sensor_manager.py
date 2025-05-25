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

    @patch("builtins.open", new_callable=mock_open, read_data=SAMPLE_CONFIG)
    def setUp(self, mock_file):
        self.logger = MagicMock()
        self.manager = SensorManager("dummy_path.json", logger=self.logger)

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

    def test_log_sensor_uses_logger(self):
        sensor = self.manager.sensors[0]
        self.manager.log_sensor(sensor.sensor_id)
        self.logger.info.assert_called_with(str(sensor))

    def test_log_all_sensors_uses_logger(self):
        self.manager.log_all_sensors()
        calls = [unittest.mock.call(str(sensor)) for sensor in self.manager.sensors]
        self.logger.info.assert_has_calls(calls, any_order=True)

if __name__ == "__main__":
    unittest.main()

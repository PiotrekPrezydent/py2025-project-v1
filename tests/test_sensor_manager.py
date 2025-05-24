import unittest
import os
import json
import asyncio
from sensors.sensor_manager import SensorManager

class TestSensorManager(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Tworzenie tymczasowej konfiguracji sensorów
        self.test_config = [
            {
                "id": "1",
                "type": "temperature",
                "name": "Czujnik temperatury",
                "unit": "°C",
                "min_value": -10,
                "max_value": 40
            },
            {
                "id": "2",
                "type": "humidity",
                "name": "Czujnik wilgotności",
                "unit": "%",
                "min_value": 10,
                "max_value": 90
            }
        ]
        self.config_path = "tests/temp_test_config.json"
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.test_config, f)

        self.manager = SensorManager(self.config_path)

    def tearDown(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)

    def test_load_config(self):
        self.assertEqual(len(self.manager.sensors), 2)
        self.assertEqual(self.manager.sensors[0].name, "Czujnik temperatury")

    def test_start_and_stop_all(self):
        self.manager.stop_all()
        for sensor in self.manager.sensors:
            self.assertFalse(sensor.active)

        self.manager.start_all()
        for sensor in self.manager.sensors:
            self.assertTrue(sensor.active)

    def test_stop_and_start_sensor_by_id(self):
        self.manager.stop_sensor("1")
        self.assertFalse(self.manager.sensors[0].active)
        self.manager.start_sensor("1")
        self.assertTrue(self.manager.sensors[0].active)

    def test_get_sensor_reading_by_id(self):
        result = self.manager.get_sensor_reading_by_id("1")
        self.assertIn("sensor_id", result)
        self.assertEqual(result["sensor_id"], "1")
        self.assertTrue(result["active"])

    def test_get_all_readings(self):
        results = self.manager.get_all_readings()
        self.assertEqual(len(results), 2)
        for reading in results:
            self.assertIn("sensor_id", reading)

    async def test_refresh_loop_updates_sensor_values(self):
        sensor = self.manager.sensors[0]
        initial_value = sensor.last_value
        self.manager.start_refresh_loop(interval=0.1)
        await asyncio.sleep(0.3)
        await self.manager.stop_refresh_loop()
        self.assertIsNotNone(sensor.last_value)
        self.assertNotEqual(sensor.last_value, initial_value)


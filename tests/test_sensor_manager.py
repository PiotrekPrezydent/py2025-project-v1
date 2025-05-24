import unittest
import json
from sensors.sensor_manager import SensorManager

# Przykładowa konfiguracja sensorów w formacie JSON jako string
SENSORS_JSON = """
[
    {
        "id": "T1",
        "name": "Czujnik temperatury",
        "type": "temperature",
        "unit": "°C",
        "min_value": -10,
        "max_value": 35,
        "frequency": 2
    },
    {
        "id": "H1",
        "name": "Czujnik wilgotności",
        "type": "humidity",
        "unit": "%",
        "min_value": 20,
        "max_value": 90
    },
    {
        "id": "P1",
        "name": "Czujnik ciśnienia",
        "type": "pressure",
        "unit": "hPa",
        "min_value": 970,
        "max_value": 1030
    },
    {
        "id": "L1",
        "name": "Czujnik światła",
        "type": "light",
        "unit": "lx",
        "min_value": 0,
        "max_value": 10000
    }
]
"""

class TestSensorManager(unittest.TestCase):

    def setUp(self):
        # Zapisz JSON do pliku tymczasowego
        with open("test_sensors.json", "w", encoding="utf-8") as f:
            f.write(SENSORS_JSON)

        self.manager = SensorManager("test_sensors.json")

    def tearDown(self):
        import os
        os.remove("test_sensors.json")

    def test_load_sensors(self):
        self.assertEqual(len(self.manager.sensors), 4)
        self.assertTrue(any(s.name == "Czujnik temperatury" for s in self.manager.sensors))
        self.assertTrue(any(s.name == "Czujnik wilgotności" for s in self.manager.sensors))

    def test_start_stop_all(self):
        self.manager.stop_all()
        self.assertFalse(any(s.active for s in self.manager.sensors))
        self.manager.start_all()
        self.assertTrue(all(s.active for s in self.manager.sensors))

    def test_stop_single_sensor(self):
        sensor_id = self.manager.sensors[0].sensor_id
        self.manager.stop_sensor(sensor_id)
        sensor = next(s for s in self.manager.sensors if s.sensor_id == sensor_id)
        self.assertFalse(sensor.active)

    def test_log_sensors_data(self):
        self.manager.start_all()
        log = self.manager.log_sensors_data()
        self.assertIsInstance(log, list)
        for entry in log:
            self.assertIn("sensor_id", entry)
            self.assertIn("name", entry)
            self.assertTrue("value" in entry or "error" in entry)

if __name__ == "__main__":
    unittest.main()

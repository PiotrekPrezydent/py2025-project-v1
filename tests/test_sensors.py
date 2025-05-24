import unittest
from sensors.temperature_sensor import TemperatureSensor
from sensors.humidity_sensor import HumiditySensor
from sensors.pressure_sensor import PressureSensor
from sensors.light_sensor import LightSensor

class TestSensors(unittest.TestCase):
    def test_temperature_sensor(self):
        sensor = TemperatureSensor(1, "Czujnik temperatury", "°C", -20, 50)
        self.assertEqual(sensor.name, "Czujnik temperatury")
        self.assertTrue(sensor.active)
        val = sensor.read_value()
        self.assertIsInstance(val, float)
        self.assertGreaterEqual(val, -20)
        self.assertLessEqual(val, 50)
        sensor.stop()
        with self.assertRaises(Exception):
            sensor.read_value()

    def test_humidity_sensor(self):
        sensor = HumiditySensor(2, "Czujnik wilgotności", "%", 0, 100)
        self.assertEqual(sensor.unit, "%")
        val = sensor.read_value()
        self.assertIsInstance(val, float)
        self.assertGreaterEqual(val, 0)
        self.assertLessEqual(val, 100)
        sensor.stop()
        with self.assertRaises(Exception):
            sensor.read_value()

    def test_pressure_sensor(self):
        sensor = PressureSensor(3, "Czujnik ciśnienia", "hPa", 950, 1050)
        val = sensor.read_value()
        self.assertIsInstance(val, float)
        # Przyjmujemy mały margines, bo fluktuacje mogą wykraczać poza zakres
        self.assertGreater(val, 940)
        self.assertLess(val, 1060)
        sensor.stop()
        with self.assertRaises(Exception):
            sensor.read_value()

    def test_light_sensor(self):
        sensor = LightSensor(4, "Czujnik światła", "lx", 0, 10000)
        val = sensor.read_value()
        self.assertIsInstance(val, float)
        self.assertGreaterEqual(val, 0)
        self.assertLessEqual(val, 10000 + 200)  # z uwzględnieniem szumu
        sensor.stop()
        with self.assertRaises(Exception):
            sensor.read_value()

if __name__ == "__main__":
    unittest.main()

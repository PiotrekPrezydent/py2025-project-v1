import unittest
from sensors.sensor import Sensor
from sensors.temperature_sensor import TemperatureSensor
from sensors.humidity_sensor import HumiditySensor
from sensors.pressure_sensor import PressureSensor
from sensors.light_sensor import LightSensor

class TestSensorBase(unittest.TestCase):

    def setUp(self):
        self.sensor = Sensor(
            sensor_id="123",
            name="Testowy Sensor",
            unit="unit",
            min_value=0,
            max_value=100,
            frequency=1
        )

    def test_initialization(self):
        self.assertEqual(self.sensor.sensor_id, "123")
        self.assertEqual(self.sensor.name, "Testowy Sensor")
        self.assertEqual(self.sensor.unit, "unit")
        self.assertTrue(self.sensor.active)

    def test_read_value_within_range(self):
        value = self.sensor.read_value()
        self.assertGreaterEqual(value, self.sensor.min_value)
        self.assertLessEqual(value, self.sensor.max_value)
        self.assertEqual(self.sensor.last_value, value)

    def test_get_last_value_without_reading(self):
        value = self.sensor.get_last_value()
        self.assertIsNotNone(value)
        self.assertEqual(value, self.sensor.last_value)

    def test_get_last_value_after_manual_read(self):
        self.sensor.read_value()
        last = self.sensor.get_last_value()
        self.assertEqual(last, self.sensor.last_value)

    def test_calibration_modifies_value(self):
        self.sensor.read_value()
        original = self.sensor.last_value
        calibrated = self.sensor.calibrate(1.1)
        self.assertAlmostEqual(calibrated, original * 1.1, delta=0.001)

    def test_stop_and_start_sensor(self):
        self.sensor.stop()
        self.assertFalse(self.sensor.active)
        self.sensor.start()
        self.assertTrue(self.sensor.active)

    def test_read_value_when_inactive_raises_exception(self):
        self.sensor.stop()
        with self.assertRaises(Exception) as context:
            self.sensor.read_value()
        self.assertIn("jest wyłączony", str(context.exception))

    def test_get_status_active(self):
        self.sensor.read_value()
        status = self.sensor.get_status()
        self.assertTrue(status["active"])
        self.assertIn("value", status)

    def test_get_status_inactive(self):
        self.sensor.stop()
        status = self.sensor.get_status()
        self.assertFalse(status["active"])
        self.assertEqual(status["value"], "OFF")

    def test_string_representation(self):
        expected = "Sensor(id=123, name=Testowy Sensor, unit=unit)"
        self.assertEqual(str(self.sensor), expected)


class TestSensors(unittest.TestCase):

    def test_temperature_sensor(self):
        sensor = TemperatureSensor(1, "Czujnik temperatury", "°C", -20, 50)
        self.assertEqual(sensor.name, "Czujnik temperatury")
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
        self.assertLessEqual(val, 10200)  # uwzględniając szum
        sensor.stop()
        with self.assertRaises(Exception):
            sensor.read_value()

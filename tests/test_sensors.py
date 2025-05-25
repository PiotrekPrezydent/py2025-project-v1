import unittest
import asyncio
from unittest.mock import patch
from sensors.sensor import Sensor
from sensors.temperature_sensor import TemperatureSensor
from sensors.humidity_sensor import HumiditySensor
from sensors.pressure_sensor import PressureSensor
from sensors.light_sensor import LightSensor

class TestSensorBase(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.sensor = Sensor("1", "Generic", "unit", 0, 100, frequency=0.1)

    def test_read_value_raises_if_inactive(self):
        self.sensor.active = False
        with self.assertRaises(Exception) as cm:
            self.sensor.read_value()
        self.assertIn("wyłączony", str(cm.exception))

    async def test_start_and_stop_loop_calls_read_value(self):
        with patch.object(self.sensor, 'read_value', wraps=self.sensor.read_value) as mock_read:
            self.sensor.register_callback(lambda *_: None)
            self.sensor.start()
            # Czekamy 0.35s - powinno wykonać się co najmniej 3 razy (frequency=0.1s)
            await asyncio.sleep(0.35)
            self.sensor.stop()
            await asyncio.sleep(0.05)  # pozwól na wyczyszczenie tasku
            self.assertGreaterEqual(mock_read.call_count, 3)

class TestTemperatureSensor(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.sensor = TemperatureSensor("temp1", "Temp", "C", -10, 40, frequency=0.1)

    def test_read_value_raises_if_inactive(self):
        self.sensor.active = False
        with self.assertRaises(Exception):
            self.sensor.read_value()

    async def test_start_and_stop_loop_calls_read_value(self):
        with patch.object(self.sensor, 'read_value', wraps=self.sensor.read_value) as mock_read:
            self.sensor.register_callback(lambda *_: None)
            self.sensor.start()
            await asyncio.sleep(0.35)
            self.sensor.stop()
            await asyncio.sleep(0.05)
            self.assertGreaterEqual(mock_read.call_count, 3)
            # dodatkowo sprawdzamy zakres ostatniej wartości
            val = self.sensor.last_value
            self.assertIsInstance(val, float)
            self.assertGreaterEqual(val, -15)
            self.assertLessEqual(val, 45)

class TestHumiditySensor(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.sensor = HumiditySensor("hum1", "Humidity", "%", 30, 90, frequency=0.1)

    def test_read_value_raises_if_inactive(self):
        self.sensor.active = False
        with self.assertRaises(Exception):
            self.sensor.read_value()

    async def test_start_and_stop_loop_calls_read_value(self):
        with patch.object(self.sensor, 'read_value', wraps=self.sensor.read_value) as mock_read:
            self.sensor.register_callback(lambda *_: None)
            self.sensor.start()
            await asyncio.sleep(0.35)
            self.sensor.stop()
            await asyncio.sleep(0.05)
            self.assertGreaterEqual(mock_read.call_count, 3)
            val = self.sensor.last_value
            self.assertIsInstance(val, float)
            self.assertGreaterEqual(val, 25)
            self.assertLessEqual(val, 95)

class TestPressureSensor(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.sensor = PressureSensor("pres1", "Pressure", "hPa", 980, 1050, frequency=0.1)

    def test_read_value_raises_if_inactive(self):
        self.sensor.active = False
        with self.assertRaises(Exception):
            self.sensor.read_value()

    async def test_start_and_stop_loop_calls_read_value(self):
        with patch.object(self.sensor, 'read_value', wraps=self.sensor.read_value) as mock_read:
            self.sensor.register_callback(lambda *_: None)
            self.sensor.start()
            await asyncio.sleep(0.35)
            self.sensor.stop()
            await asyncio.sleep(0.05)
            self.assertGreaterEqual(mock_read.call_count, 3)
            val = self.sensor.last_value
            self.assertIsInstance(val, float)
            self.assertGreaterEqual(val, 970)
            self.assertLessEqual(val, 1060)

class TestLightSensor(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.sensor = LightSensor("light1", "Light", "lux", 0, 1000, frequency=0.1)

    def test_read_value_raises_if_inactive(self):
        self.sensor.active = False
        with self.assertRaises(Exception):
            self.sensor.read_value()

    async def test_start_and_stop_loop_calls_read_value(self):
        with patch.object(self.sensor, 'read_value', wraps=self.sensor.read_value) as mock_read:
            self.sensor.register_callback(lambda *_: None)
            self.sensor.start()
            await asyncio.sleep(0.35)
            self.sensor.stop()
            await asyncio.sleep(0.05)
            self.assertGreaterEqual(mock_read.call_count, 3)
            val = self.sensor.last_value
            self.assertIsInstance(val, (float, int))
            self.assertGreaterEqual(val, 0)
            self.assertLessEqual(val, 1100)

if __name__ == '__main__':
    unittest.main()

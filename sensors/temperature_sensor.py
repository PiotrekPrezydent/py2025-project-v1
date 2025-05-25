import datetime
from sensors.sensor import Sensor
import random
import math

class TemperatureSensor(Sensor):
    def read_value(self):
        if not self.active:
            raise Exception("Czujnik temperatury jest wyłączony.")
        hour = datetime.datetime.now().hour
        base_temp = (self.max_value + self.min_value) / 2
        amplitude = (self.max_value - self.min_value) / 2
        temp = base_temp + amplitude * math.sin((hour / 24.0) * 2 * math.pi)
        noise = random.uniform(-1.5, 1.5)
        self.last_value = round(temp + noise, 2)
    
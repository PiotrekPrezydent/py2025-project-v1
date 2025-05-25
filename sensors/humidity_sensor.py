from datetime import datetime
from sensors.sensor import Sensor
import random
import math

class HumiditySensor(Sensor):
    def read_value(self):
        if not self.active:
            raise Exception("Czujnik wilgotności jest wyłączony.")
        temp_effect = random.uniform(-5, 5)
        base_humidity = random.uniform(self.min_value, self.max_value)
        self.last_value = round(base_humidity + temp_effect, 2)

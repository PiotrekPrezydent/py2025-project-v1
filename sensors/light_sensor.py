from datetime import datetime
from sensors.sensor import Sensor
import random
import math

class LightSensor(Sensor):
    def read_value(self):
        if not self.active:
            raise Exception("Czujnik oświetlenia jest wyłączony.")
        hour = datetime.now().hour
        if 6 <= hour <= 18:
            base_light = (self.max_value * math.sin(((hour - 6) / 12.0) * math.pi))
        else:
            base_light = 0
        noise = random.uniform(-100, 100)
        self.last_value = round(max(0, base_light + noise), 2)
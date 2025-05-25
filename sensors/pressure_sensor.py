from datetime import datetime
from sensors.sensor import Sensor
import random

class PressureSensor(Sensor):
    def read_value(self):
        if not self.active:
            raise Exception("Czujnik ciśnienia jest wyłączony.")
        fluctuation = random.gauss(0, 1.5)
        pressure = (self.max_value + self.min_value) / 2 + fluctuation
        self.last_value = round(pressure, 2)
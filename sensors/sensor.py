import random
import asyncio
import datetime
from collections import deque

class Sensor:
    def __init__(self, sensor_id, name, unit, min_value, max_value, frequency=1):
        self.sensor_id = sensor_id
        self.name = name
        self.unit = unit
        self.min_value = min_value
        self.max_value = max_value
        self.frequency = frequency
        self.active = False
        self.last_value = None
        self.history = deque(maxlen=100)  # ← bufor historii (do 100 wartości)

        self._callback = None
        self._stop_event = asyncio.Event()
        self._stop_event.set()
        self._task = None

    def edit_values(self, sensor_id=None, name=None, unit=None,
                    min_value=None, max_value=None, frequency=None, type=None):
        if sensor_id is not None:
            self.sensor_id = sensor_id
        if name is not None:
            self.name = name
        if unit is not None:
            self.unit = unit
        if min_value is not None:
            self.min_value = float(min_value)
        if max_value is not None:
            self.max_value = float(max_value)
        if frequency is not None:
            freq = float(frequency)
            if freq <= 0:
                raise ValueError("Częstotliwość musi być większa niż 0.")
            self.frequency = freq
        if type is not None:
            self.type = type  # jeśli atrybut `type` istnieje lub potrzebny


    def read_value(self):
        if not self.active:
            raise Exception(f"Czujnik {self.name} jest wyłączony.")

        value = random.uniform(self.min_value, self.max_value)
        self.last_value = value
        return value

    def calibrate(self, calibration_factor):
        if self.last_value is None:
            self.read_value()

        self.last_value *= calibration_factor
        return self.last_value

    def get_last_value(self):
        if self.last_value is None:
            return self.read_value()
        return self.last_value

    def get_history(self):
        return list(self.history)
    
    def register_callback(self, callback):
        if callable(callback):
            self._callback = callback
        else:
            raise ValueError("Callback musi być callable")

    def _notify_callbacks(self):
        timestamp = datetime.datetime.now()
        self._callback(timestamp, self.sensor_id, self.name, self.get_last_value(), self.unit)

    def start(self):
        if not self.active:
            self.active = True
            self._stop_event.clear()
            self._task = asyncio.create_task(self._run_loop())

    def stop(self):
        if self.active:
            self.active = False
            self._stop_event.set()
            if self._task:
                self._task.cancel()

    async def _run_loop(self):
        try:
            while not self._stop_event.is_set():
                self.read_value()
                self.history.append((datetime.datetime.now(), self.last_value))
                self._notify_callbacks()
                await asyncio.sleep(self.frequency)
        except Exception as e:
            print(e)
            pass

    def __str__(self):
        status = "ON" if self.active else "OFF"
        value = self.last_value if self.last_value is not None else "None"
        return (f"Sensor(id={self.sensor_id}, name={self.name}, unit={self.unit}, "
                f"status={status}, last_value={value})")

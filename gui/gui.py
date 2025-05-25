from gui.window import Window
import tkinter as tk
from tkinter import ttk
from gui.views.default_view import DefaultView
from sensors.sensor_manager import SensorManager
from gui.views.sensor_plot_view import SensorPlotView
import asyncio
import tkinter as tk

class GUI:
    def __init__(self, sensor_manager : SensorManager, *args, **kwargs):
        self.app = Window()
        self._running = False
        self._task = None
        self.sensor_manager = sensor_manager

        self.app.show_view(DefaultView)
        for sensor in sensor_manager.get_all_sensors():
            self.app.add_top_button(sensor.name, lambda s=sensor: self.app.show_view(SensorPlotView, s))

        self.app.add_left_button("Pokaż wykres czujnika", lambda: print("WIP"))
        self.app.add_left_button("Włącz/wyłącz czujnik", lambda: print("WIP"))
        self.app.add_left_button("Konfiguruj czujnik", lambda: print("WIP"))
        self._task = asyncio.create_task(self.async_mainloop())

    async def async_mainloop(self, interval=0.01):
        self._running = True
        try:
            while self._running:
                self.app.update()
                await asyncio.sleep(interval)
        except tk.TclError:
            # Okno zostało zamknięte
            self._running = False


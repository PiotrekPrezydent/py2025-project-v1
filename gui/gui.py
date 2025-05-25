from gui.window import Window
import tkinter as tk
from tkinter import ttk
from gui.views.default_view import DefaultView
from sensors.sensor_manager import SensorManager
from gui.views.sensor_plot_view import SensorPlotView
from gui.views.sensor_edit_view import SensorEditView
import asyncio
import tkinter as tk

class GUI:
    def __init__(self, sensor_manager : SensorManager, *args, **kwargs):
        self.app = Window()
        self._running = False
        self._task = None
        self.sensor_manager = sensor_manager
        self.current_sensor = None

        self.app.show_view(DefaultView)

        for sensor in sensor_manager.get_all_sensors():
            self.app.add_top_button(
                sensor.name,
                lambda s=sensor: self.show_sensor_plot(s)
            )

        self.app.add_left_button("Pokaż wykres czujnika", self.show_sensor_plot)

        self.app.add_left_button("Włącz/wyłącz czujnik", self.toggle_sensor)

        self.app.add_left_button("Konfiguruj czujnik", self.edit_sensor)

        self._task = asyncio.create_task(self.async_mainloop())

    def show_sensor_plot(self, sensor=None):
        if sensor == None:
            if not self.current_sensor:
                return
            self.app.show_view(SensorPlotView, self.current_sensor)
        else:
            self.current_sensor = sensor
            self.app.show_view(SensorPlotView, sensor)

    def toggle_sensor(self):
        if not self.current_sensor:
            return
        if self.current_sensor.active:
            self.current_sensor.stop()
        else:
            self.current_sensor.start()

    def edit_sensor(self, sensor=None):
        if sensor == None:
            if not self.current_sensor:
                return
        self.app.show_view(SensorEditView,self.current_sensor)

    async def async_mainloop(self, interval=0.01):
        self._running = True
        try:
            while self._running:
                self.app.update()
                await asyncio.sleep(interval)
        except tk.TclError:
            self._running = False


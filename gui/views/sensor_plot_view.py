import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import datetime

class SensorPlotView(ttk.Frame):
    def __init__(self, parent, sensor, max_points=100):
        super().__init__(parent)
        self.sensor = sensor
        self.max_points = max_points

        # Inicjalizacja historii z sensora
        self.times = []
        self.values = []
        for timestamp, value in list(sensor.history)[-self.max_points:]:  # ostatnie max_points danych
            self.times.append(timestamp)
            self.values.append(value)

        # Tworzymy wykres
        self.fig, self.ax = plt.subplots(figsize=(6, 3))
        self.line, = self.ax.plot_date(self.times, self.values, '-', label=f"Wartość {self.sensor.name}")
        self.ax.set_xlabel("Czas")
        self.ax.set_ylabel(f"{self.sensor.name} [{self.sensor.unit}]")
        self.ax.set_title(f"Wartość czujnika: {self.sensor.name} (ID: {self.sensor.sensor_id})")
        self.ax.legend()
        self.ax.grid(True)
        self.fig.autofmt_xdate()

        # Osadzenie wykresu w tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Start aktualizacji
        self.after(int(self.sensor.frequency * 1000) , self.update_plot)

    def update_plot(self):
        try:
            val = self.sensor.get_last_value()
        except Exception as e:
            val = None
            print(f"Błąd odczytu sensora {self.sensor.name}:", e)

        if val is not None:
            now = datetime.datetime.now()
            self.times.append(now)
            self.values.append(val)

            # Ograniczamy do max_points
            if len(self.times) > self.max_points:
                self.times.pop(0)
                self.values.pop(0)

            self.line.set_data(self.times, self.values)

            # Automatyczne skalowanie osi
            self.ax.relim()
            self.ax.autoscale_view()

            # Formatowanie osi czasu
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

            self.canvas.draw()

        # Zaplanuj kolejną aktualizację wg frequency
        self.after(int(self.sensor.frequency * 1000), self.update_plot)

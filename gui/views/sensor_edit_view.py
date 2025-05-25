import tkinter as tk
from tkinter import ttk

class SensorEditView(ttk.Frame):
    def __init__(self, parent, sensor):
        super().__init__(parent)
        self.sensor = sensor

        self.entries = {}

        fields = {
            "id": sensor.sensor_id,
            "name": sensor.name,
            "type": getattr(sensor, "type", "unknown"),
            "unit": sensor.unit,
            "min_value": sensor.min_value,
            "max_value": sensor.max_value,
            "frequency": sensor.frequency
        }

        row = 0
        for key, value in fields.items():
            ttk.Label(self, text=key).grid(row=row, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(self)
            entry.insert(0, str(value))
            entry.grid(row=row, column=1, padx=5, pady=5)
            self.entries[key] = entry
            row += 1

        save_button = ttk.Button(self, text="Zapisz", command=self.save)
        save_button.grid(row=row, column=0, columnspan=2, pady=10)

    def save(self):
        try:
            new_values = {
                "sensor_id": self.entries["id"].get(),
                "name": self.entries["name"].get(),
                "type": self.entries["type"].get(),
                "unit": self.entries["unit"].get(),
                "min_value": float(self.entries["min_value"].get()),
                "max_value": float(self.entries["max_value"].get()),
                "frequency": float(self.entries["frequency"].get())
            }

            self.sensor.edit_values(**new_values)
        except Exception as e:
            print(f"Błąd podczas zapisu: {e}")

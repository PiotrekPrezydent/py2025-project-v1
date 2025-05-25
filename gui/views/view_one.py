import tkinter as tk
from tkinter import ttk

class ViewOne(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="To jest widok 1", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self, text="Przycisk 1").pack()
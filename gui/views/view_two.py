import tkinter as tk
from tkinter import ttk

class ViewTwo(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="To jest widok 2", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self, text="Przycisk 2").pack()
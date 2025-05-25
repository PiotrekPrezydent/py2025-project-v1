import tkinter as tk
from tkinter import ttk

class DefaultView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Main View (widok domyślny)", font=("Arial", 18)).pack(expand=True, pady=20)
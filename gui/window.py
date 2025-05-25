import tkinter as tk
from tkinter import ttk
from gui.scrollable_frame import ScrollableFrame
from typing import List
import asyncio

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SensorApplicationClient")
        self.geometry("1000x600")
        self.minsize(600, 400)

        # Konfiguracja układu
        self.grid_rowconfigure(0, weight=1)  # górny pasek – 10%
        self.grid_rowconfigure(1, weight=9)  # reszta – 90%
        self.grid_columnconfigure(1, weight=9)  # main view
        self.grid_columnconfigure(0, weight=1)  # lewy pasek

        # -------------------- GÓRNY PANEL --------------------
        self.top_button_frame = ScrollableFrame(self, orient='horizontal', forced_height=60)
        self.top_button_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.top_button_frame.grid_propagate(False)
        self.top_buttons: List[ttk.Button] = []

        # -------------------- LEWY PANEL --------------------
        self.left_button_frame = ScrollableFrame(self, orient='vertical')
        self.left_button_frame.grid(row=1, column=0, sticky="ns")
        self.left_button_frame.grid_propagate(False)
        self.left_buttons: List[ttk.Button] = []

        # -------------------- MAIN VIEW --------------------
        self.main_view = ttk.Frame(self, relief="sunken", padding=10)
        self.main_view.grid(row=1, column=1, sticky="nsew")

        # Startowy widok (tekst)
        self.current_view = None

        # -------------------- RESPONSYWNE PRZELICZANIE --------------------
        self.bind("<Configure>", self._on_resize)

    def add_top_button(self, text, onClick):
        btn = ttk.Button(self.top_button_frame.scrollable_frame, text=text)
        btn.pack(side="left", padx=2, pady=5)
        btn.config(command=onClick)
        self.top_buttons.append(btn)
        return btn

    def remove_top_button(self, button: ttk.Button):
        if button in self.top_buttons:
            button.pack_forget()  # Usuwa z widoku
            self.top_buttons.remove(button)
            button.destroy()

    def add_left_button(self, text, onClick):
        btn = ttk.Button(self.left_button_frame.scrollable_frame, text=text)
        btn.pack(pady=2, padx=2)
        btn.config(command=onClick)
        self.left_buttons.append(btn)
        return btn

    def remove_left_button(self, button: ttk.Button):
        if button in self.left_buttons:
            button.pack_forget()
            self.left_buttons.remove(button)
            button.destroy()

    def show_view(self, view_class, *args, **kwargs):
        if self.current_view is not None:
            self.current_view.destroy()

        self.current_view = view_class(self.main_view, *args, **kwargs)
        self.current_view.pack(fill="both", expand=True)

    def _on_resize(self, event):
        window_width = self.winfo_width()
        new_width = int(window_width * 0.1)
        self.left_button_frame.canvas.config(width=new_width)

    async def async_mainloop(self):
        try:
            while True:
                self.update()
                await asyncio.sleep(0.01)  # odpuszcza sterowanie asyncio
        except tk.TclError:
            # Okno zostało zamknięte, kończymy pętlę
            pass

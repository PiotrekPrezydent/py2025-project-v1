import tkinter as tk
from tkinter import ttk
from scrollable_frame import ScrollableFrame
from views.view_one import ViewOne
from views.view_two import ViewTwo

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Układ w kształcie odwróconego L")
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

        # Dodaj górne buttony i podpięcie eventów zmieniających widok
        for i in range(20):
            btn = ttk.Button(self.top_button_frame.scrollable_frame, text=f"G{i}")
            btn.pack(side="left", padx=2, pady=5)
            btn.config(command=lambda: self.show_view(ViewTwo))  # górne buttony -> ViewTwo

        # -------------------- LEWY PANEL --------------------
        self.left_button_frame = ScrollableFrame(self, orient='vertical')
        self.left_button_frame.grid(row=1, column=0, sticky="ns")
        self.left_button_frame.grid_propagate(False)

        # Dodaj lewe buttony i podpięcie eventów zmieniających widok
        for i in range(30):
            btn = ttk.Button(self.left_button_frame.scrollable_frame, text=f"L{i}")
            btn.pack(pady=2, padx=2)
            btn.config(command=lambda: self.show_view(ViewOne))  # lewe buttony -> ViewOne

        # -------------------- MAIN VIEW --------------------
        self.main_view = ttk.Frame(self, relief="sunken", padding=10)
        self.main_view.grid(row=1, column=1, sticky="nsew")

        # Startowy widok (tekst)
        self.current_view = None
        self.start_label = ttk.Label(self.main_view, text="Main View", font=("Arial", 18))
        self.start_label.pack(expand=True)

        # -------------------- RESPONSYWNE PRZELICZANIE --------------------
        self.bind("<Configure>", self._on_resize)

    def show_view(self, view_class):
        # Usuń startowy label (jeśli jest)
        if self.start_label.winfo_ismapped():
            self.start_label.pack_forget()

        # Usuń poprzedni widok, jeśli istnieje
        if self.current_view is not None:
            self.current_view.destroy()

        # Utwórz i pokaż nowy widok
        self.current_view = view_class(self.main_view)
        self.current_view.pack(fill="both", expand=True)

    def _on_resize(self, event):
        window_width = self.winfo_width()
        new_width = int(window_width * 0.1)
        self.left_button_frame.canvas.config(width=new_width)
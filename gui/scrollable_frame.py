import tkinter as tk
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, orient='vertical', forced_height=None, forced_width=None, **kwargs):
        super().__init__(container, **kwargs)

        self.canvas = tk.Canvas(self,
                                height=forced_height if forced_height else None,
                                width=forced_width if forced_width else None)
        self.scrollable_frame = ttk.Frame(self.canvas)

        scrollbar = ttk.Scrollbar(self, orient=orient,
                                  command=self.canvas.yview if orient == 'vertical' else self.canvas.xview)

        if orient == 'vertical':
            self.canvas.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            self.canvas.pack(side="left", fill="both", expand=True)
        else:
            self.canvas.configure(xscrollcommand=scrollbar.set)
            scrollbar.pack(side="bottom", fill="x")
            self.canvas.pack(side="top", fill="both", expand=True)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))

        self.scrollable_frame.bind("<Enter>", self._bind_mouse)
        self.scrollable_frame.bind("<Leave>", self._unbind_mouse)

    def _bind_mouse(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

import tkinter as tk
from tkinter import ttk

class ProductEntryField(ttk.Frame):
    def __init__(self, parent, label_text, entry_width):
        super().__init__(parent)

        label = ttk.Label(self, text=label_text, anchor="w", width=entry_width)
        label.grid(row=0, column=0, sticky="w")

        entry = ttk.Entry(self, width=entry_width)
        entry.grid(row=1, column=0, sticky="e")

        self.label = label
        self.entry = entry

    def get(self):
        return self.entry.get()

    def set(self, value):
        self.entry.delete(0, "end")
        self.entry.insert(0, value)

import tkinter as tk
from tkinter import ttk

def create_labeled_entry(parent, label_text, row, default="", show=None):
    label = ttk.Label(parent, text=label_text)
    label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
    entry = ttk.Entry(parent, show=show)
    entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
    entry.insert(0, default)
    return entry

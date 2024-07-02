import tkinter as tk
from tkinter import ttk

class VMEntry(ttk.Frame):
    def __init__(self, parent, entry_number, delete_callback):
        super().__init__(parent)
        self.entry_number = entry_number
        self.delete_callback = delete_callback

        self.name_var = tk.StringVar()
        self.cpu_var = tk.StringVar()
        self.memory_var = tk.StringVar()
        self.disksize_var = tk.StringVar()
        self.guest_id_var = tk.StringVar()

        self.name_entry = self.create_labeled_entry("Name", 0, self.name_var)
        self.cpu_entry = self.create_labeled_entry("CPU", 1, self.cpu_var)
        self.memory_entry = self.create_labeled_entry("Memory (MB)", 2, self.memory_var)
        self.disksize_entry = self.create_labeled_entry("Disk Size (GB)", 3, self.disksize_var)
        self.guest_id_entry = self.create_labeled_entry("Guest ID", 4, self.guest_id_var)

        delete_button = ttk.Button(self, text="Delete VM", command=self.delete_vm)
        delete_button.grid(row=5, column=1, padx=5, pady=5)

    def create_labeled_entry(self, label_text, row, var):
        label = ttk.Label(self, text=label_text)
        label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        entry = ttk.Entry(self, textvariable=var)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        return entry

    def delete_vm(self):
        self.delete_callback(self.entry_number)

    def reposition(self, new_row):
        self.grid_forget()
        self.grid(row=new_row, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    def get_vm_data(self):
        return {
            "name": self.name_var.get(),
            "cpu": self.cpu_var.get(),
            "memory": self.memory_var.get(),
            "disksize": self.disksize_var.get(),
            "guest_id": self.guest_id_var.get()
        }

import tkinter as tk
from tkinter import ttk

class VMEntry(ttk.Frame):
    def __init__(self, parent, entry_number, delete_callback):
        super().__init__(parent)
        self.entry_number = entry_number
        self.delete_callback = delete_callback

        self.name = self.create_labeled_entry("Name", 0)
        self.cpu = self.create_labeled_entry("CPU", 1)
        self.cpu_hot_add_enabled = tk.BooleanVar()
        self.cpu_hot_add_enabled_check = ttk.Checkbutton(self, text="Enable CPU Hot Plug", variable=self.cpu_hot_add_enabled)
        self.cpu_hot_add_enabled_check.grid(row=2, column=1, sticky="w")
        self.memory = self.create_labeled_entry("Memory", 3)
        self.memory_hot_add_enabled = tk.BooleanVar()
        self.memory_hot_add_enabled_check = ttk.Checkbutton(self, text="Enable Memory Hot Plug", variable=self.memory_hot_add_enabled)
        self.memory_hot_add_enabled_check.grid(row=4, column=1, sticky="w")
        self.disksize = self.create_labeled_entry("Disk Size", 5)
        self.disk_provisioning = tk.StringVar()

        self.disk_provisioning_menu = ttk.OptionMenu(
            self, self.disk_provisioning,
            "Thin Provision",
            "Thick Provision Lazy Zeroed",
            "Thick Provision Eager Zeroed",
            "Thin Provision"
        )
        self.create_labeled_widget("Disk Provisioning", self.disk_provisioning_menu, 6)
        self.guest_id = self.create_labeled_entry("Guest ID", 7)

        delete_button = ttk.Button(self, text="Delete VM", command=self.delete_entry)
        delete_button.grid(row=8, column=0, columnspan=2, pady=5)

    def create_labeled_entry(self, label_text, row, show=None):
        label = ttk.Label(self, text=label_text)
        label.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
        entry = ttk.Entry(self, show=show)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky=tk.EW)
        return entry
    
    def create_labeled_widget(self, label_text, widget, row):
        label = ttk.Label(self, text=label_text)
        label.grid(row=row, column=0, padx=5, pady=5, sticky="e")
        widget.grid(row=row, column=1, padx=5, pady=5, sticky="w")

    def get_vm_data(self):
        return {
            "name": self.name.get(),
            "cpu": self.cpu.get(),
            "memory": self.memory.get(),
            "disksize": self.disksize.get(),
            "guest_id": self.guest_id.get(),
            "disk_provisioning": self.disk_provisioning.get(),
            "cpu_hot_add_enabled": self.cpu_hot_add_enabled.get(),
            "memory_hot_add_enabled": self.memory_hot_add_enabled.get()
        }

    def delete_entry(self):
        self.delete_callback(self.entry_number)

    def reposition(self, new_position):
        self.grid(row=new_position, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.entry_number = new_position

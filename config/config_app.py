import tkinter as tk
import subprocess
from tkinter import ttk, messagebox
from config.vm_entry import VMEntry
from config.utils import create_labeled_entry
from config.gui_utils import create_scrollable_frame

class ConfigApp:
    def __init__(self, root):
        self.root = root
        root.title("Configuration Input")

        # Create a scrollable frame using utility function
        scrollable_frame = create_scrollable_frame(root)

        # Initialize lists to keep track of VM entries and their instances
        self.vm_entries = []
        self.vm_entry_instances = []

        # Frame for vCenter
        self.vcenter_frame = ttk.LabelFrame(scrollable_frame, text="vCenter Configuration")
        self.vcenter_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.vcenter_user = create_labeled_entry(self.vcenter_frame, "vCenter User", 0)
        self.vcenter_password = create_labeled_entry(self.vcenter_frame, "vCenter Password", 1, show="*")
        self.vcenter_server = create_labeled_entry(self.vcenter_frame, "vCenter Server", 2)

        # Frame for Jumphost
        self.jumphost_frame = ttk.LabelFrame(scrollable_frame, text="Jumphost Configuration")
        self.jumphost_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.jumphost_ip = create_labeled_entry(self.jumphost_frame, "Jumphost IP", 0)
        self.jumphost_subnet = create_labeled_entry(self.jumphost_frame, "Jumphost Subnet", 1)
        self.jumphost_gateway = create_labeled_entry(self.jumphost_frame, "Jumphost Gateway", 2)
        self.jumphost_user = create_labeled_entry(self.jumphost_frame, "Jumphost User", 3)
        self.jumphost_password = create_labeled_entry(self.jumphost_frame, "Jumphost Password", 4, show="*")

        # Frame for DNS
        self.dns_frame = ttk.LabelFrame(scrollable_frame, text="DNS Configuration")
        self.dns_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.dns_server_list = create_labeled_entry(self.dns_frame, "DNS Server List (comma-separated)", 0)
        self.dns_suffix_list = create_labeled_entry(self.dns_frame, "DNS Suffix List (comma-separated)", 1)

        # Frame for VMs
        self.vms_frame = ttk.LabelFrame(scrollable_frame, text="VMs Configuration")
        self.vms_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Button to add new VM entry
        add_vm_button = ttk.Button(self.vms_frame, text="Add VM", command=self.add_vm_entry)
        add_vm_button.grid(row=0, column=0, padx=5, pady=5)

        # Actions frame
        self.action_frame = ttk.Frame(scrollable_frame)
        self.action_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.save_button = ttk.Button(self.action_frame, text="Generate Terraform Config", command=self.generate_terraform_config)
        self.save_button.grid(row=0, column=0, padx=5, pady=5)

        self.next_button = ttk.Button(self.action_frame, text="Additional Configuration", command=self.open_additional_window)
        self.next_button.grid(row=0, column=1, padx=5, pady=5)

        self.iso_button = ttk.Button(self.action_frame, text="Main.tf file", command=self.open_iso_path_window)
        self.iso_button.grid(row=0, column=2, padx=5, pady=5)

        self.terraform_button = ttk.Button(self.action_frame, text="Run Terraform Files", command=self.open_terraform_window)
        self.terraform_button.grid(row=0, column=3, padx=5, pady=5)        

        self.quit_button = ttk.Button(self.action_frame, text="Quit", command=root.quit)
        self.quit_button.grid(row=0, column=4, padx=5, pady=5)

    def add_vm_entry(self):
        new_entry_number = len(self.vm_entries) + 1
        vm_entry = VMEntry(self.vms_frame, new_entry_number, self.delete_vm_entry)
        vm_entry.grid(row=new_entry_number, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.vm_entries.append(vm_entry)
        self.vm_entry_instances.append(vm_entry)

    def delete_vm_entry(self, entry_number):
        if entry_number <= len(self.vm_entries):
            vm_entry = self.vm_entries[entry_number - 1]
            vm_entry.destroy()
            self.vm_entries.remove(vm_entry)
            self.vm_entry_instances.remove(vm_entry)
            self.reposition_vm_entries()
        else:
            messagebox.showerror("Error", f"VM entry {entry_number} does not exist.")

    def reposition_vm_entries(self):
        for index, entry in enumerate(self.vm_entries):
            entry.reposition(index + 1)

    def generate_terraform_config(self):
        terraform_config = ""

        # Generate vCenter configuration
        vcenter_config = f"""
vCenter_user       = "{self.vcenter_user.get()}"
vCenter_password   = "{self.vcenter_password.get()}"
vCenter_server     = "{self.vcenter_server.get()}"
"""
        terraform_config += vcenter_config

        # Generate Jumphost configuration
        jumphost_config = f"""
jumphost_ip           = "{self.jumphost_ip.get()}"
jumphost_subnet       = "{self.jumphost_subnet.get()}"
jumphost_gateway      = "{self.jumphost_gateway.get()}"
jumphost_user         = "{self.jumphost_user.get()}"
jumphost_password     = "{self.jumphost_password.get()}"
"""
        terraform_config += jumphost_config

        # Generate DNS configuration
        dns_config = f"""
dns_server_list       = [ "{self.dns_server_list.get()}" ]
dns_suffix_list       = [ "{self.dns_suffix_list.get()}" ]
"""
        terraform_config += dns_config

        # Generate VMs configuration
        
        vms_config = "\nvms = {\n"
        for i, vm_entry in enumerate(self.vm_entries):
            vm_data = vm_entry.get_vm_data()
            vms_config += f'  "VM_{i+1}" = {{\n'
            vms_config += f'    name        = "{vm_data["name"]}"\n'
            vms_config += f'    cpu         = {vm_data["cpu"]}\n'
            vms_config += f'    memory      = {vm_data["memory"]}\n'
            vms_config += f'    disksize    = {vm_data["disksize"]}\n'
            vms_config += f'    guest_id    = "{vm_data["guest_id"]}"\n'
            
            vms_config += f'    cpu_hot_add_enabled  = {self.get_boolean_value(vm_data["cpu_hot_add_enabled"])}\n'
            vms_config += f'    memory_hot_add_enabled = {self.get_boolean_value(vm_data["memory_hot_add_enabled"])}\n'
            
            vms_config += f'    eagerly_scrub = {self.get_eagerly_scrub(vm_data["disk_provisioning"])}\n'
            vms_config += f'    thin_provisioned = {self.get_thin_provisioned(vm_data["disk_provisioning"])}\n'
            vms_config += "  }\n"
        vms_config += "}\n"
        terraform_config += vms_config

        # Write to file
        with open("terraform.tfvars", "w") as f:
            f.write(terraform_config)

        messagebox.showinfo("Info", "Terraform configuration generated to terraform.tfvars")

    def clear_entries(self):
        for widget in self.vcenter_frame.winfo_children():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
        for widget in self.jumphost_frame.winfo_children():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
        for widget in self.dns_frame.winfo_children():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
        for vm_entry in self.vm_entries:
            vm_entry.destroy()
        self.vm_entries.clear()
        self.add_vm_entry()

    def open_additional_window(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Additional Configuration")

        # Additional configuration inputs
        additional_frame = ttk.Frame(new_window, padding="10")
        additional_frame.pack(fill=tk.BOTH, expand=True)

        additional_config_label = ttk.Label(additional_frame, text="Additional Configuration")
        additional_config_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.datacenter_entry = create_labeled_entry(additional_frame, "Datacenter", 1)
        self.cluster_entry = create_labeled_entry(additional_frame, "Cluster", 2)
        self.network_entry = create_labeled_entry(additional_frame, "Network", 3)
        self.datastore_entry = create_labeled_entry(additional_frame, "Datastore", 4)
        self.disksize_entry = create_labeled_entry(additional_frame, "Disk Size", 5)

        submit_button = ttk.Button(additional_frame, text="Submit", command=self.generate_variables_tf)
        submit_button.grid(row=8, column=0, columnspan=2, pady=10)

        close_button = ttk.Button(additional_frame, text="Close", command=new_window.destroy)
        close_button.grid(row=7, column=0, columnspan=2, pady=10)

    def open_iso_path_window(self):
        iso_window = tk.Toplevel(self.root)
        iso_window.title("ISO Path Configuration")

        iso_frame = ttk.Frame(iso_window, padding="10")
        iso_frame.pack(fill=tk.BOTH, expand=True)

        iso_label = ttk.Label(iso_frame, text="ISO Path Configuration")
        iso_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.iso_path_entry = create_labeled_entry(iso_frame, "ISO Path", 1)

        submit_button = ttk.Button(iso_frame, text="Submit", command=self.generate_main_tf)
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)

        close_button = ttk.Button(iso_frame, text="Close", command=iso_window.destroy)
        close_button.grid(row=3, column=0, columnspan=2, pady=10)



    def open_terraform_window(self):
        terraform_window = tk.Toplevel(self.root)
        terraform_window.title("Create Terraform Files")

        terraform_frame = ttk.Frame(terraform_window, padding="10")
        terraform_frame.pack(fill=tk.BOTH, expand=True)

        terraform_label = ttk.Label(terraform_frame, text="Create Terraform Files")
        terraform_label.grid(row=0, column=0, columnspan=2, pady=10)

        init_button = ttk.Button(terraform_frame, text="Init", command=self.terraform_init)
        init_button.grid(row=2, column=0, padx=5, pady=10)

        plan_button = ttk.Button(terraform_frame, text="Plan", command=self.terraform_plan)
        plan_button.grid(row=2, column=1, padx=5, pady=10)

        apply_button = ttk.Button(terraform_frame, text="Apply", command=self.terraform_apply)
        apply_button.grid(row=2, column=2, padx=5, pady=10)

        close_button = ttk.Button(terraform_frame, text="Close", command=terraform_window.destroy)
        close_button.grid(row=3, column=0, columnspan=3, pady=10)

    def terraform_init(self):
        self.run_terraform_command("terraform init")

    def terraform_plan(self):
        self.run_terraform_command("terraform plan")

    def terraform_apply(self):
        self.run_terraform_command("terraform apply -auto-approve")

    def run_terraform_command(self, command):
        try:
            result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            messagebox.showinfo("Success", f"Command '{command}' executed successfully:\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Command '{command}' failed:\n{e.stderr}")


    def generate_variables_tf(self):
        variables_tf_content = f"""
variable "vCenter_user" {{
  description = "Username to connect to vCenter Server"
  type        = string
}}

variable "vCenter_password" {{
  description = "Password to connect to vCenter Server"
  type        = string
}}

variable "vCenter_server" {{
  description = "IP or DNS name to connect to vCenter server"
  type        = string
}}

variable "datacenter" {{
  description = "Virtual Datacenter name where VM will be placed"
  type        = string
  default     = "{self.datacenter_entry.get()}"
}}

variable "standalone_host" {{
  description = "Host name"
  type        = string
  default     = "{self.cluster_entry.get()}"
}}


variable "network" {{
  description = "Network name for the VM"
  type        = string
  default     = "{self.network_entry.get()}"
}}

variable "datastore" {{
  description = "Datastore name for the VM"
  type        = string
  default     = "{self.datastore_entry.get()}"
}}

variable "jumphost_ip" {{
  description = "Jumphost IP"
  type        = string
}}

variable "jumphost_subnet" {{
  description = "Jumphost subnet"
  type        = string
}}

variable "jumphost_gateway" {{
  description = "Jumphost gateway"
  type        = string
}}

variable "disksize" {{
  description = "Size of the disk for the VM. Leave empty to use the size from the template."
  type        = string
  default     = "{self.disksize_entry.get()}"
}}

variable "jumphost_user" {{
  description = "Jumphost username"
  type        = string
}}

variable "jumphost_password" {{
  description = "Jumphost password"
  type        = string
}}

variable "dns_server_list" {{
  type = list(string)
  default = []
}}

variable "dns_suffix_list" {{
  type = list(string)
  default = []
}}

variable "vms" {{
  type = map(object({{
    name       = string
    cpu        = number
    memory     = number
    disksize   = number
    guest_id   = string
    cpu_hot_add_enabled   = bool
    memory_hot_add_enabled = bool
    disk_provisioning     = string
  }}))
}}
"""

        # Write to variables.tf file
        with open("variable.tf", "w") as f:
            f.write(variables_tf_content)
            messagebox.showinfo("Info", "Terraform variables configuration generated to variable.tf")
    def get_boolean_value(self, boolean_var):
        return "true" if boolean_var.get() else "false"

    def get_eagerly_scrub(self, disk_provisioning):
        if disk_provisioning.lower() == "thick provision lazy zeroed":
            return "false"
        elif disk_provisioning.lower() == "thick provision eager zeroed":
            return "true"
        elif disk_provisioning.lower() == "thin provision":
            return "false"
        else:
            # Handle other cases or raise an error if needed
            return "false"  # Default to false if input doesn't match expected values

    def get_thin_provisioned(self, disk_provisioning):
        if disk_provisioning.lower() == "thick provision lazy zeroed":
            return "false"
        elif disk_provisioning.lower() == "thick provision eager zeroed":
            return "false"
        elif disk_provisioning.lower() == "thin provision":
            return "true"
        else:
            # Handle other cases or raise an error if needed
            return "false"  # Default to false if input doesn't match expected values

    def generate_main_tf(self):
        vms_data = [entry.get_vm_data() for entry in self.vm_entries]
        
        vms_tf_data = [
        f"""
        {{
            name = "{vm['name']}",
            cpu = {vm['cpu']},
            memory = {vm['memory']},
            disksize = {vm['disksize']},
            guest_id = "{vm['guest_id']}",
            cpu_hot_add_enabled = {vm['cpu_hot_add_enabled']},
            memory_hot_add_enabled = {vm['memory_hot_add_enabled']},
            eagerly_scrub = {vm['eagerly_scrub']},
            thin_provisioned = {vm['thin_provisioned']}
        }}
        """
        for vm in vms_data
    ]

        main_tf_content = f"""
data "vsphere_datacenter" "dc" {{
  name = var.datacenter
}}

data "vsphere_datastore" "datastore" {{
  name          = var.datastore
  datacenter_id = data.vsphere_datacenter.dc.id
}}

data "vsphere_host" "standalone_host" {{
  name          = var.standalone_host
  datacenter_id = data.vsphere_datacenter.dc.id
}}

data "vsphere_network" "network" {{
  name          = var.network
  datacenter_id = data.vsphere_datacenter.dc.id
}}

resource "vsphere_virtual_machine" "vm" {{
  count            = length(var.vms)
  name             = values(var.vms)[count.index].name
  resource_pool_id = data.vsphere_host.standalone_host.resource_pool_id
  datastore_id     = data.vsphere_datastore.datastore.id

  num_cpus             = values(var.vms)[count.index].cpu
  memory               = values(var.vms)[count.index].memory
  guest_id             = values(var.vms)[count.index].guest_id
  cpu_hot_add_enabled  = {self.get_boolean_value("values(var.vms)[count.index].cpu_hot_add_enabled")}
  memory_hot_add_enabled = {self.get_boolean_value("values(var.vms)[count.index].memory_hot_add_enabled")}

  network_interface {{
    network_id   = data.vsphere_network.network.id
    adapter_type = "vmxnet3"
  }}

  disk {{
    label            = "disk0"
    size             = values(var.vms)[count.index].disksize
    eagerly_scrub    = {self.get_eagerly_scrub("values(var.vms)[count.index].disk_provisioning")}
    thin_provisioned = {self.get_thin_provisioned("values(var.vms)[count.index].disk_provisioning")}
  }}
  
  cdrom {{
    datastore_id = data.vsphere_datastore.datastore.id
    path         = "{self.iso_path_entry.get()}"
  }}
}}
"""

        with open("main.tf", "w") as f:
            f.write(main_tf_content)

        messagebox.showinfo("Info", "Terraform configuration generated to main.tf")

    def get_eagerly_scrub(self, disk_provisioning):
        eagerly_scrub_map = {
            "Thick Provision Lazy Zeroed": "false",
            "Thick Provision Eager Zeroed": "true",
            "Thin Provision": "false"
        }
        return eagerly_scrub_map.get(disk_provisioning, "false")

    def get_thin_provisioned(self, disk_provisioning):
        thin_provisioned_map = {
            "Thick Provision Lazy Zeroed": "false",
            "Thick Provision Eager Zeroed": "false",
            "Thin Provision": "true"
        }
        return thin_provisioned_map.get(disk_provisioning, "true")


if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigApp(root)
    root.mainloop()

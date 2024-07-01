import tkinter as tk
from tkinter import ttk, messagebox

class ConfigApp:
    def __init__(self, root):
        self.root = root
        root.title("Configuration Input")

        # Create a canvas and a vertical scrollbar for scrolling
        canvas = tk.Canvas(root)
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        main_frame = ttk.Frame(scrollable_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame for vCenter
        self.vcenter_frame = ttk.LabelFrame(main_frame, text="vCenter Configuration")
        self.vcenter_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.vcenter_user = self.create_labeled_entry(self.vcenter_frame, "vCenter User", 0)
        self.vcenter_password = self.create_labeled_entry(self.vcenter_frame, "vCenter Password", 1, show="*")
        self.vcenter_server = self.create_labeled_entry(self.vcenter_frame, "vCenter Server", 2, default="172.25.204.15")

        # Frame for Jumphost
        self.jumphost_frame = ttk.LabelFrame(main_frame, text="Jumphost Configuration")
        self.jumphost_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.jumphost_ip = self.create_labeled_entry(self.jumphost_frame, "Jumphost IP", 0, default="172.25.204.50")
        self.jumphost_subnet = self.create_labeled_entry(self.jumphost_frame, "Jumphost Subnet", 1, default="24")
        self.jumphost_gateway = self.create_labeled_entry(self.jumphost_frame, "Jumphost Gateway", 2, default="172.25.204.1")
        self.jumphost_user = self.create_labeled_entry(self.jumphost_frame, "Jumphost User", 3)
        self.jumphost_password = self.create_labeled_entry(self.jumphost_frame, "Jumphost Password", 4, show="*")

        # Frame for DNS
        self.dns_frame = ttk.LabelFrame(main_frame, text="DNS Configuration")
        self.dns_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.dns_server_list = self.create_labeled_entry(self.dns_frame, "DNS Server List (comma-separated)", 0, default="10.11.10.69")
        self.dns_suffix_list = self.create_labeled_entry(self.dns_frame, "DNS Suffix List (comma-separated)", 1)

        # Frame for VMs
        self.vms_frame = ttk.LabelFrame(main_frame, text="VMs Configuration")
        self.vms_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.vm1_name = self.create_labeled_entry(self.vms_frame, "VM 1 Name", 0, default="VM-1")
        self.vm1_ip = self.create_labeled_entry(self.vms_frame, "VM 1 IP", 1, default="172.25.204.49")
        self.vm1_cpu = self.create_labeled_entry(self.vms_frame, "VM 1 CPU", 2, default="2")
        self.vm1_memory = self.create_labeled_entry(self.vms_frame, "VM 1 Memory (MB)", 3, default="1024")
        self.vm1_disksize = self.create_labeled_entry(self.vms_frame, "VM 1 Disk Size (GB)", 4, default="40")
        self.vm1_guest_id = self.create_labeled_entry(self.vms_frame, "VM 1 Guest ID", 5, default="centos7_64Guest")
        self.vm1_netmask = self.create_labeled_entry(self.vms_frame, "VM 1 IPv4 Netmask", 6, default="24")
        self.vm1_gateway = self.create_labeled_entry(self.vms_frame, "VM 1 IPv4 Gateway", 7, default="172.25.204.1")
        self.vm1_username = self.create_labeled_entry(self.vms_frame, "VM 1 Username", 8, default="kube-spray")
        self.vm1_password = self.create_labeled_entry(self.vms_frame, "VM 1 Password", 9, default="12345", show="*")

        self.vm2_name = self.create_labeled_entry(self.vms_frame, "VM 2 Name", 10, default="VM-2")
        self.vm2_ip = self.create_labeled_entry(self.vms_frame, "VM 2 IP", 11, default="172.25.204.50")
        self.vm2_cpu = self.create_labeled_entry(self.vms_frame, "VM 2 CPU", 12, default="2")
        self.vm2_memory = self.create_labeled_entry(self.vms_frame, "VM 2 Memory (MB)", 13, default="1024")
        self.vm2_disksize = self.create_labeled_entry(self.vms_frame, "VM 2 Disk Size (GB)", 14, default="40")
        self.vm2_guest_id = self.create_labeled_entry(self.vms_frame, "VM 2 Guest ID", 15, default="centos7_64Guest")
        self.vm2_netmask = self.create_labeled_entry(self.vms_frame, "VM 2 IPv4 Netmask", 16, default="24")
        self.vm2_gateway = self.create_labeled_entry(self.vms_frame, "VM 2 IPv4 Gateway", 17, default="172.25.204.1")
        self.vm2_username = self.create_labeled_entry(self.vms_frame, "VM 2 Username", 18, default="kube-spray")
        self.vm2_password = self.create_labeled_entry(self.vms_frame, "VM 2 Password", 19, default="12345", show="*")

        # Frame for actions
        self.action_frame = ttk.Frame(main_frame)
        self.action_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.save_button = ttk.Button(self.action_frame, text="Generate Terraform Config", command=self.generate_terraform_config)
        self.save_button.pack(side="left", padx=5)

        self.next_button = ttk.Button(self.action_frame, text="Next", command=self.open_additional_window)
        self.next_button.pack(side="left", padx=5)

        self.clear_button = ttk.Button(self.action_frame, text="Clear", command=self.clear_entries)
        self.clear_button.pack(side="left", padx=5)

        self.quit_button = ttk.Button(self.action_frame, text="Quit", command=root.quit)
        self.quit_button.pack(side="right", padx=5)

    def create_labeled_entry(self, parent, label_text, row, default="", show=None):
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        entry = ttk.Entry(parent, show=show)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        entry.insert(0, default)
        return entry

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
        vms_config = f"""
disksize               = "{self.vm1_disksize.get()}"

vms = {{
   "rocky_test_1"= {{
    name                = "{self.vm1_name.get()}"
    vm_ip               = "{self.vm1_ip.get()}"
    cpu                 = {self.vm1_cpu.get()}
    memory              = {self.vm1_memory.get()}
    disksize            = {self.vm1_disksize.get()}
    guest_id            = "{self.vm1_guest_id.get()}"
    ipv4_netmask        = {self.vm1_netmask.get()}
    ipv4_gateway        = "{self.vm1_gateway.get()}"
    username            = "{self.vm1_username.get()}"
    password            = "{self.vm1_password.get()}"
  }}
   "rocky_test_2"= {{
    name                = "{self.vm2_name.get()}"
    vm_ip               = "{self.vm2_ip.get()}"
    cpu                 = {self.vm2_cpu.get()}
    memory              = {self.vm2_memory.get()}
    disksize            = {self.vm2_disksize.get()}
    guest_id            = "{self.vm2_guest_id.get()}"
    ipv4_netmask        = {self.vm2_netmask.get()}
    ipv4_gateway        = "{self.vm2_gateway.get()}"
    username            = "{self.vm2_username.get()}"
    password            = "{self.vm2_password.get()}"
  }}
}}
"""
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
        for widget in self.vms_frame.winfo_children():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)

    def open_additional_window(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Additional Configuration")

        # Additional configuration inputs
        additional_frame = ttk.Frame(new_window, padding="10")
        additional_frame.pack(fill=tk.BOTH, expand=True)

        additional_config_label = ttk.Label(additional_frame, text="Additional Configuration")
        additional_config_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.datacenter_entry = self.create_labeled_entry(additional_frame, "Datacenter", 1, default="TU-Datacenter")
        self.cluster_entry = self.create_labeled_entry(additional_frame, "Cluster", 2, default="Database Server B")
        self.network_entry = self.create_labeled_entry(additional_frame, "Network", 3, default="VM Network")
        self.datastore_entry = self.create_labeled_entry(additional_frame, "Datastore", 4, default="Database-Server-B-Datastore")
        self.disksize_entry = self.create_labeled_entry(additional_frame, "Disk Size", 5, default="20")

        next_button = ttk.Button(additional_frame, text="Next", command=self.open_iso_path_window)
        next_button.grid(row=6, column=0, columnspan=2, pady=10)

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

        self.iso_path_entry = self.create_labeled_entry(iso_frame, "ISO Path", 1, default="ISO/CentOS-7-x86_64-DVD-2009.iso")

        submit_button = ttk.Button(iso_frame, text="Submit", command=self.generate_main_tf)
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)

        close_button = ttk.Button(iso_frame, text="Close", command=iso_window.destroy)
        close_button.grid(row=3, column=0, columnspan=2, pady=10)

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

variable "cluster" {{
  description = "Cluster name"
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
    vm_ip      = string
    cpu        = number
    memory     = number
    disksize   = number
    guest_id   = string
    ipv4_netmask = number
    ipv4_gateway = string
    username    = string
    password    = string
  }}))
  default = {{
    rocky_test_1 = {{
      name       = "{self.vm1_name.get()}"
      vm_ip      = "{self.vm1_ip.get()}"
      cpu        = {self.vm1_cpu.get()}
      memory     = {self.vm1_memory.get()}
      disksize   = {self.vm1_disksize.get()}
      guest_id   = "{self.vm1_guest_id.get()}"
      ipv4_netmask = {self.vm1_netmask.get()}
      ipv4_gateway = "{self.vm1_gateway.get()}"
      username    = "{self.vm1_username.get()}"
      password    = "{self.vm1_password.get()}"
    }}
    rocky_test_2 = {{
      name       = "{self.vm2_name.get()}"
      vm_ip      = "{self.vm2_ip.get()}"
      cpu        = {self.vm2_cpu.get()}
      memory     = {self.vm2_memory.get()}
      disksize   = {self.vm2_disksize.get()}
      guest_id   = "{self.vm2_guest_id.get()}"
      ipv4_netmask = {self.vm2_netmask.get()}
      ipv4_gateway = "{self.vm2_gateway.get()}"
      username    = "{self.vm2_username.get()}"
      password    = "{self.vm2_password.get()}"
    }}
  }}
}}

variable "vminfo" {{
  type = map(object({{
    vm     = string
    cpu    = string
    memory = string
  }}))
  default = {{
    "rocky_test_1" = {{
      vm     = "{self.vm1_name.get()}"
      cpu    = "{self.vm1_cpu.get()}"
      memory = "{self.vm1_memory.get()}"
    }}
    "rocky_test_2" = {{
      vm = "{self.vm2_name.get()}"
      cpu = "{self.vm2_cpu.get()}"
      memory = "{self.vm2_memory.get()}"
    }}
  }}
}}
"""

        # Write to variables.tf file
        with open("variable.tf", "w") as f:
            f.write(variables_tf_content)
            messagebox.showinfo("Info", "Terraform variables configuration generated to variable.tf")

    def generate_main_tf(self):
        main_tf_content = f"""
data "vsphere_datacenter" "dc" {{
  name = "var.datacenter"
}}

data "vsphere_datastore" "datastore" {{
  name          = var.datastore
  datacenter_id = data.vsphere_datacenter.dc.id
}}

data "vsphere_compute_cluster" "cluster" {{
  name          = var.cluster
  datacenter_id = data.vsphere_datacenter.dc.id
}}

data "vsphere_network" "network" {{
  name          = var.network
  datacenter_id = data.vsphere_datacenter.dc.id
}}

resource "vsphere_virtual_machine" "vm" {{
  count            = length(var.vms)
  name             = values(var.vms)[count.index].name
  resource_pool_id = data.vsphere_compute_cluster.cluster.resource_pool_id
  datastore_id     = data.vsphere_datastore.datastore.id

  num_cpus             = values(var.vms)[count.index].cpu
  memory               = values(var.vms)[count.index].memory
  guest_id             = values(var.vms)[count.index].guest_id
  cpu_hot_add_enabled  = true
  memory_hot_add_enabled = true

  network_interface {{
    network_id   = data.vsphere_network.network.id
    adapter_type = "vmxnet3"
  }}

  disk {{
    label            = "disk0"
    size             = values(var.vms)[count.index].disksize
    eagerly_scrub    = false
    thin_provisioned = false
  }}
  
  cdrom {{
    datastore_id = data.vsphere_datastore.datastore.id
    path         = "{self.iso_path_entry.get()}"
  }}

  extra_config = {{
    "guestinfo.userdata" = <<EOF
#cloud-config
users:
  - default
  - name: ${{values(var.vms)[count.index].username}}
    sudo: ALL=(ALL) NOPASSWD:ALL
    groups: users, admin
    home: /home/${{values(var.vms)[count.index].username}}
    shell: /bin/bash
    lock_passwd: false
    passwd: ${{values(var.vms)[count.index].password}}

network:
  version: 2
  ethernets:
    eth0:
      addresses:
        - ${{values(var.vms)[count.index].vm_ip}}/${{values(var.vms)[count.index].ipv4_netmask}}
      gateway4: ${{values(var.vms)[count.index].ipv4_gateway}}
      nameservers:
        addresses: ${{jsonencode(var.dns_server_list)}}
        search: ${{jsonencode(var.dns_suffix_list)}}
EOF
  }}

  wait_for_guest_net_timeout = 120

  provisioner "remote-exec" {{
    inline = [
      "echo -e '${{values(var.vms)[count.index].password}}${{values(var.vms)[count.index].password}}' | passwd ${{values(var.vms)[count.index].username}}"
    ]

    connection {{
      type     = "ssh"
      user     = "root"
      password = "12345"  # Replace with the actual root password or another initial password
      host     = values(var.vms)[count.index].vm_ip
    }}
  }}
}}

output "vm_ips" {{
  value = {{ for k, v in var.vms : k => v.vm_ip }}
}}

output "vm_names" {{
  value = {{ for k, v in var.vms : k => v.name }}
}}

"""

        # Write to main.tf file
        with open("main.tf", "w") as f:
            f.write(main_tf_content)

        messagebox.showinfo("Info", "Terraform variables configuration generated to main.tf")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigApp(root)
    root.mainloop()

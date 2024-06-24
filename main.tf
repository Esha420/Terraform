data "vsphere_datacenter" "dc" {
  name = var.datacenter
}

data "vsphere_datastore" "datastore" {
  name          = var.datastore
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_compute_cluster" "cluster" {
  name          = var.cluster
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_network" "network" {
  name          = var.network
  datacenter_id = data.vsphere_datacenter.dc.id
}

resource "vsphere_virtual_machine" "vm" {
  name             = var.vms["rocky_test_1"]["name"]
  resource_pool_id = data.vsphere_compute_cluster.cluster.resource_pool_id
  datastore_id     = data.vsphere_datastore.datastore.id
  num_cpus         = 2
  memory           = 4096  # in MB (4 GB)
  guest_id         = "centos64Guest"  # Adjust guest_id based on your operating system
  
  network_interface {
    network_id   = data.vsphere_network.network.id
    adapter_type = "vmxnet3"
  }

  disk {
    label            = "disk0"
    size             = var.disksize  # Convert to GB
    thin_provisioned = true
  }

  cdrom {
    datastore_id = data.vsphere_datastore.datastore.id
    path         = "/vmfs/volumes/${var.datastore}/ISO/CentOS-7-x86_64-DVD-2009.iso"  # Adjust path as per your ISO
  }

  # Customize further properties as needed (e.g., CPU limits, custom scripts, etc.)

}

# Outputs for useful information
output "vm_name" {
  value = vsphere_virtual_machine.vm.name
}

output "vm_ip_address" {
  value = var.vms["rocky_test_1"]["vm_ip"]
}

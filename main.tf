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

data "vsphere_virtual_machine" "template" {
  name          = var.template
  datacenter_id = data.vsphere_datacenter.dc.id
}

resource "vsphere_virtual_machine" "vm" {
  name             = "terraform_test"
  resource_pool_id = data.vsphere_compute_cluster.cluster.resource_pool_id
  datastore_id     = data.vsphere_datastore.datastore.id
 
  num_cpus = 2
  memory   = 4096
  guest_id = "centos7_64Guest"
 
  network_interface {
    network_id = data.vsphere_network.network.id
    adapter_type = "vmxnet3"
  }
 
  disk {
    label            = "disk0"
    size             = 40
    eagerly_scrub    = false
    thin_provisioned = true
  }
 
  clone {
    template_uuid = data.vsphere_virtual_machine.template.id
 
    customize {
      linux_options {
        host_name = "terraform_test"
        domain    = "local"
      }
 
      network_interface {
        ipv4_address = var.jumphost_ip
        ipv4_netmask = var.jumphost_subnet
      }
 
      ipv4_gateway = var.jumphost_gateway
    }
  }
}

# Outputs for useful information
output "vm_name" {
  value = vsphere_virtual_machine.vm.name
}

output "vm_ip_address" {
  value = var.vms["terraform_test"]["vm_ip"]
}

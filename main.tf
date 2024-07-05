
data "vsphere_datacenter" "dc" {
  name = var.datacenter
}

data "vsphere_datastore" "datastore" {
  name          = var.datastore
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_host" "standalone_host" {
  name          = var.standalone_host
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_network" "network" {
  name          = var.network
  datacenter_id = data.vsphere_datacenter.dc.id
}

resource "vsphere_virtual_machine" "vm" {
  count            = length(var.vms)
  name             = values(var.vms)[count.index].name
  resource_pool_id = data.vsphere_host.standalone_host.resource_pool_id
  datastore_id     = data.vsphere_datastore.datastore.id

  num_cpus             = values(var.vms)[count.index].cpu
  memory               = values(var.vms)[count.index].memory
  guest_id             = values(var.vms)[count.index].guest_id
  cpu_hot_add_enabled  = false
  memory_hot_add_enabled = false

  network_interface {
    network_id   = data.vsphere_network.network.id
    adapter_type = "vmxnet3"
  }

  disk {
    label            = "disk0"
    size             = values(var.vms)[count.index].disksize
    eagerly_scrub    = false
    thin_provisioned = true
  }
  
  cdrom {
    datastore_id = data.vsphere_datastore.datastore.id
    path         = ""
  }
}

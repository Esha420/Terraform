locals {
  disks = [
    { "id": 1, "dev": "sdb", "lvm": 0, "sizeGB": 16, "dir": "/data1" }
  ]

  disk_format_args = join(" ", [
    for disk in local.disks: "${disk.dev},${disk.lvm},${disk.sizeGB},${disk.dir}"
  ])
}

data "vsphere_datacenter" "datacenter" {
  name = var.datacenter
}

data "vsphere_datastore" "datastore" {
  name          = var.datastore
  datacenter_id = data.vsphere_datacenter.datacenter.id
}

data "vsphere_compute_cluster" "cluster" {
  name          = var.cluster
  datacenter_id = data.vsphere_datacenter.datacenter.id
}

data "vsphere_network" "network" {
  name          = var.network
  datacenter_id = data.vsphere_datacenter.datacenter.id

}

resource "vsphere_virtual_machine" "vm" {
  name             = "my-ucentos-vm"
  resource_pool_id = data.vsphere_compute_cluster.cluster.resource_pool_id
  datastore_id     = data.vsphere_datastore.datastore.id
  num_cpus         = 2
  memory           = 4096
  guest_id         = "CentOS64Guest"
  
  network_interface {
    network_id = data.vsphere_network.network.id
    
  }

  disk {
    label = "disk0"
    size  = 40
  }

 cdrom {
    datastore_id = data.vsphere_datastore.datastore.id
    path         = "/vmfs/volumes/Database-Server-B-Datastore/ISO/CentOS-7-x86_64-DVD-2009.iso"
  }

   
  }

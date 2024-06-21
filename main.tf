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
data "vsphere_virtual_machine" "template" {
  name          = var.template
  datacenter_id = data.vsphere_datacenter.datacenter.id
}

resource "vsphere_virtual_machine" "vm" {
  for_each         = var.vminfo
  name             = each.value["vm"]
  resource_pool_id = data.vsphere_compute_cluster.cluster.resource_pool_id
  datastore_id     = data.vsphere_datastore.datastore.id
  num_cpus         = each.value["cpu"]
  memory           = each.value["memory"]
  guest_id         = data.vsphere_virtual_machine.template.guest_id
  scsi_type        = data.vsphere_virtual_machine.template.scsi_type
  wait_for_guest_net_timeout = 0
  network_interface {
    network_id   = data.vsphere_network.network.id
    adapter_type = "vmxnet3"
  }

  disk {
    label            = "${each.value["vm"]}-disk0"
    size             =40
    eagerly_scrub    = data.vsphere_virtual_machine.template.disks.0.eagerly_scrub
    thin_provisioned = data.vsphere_virtual_machine.template.disks.0.thin_provisioned
  }

  dynamic "disk" {
    for_each = [ for disk in local.disks: disk ]
    
    content {
     label            = "disk${disk.value.id}"
     unit_number      = disk.value.id
     datastore_id     = data.vsphere_datastore.datastore.id
     size             = disk.value.sizeGB
     eagerly_scrub    = false
     thin_provisioned = true
    }
  }


   clone {
    template_uuid = data.vsphere_virtual_machine.template.id
    customize {
      linux_options {
        host_name = "terraform1"
        domain    = "example.com"
      }
      network_interface {
        ipv4_address = var.jumphost_ip
        ipv4_netmask = var.jumphost_subnet
      }
      ipv4_gateway = var.jumphost_gateway
      dns_server_list = var.dns_server_list
      dns_suffix_list = var.dns_suffix_list
    }
  }
   
  }

locals {
  disks = [
    { "id": 1, "dev": "sdb", "lvm": 0, "sizeGB": tonumber(var.disksize), "dir": "/data1" }
  ]

  disk_format_args = join(" ", [
    for disk in local.disks : "${disk.dev},${disk.lvm},${disk.sizeGB},${disk.dir}"
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
  for_each         = var.vms
  name             = each.value.name
  resource_pool_id = data.vsphere_compute_cluster.cluster.resource_pool_id
  datastore_id     = data.vsphere_datastore.datastore.id
  num_cpus         = tonumber(var.vminfo[each.key].cpu)
  memory           = tonumber(var.vminfo[each.key].memory)
  guest_id         = "centos64Guest"
  scsi_type        = "lsilogic-sas"

  network_interface {
    network_id   = data.vsphere_network.network.id
    adapter_type = "vmxnet3"
  }

  disk {
    label = "disk0"
    size  = tonumber(var.disksize)
  }

  cdrom {
    datastore_id = data.vsphere_datastore.datastore.id
    path         = "/vmfs/volumes/${var.datastore}/ISO/CentOS-7-x86_64-DVD-2009.iso"
  }

  dynamic "disk" {
    for_each = local.disks
    content {
      label           = "disk${disk.value.id}"
      size            = disk.value.sizeGB
      unit_number     = disk.value.id
      eagerly_scrub   = false
      thin_provisioned = true
    }
  }

  provisioner "remote-exec" {
    inline = [
      "sudo mkfs.ext4 /dev/sdb",
      "sudo mkdir -p /data1",
      "sudo mount /dev/sdb /data1",
      "echo '/dev/sdb /data1 ext4 defaults 0 0' | sudo tee -a /etc/fstab"
    ]

    connection {
      type     = "ssh"
      user     = var.jumphost_user
      password = var.jumphost_password
      host     = each.value.vm_ip
    }
  }
}

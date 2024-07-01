
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
  count            = length(var.vms)
  name             = values(var.vms)[count.index].name
  resource_pool_id = data.vsphere_compute_cluster.cluster.resource_pool_id
  datastore_id     = data.vsphere_datastore.datastore.id

  num_cpus             = values(var.vms)[count.index].cpu
  memory               = values(var.vms)[count.index].memory
  guest_id             = values(var.vms)[count.index].guest_id
  cpu_hot_add_enabled  = true
  memory_hot_add_enabled = true

  network_interface {
    network_id   = data.vsphere_network.network.id
    adapter_type = "vmxnet3"
  }

  disk {
    label            = "disk0"
    size             = values(var.vms)[count.index].disksize
    eagerly_scrub    = false
    thin_provisioned = false
  }
  
  cdrom {
    datastore_id = data.vsphere_datastore.datastore.id
    path         = "ubuntu-20.04.4-live-server-amd64.iso"
  }

  extra_config = {
    "guestinfo.userdata" = <<EOF
#cloud-config
users:
  - default
  - name: ${values(var.vms)[count.index].username}
    sudo: ALL=(ALL) NOPASSWD:ALL
    groups: users, admin
    home: /home/${values(var.vms)[count.index].username}
    shell: /bin/bash
    lock_passwd: false
    passwd: ${values(var.vms)[count.index].password}

network:
  version: 2
  ethernets:
    eth0:
      addresses:
        - ${values(var.vms)[count.index].vm_ip}/${values(var.vms)[count.index].ipv4_netmask}
      gateway4: ${values(var.vms)[count.index].ipv4_gateway}
      nameservers:
        addresses: ${jsonencode(var.dns_server_list)}
        search: ${jsonencode(var.dns_suffix_list)}
EOF
  }

  wait_for_guest_net_timeout = 120

  provisioner "remote-exec" {
    inline = [
      "echo -e '${values(var.vms)[count.index].password}${values(var.vms)[count.index].password}' | passwd ${values(var.vms)[count.index].username}"
    ]

    connection {
      type     = "ssh"
      user     = "root"
      password = "12345"  # Replace with the actual root password or another initial password
      host     = values(var.vms)[count.index].vm_ip
    }
  }
}

output "vm_ips" {
  value = { for k, v in var.vms : k => v.vm_ip }
}

output "vm_names" {
  value = { for k, v in var.vms : k => v.name }
}


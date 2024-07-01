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

# resource "vsphere_virtual_machine" "vm" {
#   name             = "terraform_test"
#   resource_pool_id = data.vsphere_compute_cluster.cluster.resource_pool_id
#   datastore_id     = data.vsphere_datastore.datastore.id
 
#   num_cpus = 2
#   memory   = 4096
#   guest_id = "centos7_64Guest"
 
#   network_interface {
#     network_id = data.vsphere_network.network.id
#     adapter_type = "vmxnet3"
#   }
 
#   disk {
#     label            = "disk0"
#     size             = 40
#     eagerly_scrub    = false
#     thin_provisioned = true
#   }
 
#   clone {
#     template_uuid = data.vsphere_virtual_machine.template.id
 
#     customize {
#       linux_options {
#         host_name = "terraform"
#         domain    = "local"
#       }
 
#       network_interface {
#         ipv4_address = var.jumphost_ip
#         ipv4_netmask = var.jumphost_subnet
#       }
 
#       ipv4_gateway = var.jumphost_gateway
#     }
#   }
# }


resource "vsphere_virtual_machine" "vm" {
  count            = length(var.vms)
  name             = values(var.vms)[count.index].name
  resource_pool_id = data.vsphere_compute_cluster.cluster.resource_pool_id
  datastore_id     = data.vsphere_datastore.datastore.id

  num_cpus = values(var.vms)[count.index].cpu
  memory   = values(var.vms)[count.index].memory
  guest_id = values(var.vms)[count.index].guest_id

  network_interface {
    network_id   = data.vsphere_network.network.id
    adapter_type = "vmxnet3"
  }

  disk {
    label            = "disk0"
    size             = values(var.vms)[count.index].disksize
    eagerly_scrub    = true
    thin_provisioned = false
  }

  clone {
    template_uuid = data.vsphere_virtual_machine.template.id

    customize {
      linux_options {
        host_name = values(var.vms)[count.index].name
        domain    = "local"
      }

      network_interface {
        ipv4_address = values(var.vms)[count.index].vm_ip
        ipv4_netmask = values(var.vms)[count.index].ipv4_netmask
      }

      ipv4_gateway = values(var.vms)[count.index].ipv4_gateway

      dns_server_list = var.dns_server_list
      dns_suffix_list = var.dns_suffix_list
    }
  }

  provisioner "remote-exec" {
    inline = [
      "echo -e '${var.vms[count.index].password}\n${var.vms[count.index].password}' | passwd ${var.vms[count.index].username}"
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


# resource "vsphere_virtual_machine" "vm" {
#   for_each         = var.vms
#   name             = each.value.name
#   resource_pool_id = data.vsphere_compute_cluster.cluster.resource_pool_id
#   datastore_id     = data.vsphere_datastore.datastore.id
#   num_cpus         = each.value.cpu
#   memory           = each.value.memory
#   guest_id         = each.value.guest_id

#   network_interface {
#     network_id   = data.vsphere_network.network.id
#     adapter_type = "vmxnet3"
#   }

#   disk {
#     label            = "disk0"
#     size             = each.value.disksize
#     eagerly_scrub    = false
#     thin_provisioned = true
#   }

#   clone {
#     template_uuid = data.vsphere_virtual_machine.template.id

#     customize {
#       linux_options {
#         host_name = each.value.name
#         domain    = "local"
#       }

#       network_interface {
#         ipv4_address = each.value.vm_ip
#         ipv4_netmask = each.value.ipv4_netmask
#       }

#       ipv4_gateway = each.value.ipv4_gateway
#     }
#   }
# }

# Outputs for useful information
# output "vm_ips" {
#   value = { for k, v in var.vms : k => v.vm_ip }
# }

# output "vm_names" {
#   value = { for k, v in var.vms : k => v.name }
# }

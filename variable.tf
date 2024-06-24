variable "vCenter_user" {
  description = "Username to connect to vCenter Server"
  type        = string
}

variable "vCenter_password" {
  description = "Password to connect to vCenter Server"
  type        = string
}

variable "vCenter_server" {
  description = "IP or DNS name to connect to vCenter server"
  type        = string
}

variable "datacenter" {
  description = "Virtual Datacenter name where VM will be placed"
  type        = string
  default     = "TU-Datacenter"
}

variable "cluster" {
  description = "Cluster name"
  type        = string
  default     = "Database Server B"
}

variable "network" {
  description = "Network name for the VM"
  type        = string
  default     = "VM Network"
}

variable "datastore" {
  description = "Datastore name for the VM"
  type        = string
  default     = "Database-Server-B-Datastore"
}

variable "template" {
  description = "Template to use for the VM"
  type        = string
  default     = "CentOs"
}

variable "jumphost_ip" {
  description = "Jumphost IP"
  type        = string
}

variable "jumphost_subnet" {
  description = "Jumphost subnet"
  type        = string
}

variable "jumphost_gateway" {
  description = "Jumphost gateway"
  type        = string
}

variable "disksize" {
  description = "Size of the disk for the VM. Leave empty to use the size from the template."
  type        = string
  default     = "20"
}

variable "jumphost_user" {
  description = "Jumphost username"
  type        = string
}

variable "jumphost_password" {
  description = "Jumphost password"
  type        = string
}

variable "dns_server_list" { 
  type = list(string)
  default = []
}

variable "dns_suffix_list" { 
  type = list(string)
  default = []
}

# variable "vms" {
#   type = map(object({
#     name  = string
#     vm_ip = string
#   }))
  
#   default = {
#     rocky_test_1 = {
#       name  = "terraform_test"
#       vm_ip = "172.25.204.50"
#     }
#   }
# }


variable "vms" {
  type = map(object({
    name       = string
    vm_ip      = string
    cpu        = number
    memory     = number
    disksize   = number
    guest_id   = string
    ipv4_netmask = number
    ipv4_gateway = string
  }))
  default = {
    rocky_test_1 = {
      name       = "VM-1"
      vm_ip      = "172.25.204.49"
      cpu        = 2
      memory     = 1024
      disksize   = 40
      guest_id   = "centos7_64Guest"
      ipv4_netmask = 24
      ipv4_gateway = "172.25.204.1"
    }
    rocky_test_2 = {
      name       = "VM-2"
      vm_ip      = "172.25.204.50"
      cpu        = 2
      memory     = 1024
      disksize   = 40
      guest_id   = "centos7_64Guest"
      ipv4_netmask = 24
      ipv4_gateway = "172.25.204.1"
    }
  }
}

variable "vminfo" {
  type = map(object({
    vm     = string
    cpu    = string
    memory = string
  }))
  default = {
    "rocky_test_1" = {
      vm     = "VM-1"
      cpu    = "2"
      memory = "1024"
    }
    "rocky_test_2" = {
      vm = "VM-2"
      cpu = "2"
      memory = "1024"
    }
  }
}
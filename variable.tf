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
  default     = "Application Server A"
}

variable "network" {
  description = "IP or DNS name to connect to vCenter server"
  type        = string
  default     = "VM Network"
}

variable "datastore" {
  description = "IP or DNS name to connect to vCenter server"
  type        = string
  default     = "Database-Server-B-Datastore"
}

variable "template" {
  description = "IP or DNS name to connect to vCenter server"
  type        = string
  default     = "Ubuntu"
}

variable "jumphost_ip" {
  description = "jumphost_ip"
}

variable "jumphost_subnet" {
  description = "jumphost_subnet"
}

variable "jumphost_gateway" {
  description = "jumphost_gateway"
}

variable "disksize" {
  description = "Size of the disk for the VM. Leave empty to use the size from the template."
  type        = string
  default     = "20"
}


variable "jumphost_user" { }
variable "jumphost_password" {}

variable "dns_server_list" { 
  type = list(string)
  default = [ ]
}
variable "dns_suffix_list" { 
  type = list(string)
  default = [ ]
}

variable "vms" {
  type = map(object({
    name  = string
    vm_ip = string
  }))
  
  default = {
    rocky_test_1 = {
      name  = "rocky-1"
      vm_ip = "172.25.204.49"
    }
  }
}

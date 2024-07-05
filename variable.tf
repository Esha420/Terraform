
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
  default     = "LIS_ESXI"
}

variable "standalone_host" {
  description = "Host name"
  type        = string
  default     = "192.168.50.198"
}

variable "network" {
  description = "Network name for the VM"
  type        = string
  default     = "VM Network"
}

variable "datastore" {
  description = "Datastore name for the VM"
  type        = string
  default     = "QNAP_ISO"
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
  default     = "40"
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

variable "vms" {
  type = map(object({
    name       = string
    cpu        = number
    memory     = number
    disksize   = number
    guest_id   = string
  }))
}

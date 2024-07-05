
vCenter_user       = ""
vCenter_password   = ""
vCenter_server     = ""

jumphost_ip           = ""
jumphost_subnet       = ""
jumphost_gateway      = ""
jumphost_user         = ""
jumphost_password     = ""

dns_server_list       = [ "" ]
dns_suffix_list       = [ "" ]

vms = {
  "VM_1" = {
    name        = "1"
    cpu         = 1
    memory      = 1
    disksize    = 1
    guest_id    = "1"
    cpu_hot_add_enabled  = true
    memory_hot_add_enabled = false
    eagerly_scrub = false
    thin_provisioned = false
  }
}

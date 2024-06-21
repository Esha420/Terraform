vCenter_user       = "Administrator@vcsa.local"
vCenter_password   = "Tu$P@ssw0rdVr@"
vCenter_server     = "172.25.204.172"


jumphost_ip           = "172.25.204.4"
jumphost_subnet       = "24"
jumphost_gateway      = "172.25.204.4"

jumphost_user         = "tuadmin"
jumphost_password     = "TU@123"

dns_server_list       = [ "10.11.10.69" ]
dns_suffix_list       = [ "tudc.com" ]

disksize               = "20"

vms = {
  rocky_test_1 = {
    name                = "rocky-1"
    vm_ip               = "172.25.204.49"
  }
}

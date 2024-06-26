
vCenter_user       = "Administrator@vcsa.local"
vCenter_password   = "Tu$P@ssw0rdVr@"
vCenter_server     = "172.25.204.15"

jumphost_ip           = "172.25.204.50"
jumphost_subnet       = "24"
jumphost_gateway      = "172.25.204.1"
jumphost_user         = "tuadmin"
jumphost_password     = "TU@123"

dns_server_list       = [ "10.11.10.69" ]
dns_suffix_list       = [ "tudc.com" ]

disksize               = "40"

vms = {
   "rocky_test_1"= {
    name                = "VM-1"
    vm_ip               = "172.25.204.49"
    cpu                 = 2
    memory              = 1024
    disksize            = 40
    guest_id            = "ubuntu64Guest"
    ipv4_netmask        = 24
    ipv4_gateway        = "172.25.204.1"
    username            = "kube-spray"
    password            = "12345"
  }
   "rocky_test_2"= {
    name                = "VM-2"
    vm_ip               = "172.25.204.50"
    cpu                 = 2
    memory              = 1024
    disksize            = 40
    guest_id            = "ubuntu64Guest"
    ipv4_netmask        = 24
    ipv4_gateway        = "172.25.204.1"
    username            = "kube-spray"
    password            = "12345"
  }
}

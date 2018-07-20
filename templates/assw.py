# -*- coding: UTF-8 -*-
#24p-assw-template

def conf(sw_sysname,IPv30,i):
    
    conf ='''admin
admin@huawei.com
y
admin@huawei.com
<password>
<password>

sys
sysname '''+sw_sysname+'''
lldp enable
#
#
stp region-configuration
region-name mstp
revision-level 1
instance 1 vlan 1 to 4094
active region-configuration
#
radius-server template default
#

vlan 30
desc MangerVlan
vlan 70
desc Printer
vlan 90
desc IT-Services
vlan 110
desc BMS/Security
aaa
local-user admin privilege level 15
local-user admin service-type terminal ssh
#
ntp-service ipv6 server disable    
y       
ntp-service unicast-server 10.4.16.34

#
interface Vlanif30
desc Manage
ip address '''+str(list(IPv30)[i+4])+' '+str(IPv30.prefixlen)+'''

interface Eth-Trunk1
des up-link-g0/0/25-26
port link-type trunk
port trunk allow-pass vlan all
mode lacp
 
 
#
interface GigabitEthernet0/0/23
port link-type trunk
port trunk allow-pass vlan all
interface GigabitEthernet0/0/24
port link-type trunk
port trunk allow-pass vlan all
#
interface GigabitEthernet0/0/25 
eth-trunk 1
interface GigabitEthernet0/0/26
eth-trunk 1
int range g0/0/1 to g0/0/22
port link-type acc
port def vlan 110
qu
snmp-agent 
snmp-agent community read cipher <snmp-community>
snmp-agent sys-info version v2c v3

ip route-static 0.0.0.0 0.0.0.0 '''+str(list(IPv30)[1])+'''
#
stelnet server enable
ssh authentication-type default password  
#
user-interface con 0
authentication-mode password 
set authentication password 
<password>
<password>

user-interface vty 0 4
authentication-mode aaa
protocol inbound all

run save
y
#
'''
    return conf

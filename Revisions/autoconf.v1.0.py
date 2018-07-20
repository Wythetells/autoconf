#!/usr/bin/python
# -*- coding: UTF-8 -*- 
#conf 生成测试/22

import os
from netaddr import *
from templates  import (csw,asw,asww,dhcpd)
#------定义区----------
OfficeNetwork='10.2.44.0/22'
IPv700=IPNetwork('172.16.52.0/23')
OfficeCode='CNQD1'
Floor='44F'
#asw&asww
Asw_Num='7'
#----------------------

ip=IPNetwork(OfficeNetwork)
if ip.prefixlen == 22:
	IP_uplink = list(list(ip.subnet(29))[0])[6]
	IP_gateway= list(ip.subnet(29))[0]
	IPv70     = list(ip.subnet(28))[1]
	IPv90     = list(ip.subnet(28))[2]
	IPv60     = list(ip.subnet(28))[3]
	IPv110    = list(ip.subnet(27))[2]
	IPv30 	  = list(ip.subnet(27))[3]
	IPv201 	  = list(ip.subnet(25))[1]
	IPv800 	  = list(ip.subnet(24))[1]
	IPv802 	  = list(ip.subnet(24))[2]
	IPv803 	  = list(ip.subnet(24))[3]
elif ip.prefixlen == 21:
	IP_uplink = list(list(ip.subnet(29))[0])[6]
	IP_gateway= list(ip.subnet(29))[0]
	IPv70     = list(ip.subnet(28))[1]
	IPv90     = list(ip.subnet(28))[2]
	IPv60     = list(ip.subnet(28))[3]
	IPv110    = list(ip.subnet(27))[2]
	IPv30 	  = list(ip.subnet(25))[1]
	IPv201    = list(ip.subnet(24))[1]
	IPv800    = list(ip.subnet(23))[1]
	IPv802    = list(ip.subnet(23))[2]
	IPv803    = list(ip.subnet(23))[3]
elif ip.prefixlen == 20:
	IP_uplink = list(list(ip.subnet(29))[0])[6]
	IP_gateway= list(ip.subnet(29))[0]
	IPv70     = list(ip.subnet(28))[1]
	IPv90     = list(ip.subnet(28))[2]
	IPv60     = list(ip.subnet(28))[3]
	IPv110    = list(ip.subnet(27))[2]
	IPv30 	  = list(ip.subnet(25))[1]
	IPv201    = list(ip.subnet(24))[1]
	IPv800    = list(ip.subnet(22))[1]
	IPv802    = list(ip.subnet(22))[2]
	IPv803    = list(ip.subnet(22))[3]
else :
	print('network\'s subnet error!')
IPv300 = list(IPNetwork('192.168.60.0/23'))[1]
IPv600 = list(IPNetwork('192.168.100.0/24'))[1]

csw_sysname = OfficeCode+'-'+Floor+'-'+'CSW01'
cswconf = csw.conf(csw_sysname,IP_uplink,IP_gateway,IPv30,IPv60,IPv70,IPv90,IPv110,IPv201,IPv800,IPv802,IPv803,IPv700)
dhcpconf=dhcpd.conf(IP_gateway,IPv60,IPv70,IPv90,IPv110,IPv201,IPv800,IPv802,IPv803,IPv700)

os.mkdir(os.path.join(os.path.abspath('.'), OfficeCode))

fo = open(OfficeCode+'/'+csw_sysname, "w")
fo.write(cswconf)
fo.close()

fo = open(OfficeCode+'/dhcpd.conf', "w")
fo.write(dhcpconf)
fo.close()

for i in range(int(Asw_Num)):
	if (i+1)==int(Asw_Num):
		asw_sysname=OfficeCode+'-'+Floor+'-'+'ASWW01'
		aswconf=asww.conf(asw_sysname,IPv30,i)
	else:
		asw_sysname=OfficeCode+'-'+Floor+'-'+'ASW0'+str(i+1)
		aswconf=asw.conf(asw_sysname,IPv30,i)
		
	fo = open(OfficeCode+'/'+asw_sysname, "w")
	fo.write(aswconf)
	fo.close()

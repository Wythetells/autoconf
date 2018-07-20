#!/usr/bin/python
# -*- coding: UTF-8 -*- 
#conf 生成测试/22

import os
import sys
sys.path.append(r'/autoconf/') 
from netaddr import *
from templates  import (csw,csw_stack_a,csw_stack_b,asw,asw_other,dsw,asww,assw,dhcpd)

#------定义区----------
#当前仅支持华为交换机配置生成！
#每层楼固定生成asw，asww，assw配置，
OfficeNetwork='10.2.44.0/20'
IPv700=IPNetwork('172.16.52.0/23')
OfficeCode='CNQD1'
#CSW是否堆叠，1是 0否 
stack=0
#楼层号，核心所在楼层放在首位
floor =(18,15,16,17,19,20,21,22)
#每楼层交换机数目asw，2台及以上自动增加dsw配置
sw_num=(10,9,8,9,8,10,10,10)
#默认ASW起始IP，一般不需修改
sw_ip_start=130
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
#	
IPv300 = list(IPNetwork('192.168.60.0/23'))[1]
IPv600 = list(IPNetwork('192.168.100.0/24'))[1]

def writeconf(sw_sysname,swconf):
	fo = open(OfficeCode+'/'+sw_sysname, "w")
	fo.write(swconf)
	fo.close()

#创建配置文件目录
os.mkdir(os.path.join(os.path.abspath('.'), OfficeCode))

csw_sysname = OfficeCode+'-'+str(floor[0])+'F-'+'CSW'
if stack == 1:
	cswconf = csw-stack-a.conf(csw_sysname,IP_uplink,IP_gateway,IPv30,IPv60,IPv70,IPv90,IPv110,IPv201,IPv800,IPv802,IPv803,IPv700)
	writeconf(csw_sysname,cswconf)
	cswconf = csw-stack-b.conf()
	writeconf(csw_sysname,cswconf)
elif stack ==0:
	cswconf = csw.conf(csw_sysname,IP_uplink,IP_gateway,IPv30,IPv60,IPv70,IPv90,IPv110,IPv201,IPv800,IPv802,IPv803,IPv700)
	writeconf(csw_sysname,cswconf)
	
#生成dhcpd.conf配置
dhcpconf=dhcpd.conf(IP_gateway,IPv60,IPv70,IPv90,IPv110,IPv201,IPv800,IPv802,IPv803,IPv700)
fo = open(OfficeCode+'/dhcpd.conf', "w")
fo.write(dhcpconf)
fo.close()
#sw数，用于计算swIP
sw_sum=0
#sw互联光模块数
sw_mod=0

for f in floor: 			#循环读取楼层号
	swn=sw_num[floor.index(f)]#当前楼层接入交换机数量
	if floor.index(f) == 0: #如果是元组第一个元素，默认为核心所在楼层，则无dsw
		for i in range(swn): 
			sw_sysname=OfficeCode+'-'+str(f)+'F-ASW0'+str(i+1)
			swconf=asw.conf(sw_sysname,IPv30,sw_sum)
			writeconf(sw_sysname,swconf)
			sw_sum=sw_sum+1
			sw_mod+=4
		sw_mod+=12
	else:
		if swn == 1:#如果分楼层1台交换机
			#生成asw配置
			sw_sysname=OfficeCode+'-'+str(f)+'F-ASW01'
			swconf=asw.conf(sw_sysname,IPv30,sw_sum)
			writeconf(sw_sysname,swconf)
			sw_sum=sw_sum+1
		else:	
			swn+=2 #否则，增加两台DSW
			for i in range(swn):  #读取当前楼层交换机数
				if i == 0: #如果是前两台交换机，生成dsw配置
					sw_sysname=OfficeCode+'-'+str(f)+'F-DSW01'
					swconf=dsw.conf(sw_sysname,IPv30,sw_sum)
				elif i == 1:
					sw_sysname=OfficeCode+'-'+str(f)+'F-DSW02'
					swconf=dsw.conf(sw_sysname,IPv30,sw_sum)
				else: 				#否则，生成asw配置
					sw_sysname=OfficeCode+'-'+str(f)+'F-ASW0'+str(i-1)
					swconf=asw_other.conf(sw_sysname,IPv30,sw_sum)
					
				writeconf(sw_sysname,swconf)
				sw_sum=sw_sum+1
		sw_mod+=4
	#生成asww配置
	sw_sysname=OfficeCode+'-'+str(f)+'F-ASWW01'
	swconf=asww.conf(sw_sysname,IPv30,sw_sum)
	writeconf(sw_sysname,swconf)
	sw_sum=sw_sum+1
	#生成assw配置
	sw_sysname=OfficeCode+'-'+str(f)+'F-ASSW01'
	swconf=assw.conf(sw_sysname,IPv30,sw_sum)
	writeconf(sw_sysname,swconf)
	sw_sum=sw_sum+1
	
readme='光模块数量为'+str(sw_mod)
fo = open(OfficeCode+'/readme', "w")
fo.write(readme)
fo.close()


'''
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
'''

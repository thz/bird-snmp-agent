#!/usr/bin/python
#
# Copyright (c) 2016 Travelping GmbH <copyright@travelping.com>
# by Tobias Hintze <tobias.hintze@travelping.com>
#
# This code is inspired and partially copied from 
# https://r3blog.nl/index.php/archives/2011/02/24/bgp4-mib-support-for-bird/
# That original code does not clearly declare any license.
# 
# This code also uses python-agentx library licensed under GPLv3
# (see agentx.py for details)
#
# So this code is licensed under the GPLv3 (see COPYING.GPLv3).
#

from adv_agentx import AgentX
from adv_agentx import SnmpGauge32, SnmpCounter32, SnmpIpAddress
import time, os

from birdagent import BirdAgent

## handle get and getnext requests
def OnSnmpRead(req, ax, axd):
	pass

# handle set requests
def OnSnmpWrite(req, ax, axd):
	pass

# handle get, getnext and set requests
def OnSnmpRequest(req, ax, axd):
	pass

## initialize any ax and axd dependant code here
def OnInit(ax, axd):
	pass

## register some variables
## this function is called when a new snmp request has been received and
## if CacheInterval has expired at that time
def OnUpdate(ax, axd, state):
	print('updated bird-ospf state: {0}'.format(time.time()))
	## register variables
	axd.RegisterVar('ospf', 0)

	axd.RegisterVar("ospfNbrEntry.%s"%"10.10.1.2",SnmpIpAddress("10.10.1.2"))
	axd.RegisterVar("ospfNbrState.%s"%"10.10.1.2",4)
	return
	"""
	for nbrid in sorted(state["ospf-neighbors"].keys()), BirdAgent.ipCompare):
			oid = "%s.%s"%(snmpkey, peer)
			if peers[peer].has_key(snmpkey):
				axd.RegisterVar(oid, peers[peer][snmpkey])
			else:
				axd.RegisterVar(oid, BirdAgent.bgp_defaults[snmpkey])
	return
	"""


# main program
if __name__ == '__main__':
	print('bird-ospf AgentX starting')

	bird = BirdAgent( \
			os.environ.get("BIRDCONF") or "/etc/bird/bird.conf", \
			os.environ.get("BIRDCPATH") or "/usr/sbin/birdc", \
			os.environ.get("NETSTATCMD") or "netstat -na")

	instance = "o_main"

	callbacks = {
			"OnSnmpRead"    : OnSnmpRead,
			"OnSnmpWrite"   : OnSnmpWrite,
			"OnSnmpRequest" : OnSnmpRequest,
			"OnInit"        : OnInit,
			"OnUpdate"      : lambda ax, axd: OnUpdate(ax,axd,bird.getOSPFState(instance))
			}

	## initialize agentx module and run main loop
	AgentX(
		callbacks,
		Name		= 'bird-ospf',
		#RootOID = '1.3.6.1.2.1.14',
		MIBFile		= os.environ.get("OSPFMIBFILE") or "/usr/share/bird-snmp/OSPF-MIB.txt",
		RootOID = 'OSPF-MIB::ospf',
		CacheInterval	= int(os.environ.get("AGENTCACHEINTERVAL") or "30")
	)
	print('bird-ospf AgentX terminating')

# vim:ts=4:sw=4:noexpandtab

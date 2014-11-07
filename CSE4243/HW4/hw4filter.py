#!/usr/bin/env python3

from urllib.request import urlopen as fetchurl
import pickle
import os.path as path
from ipaddress import ip_address as ipaddr
from socket import getaddrinfo as resolve
from socket import gethostbyaddr as unresolve

# This need not be called by the user.
# Doing so anyway shouldn't break anything, though.
def hostfilter_init():
	global hostdeny
	hostdeny = []
	if (path.isfile(path.expanduser("~/.jam927_hostdeny2"))):
		conf_file = open(path.expanduser("~/.jam927_hostdeny2"), "rb")
		hostdeny = pickle.load(conf_file)
		conf_file.close()
	else:
		conf_file = open(path.expanduser("~/.jam927_hostdeny2"), "wb")
		pickle.dump(hostdeny, conf_file)
		conf_file.close()

def add_host(hoststr):
	try:
		hostdeny
	except:
		hostfilter_init()
	host = ''
	try:
		host = str(ipaddr(hoststr))
	except:
		host = hoststr
	if host in hostdeny:
		raise Exception("This host already exists in the configuration.")
	else:
		hostdeny.append(host)
		conf_file = open(path.expanduser("~/.jam927_hostdeny2"), "wb")
		pickle.dump(hostdeny, conf_file)
		conf_file.close()

def remove_host(hoststr):
	try:
		hostdeny
	except:
		hostfilter_init()
	host = ''
	try:
		host = str(ipaddr(hoststr))
	except:
		host = hoststr
	if host not in hostdeny:
		raise Exception("This host does not exist in the configuration.")
	else:
		hostdeny.remove(host)
		conf_file = open(path.expanduser("~/.jam927_hostdeny2"), "wb")
		pickle.dump(hostdeny, conf_file)
		conf_file.close()

def get_blacklist():
	try:
		hostdeny
	except:
		hostfilter_init()
	hoststringlist = []
	for host in hostdeny:
		hoststringlist.append(host)
	return hoststringlist

def get_web_index(hoststr):
	try:
		hostdeny
	except:
		hostfilter_init()
	try:
		host = str(ipaddr(hoststr))
	except:
		host = hoststr
	if host in hostdeny:
		raise Exception("This host has been added to the hostfilter.")
	ipaddrs = []
	try:
		ipaddrs.append(str(ipaddr(host)))
	except:
		try:
			gunk = resolve(hoststr, 80)
		except:
			pass
		else:
			for ipset in gunk:
				ip = ipaddr(ipset[-1][0])
				if str(ip) not in ipaddrs:
					ipaddrs.append(str(ip))
	if (len(hostdeny) > len(list(set(hostdeny) - set(ipaddrs)))):
		raise Exception("This host resolves to at least one blacklisted host.")
	else:
		hosts = []
		try:
			gunk = unresolve(hoststr)
		except:
			pass
		else:
			hosts.append(gunk[0])
			for host in gunk[1]:
				hosts.append(host)
		if (len(hostdeny) > len(list(set(hostdeny) - set(hosts)))):
			raise Exception("This host resolves to at least one blacklisted host.")
	try:
		index = fetchurl("http://"+hoststr)
	except Exception as e:
		return "No page"
	html = index.read()
	return html


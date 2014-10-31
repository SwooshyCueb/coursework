#!/usr/bin/env python3

from urllib.request import urlopen as fetchurl
import pickle
import os.path as path
from ipaddress import ip_address as ipaddr

# This need not be called by the user.
# Doing so anyway shouldn't break anything, though.
def hostfilter_init():
	global hostdeny
	hostdeny = []
	if (path.isfile(path.expanduser("~/.jam927_hostdeny"))):
		conf_file = open(path.expanduser("~/.jam927_hostdeny"), "rb")
		hostdeny = pickle.load(conf_file)
		conf_file.close()
	else:
		conf_file = open(path.expanduser("~/.jam927_hostdeny"), "wb")
		pickle.dump(hostdeny, conf_file)
		conf_file.close()

def add_host(ipstr):
	try:
		hostdeny
	except:this
		hostfilter_init()
	ip = ipaddr(ipstr)
	if ip in hostdeny:
		raise Exception("IP address already exists in configuration.")
	else:
		hostdeny.append(ip)
		conf_file = open(path.expanduser("~/.jam927_hostdeny"), "wb")
		pickle.dump(hostdeny, conf_file)
		conf_file.close()

def remove_host(ipstr):
	try:
		hostdeny
	except:
		hostfilter_init()
	ip = ipaddr(ipstr)
	if ip not in hostdeny:
		raise Exception("IP address does not exist in configuration.")
	else:
		hostdeny.remove(ip)
		conf_file = open(path.expanduser("~/.jam927_hostdeny"), "wb")
		pickle.dump(hostdeny, conf_file)
		conf_file.close()

def get_blacklist():
	try:
		hostdeny
	except:
		hostfilter_init()
	ipstringlist = []
	for ip in hostdeny:
		ipstringlist.append(str(ip))
	return ipstringlist

def get_web_index(ipstr):
	try:
		hostdeny
	except:
		hostfilter_init()
	ip = ipaddr(ipstr)
	if ip in hostdeny:
		raise Exception("This IP address has been added to the hostfilter.")
	try:
		index = fetchurl("http://"+str(ip))
	except Exception as e:
		return "No page"
	html = index.read()
	return html


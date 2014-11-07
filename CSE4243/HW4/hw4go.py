#!/usr/bin/env python3

from hw3filter import add_host, remove_host, get_blacklist, get_web_index

mate_hn = "mate-desktop.org"
mate_ip = "79.133.49.138"
# These resolve into each other just fine

google_hn = "google.com"
google_ip1 = "74.125.228.2"
google_ip2 = "74.125.228.14"
google_ip1_hn = "iad23s05-in-f2.1e100.net"
google_ip2_hn = "iad23s05-in-f14.1e100.net"
# Google's FQDN resolves to a plethora of IP addresses. I picked two at random.
# Neither resolve back to google.com, but the hostnames they give to resolve
# back to the IP addresses at this time of writing.

twitter = "199.59.148.10"
# Twitter 404s when you try to go directly to the IP address.
# Or it did when I wrote this script anyway.



try:
	print("Removing " + mate_hn + " from hostfilter")
	remove_host(mate_hn)
except Exception as e:
	print("Exception: " + format(e))
else:
	print(mate_hn + " removed from hostfilter")
print("")

try:
	print("Fetching index from " + mate_hn)
	mate = get_web_index(mate_hn)
except Exception as e:
	print("Exception: " + format(e))
else:
	print(mate[0:79])
# I think 80 characters is enough to print
print("")

try:
	print("Adding " + mate_hn + " to hostfilter")
	add_host(mate_hn)
except Exception as e:
	print("Exception: " + format(e))
else:
	print(mate_hn + " added to hostfilter")
print("")

try:
	print("Adding " + mate_hn + " to hostfilter")
	add_host(mate_hn)
except Exception as e:
	print("Exception: " + format(e))
else:
	print(mate_hn + " added to hostfilter")
print("")

print("Fetching index from " + twitter)
print(get_web_index(twitter)[0:79])
print("")

print("Fetching blacklist")
print(str(get_blacklist()))
print("")

try:
	print("Fetching index from " + mate_ip)
	mate = get_web_index(mate_ip)
except Exception as e:
	print("Exception: " + format(e))
else:
	print(mate[0:79])
print("")

try:
	print("Removing " + mate_hn + " from hostfilter")
	remove_host(mate_hn)
except Exception as e:
	print("Exception: " + format(e))
else:
	print(mate_hn + " removed from hostfilter")
print("")

try:
	print("Adding " + google_ip1 + " to hostfilter")
	add_host(google_ip1)
except Exception as e:
	print("Exception: " + format(e))
else:
	print(google_ip1 + " added to hostfilter")
print("")

try:
	print("Fetching index from " + google_hn)
	goog = get_web_index(google_hn)
except Exception as e:
	print("Exception: " + format(e))
else:
	print(goog[0:79])
# I think 80 characters is enough to print
print("")

try:
	print("Removing " + google_ip1 + " from hostfilter")
	remove_host(google_ip1)
except Exception as e:
	print("Exception: " + format(e))
else:
	print(google_ip1 + " removed from hostfilter")

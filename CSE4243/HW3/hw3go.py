#!/usr/bin/env python3

from hw3filter import add_host, remove_host, get_blacklist, get_web_index

mate = "79.133.49.138"
twitter = "199.59.148.10"
# Twitter 404s when you try to go directly to the IP address.
# Or it did when I wrote this script anyway.

try:
	print("Removing " + mate + " from hostfilter")
	remove_host(mate)
except Exception as e:
	print("Exception: " + format(e))
else:
	print(mate + " removed from hostfilter")
print("")

print("Fetching index from " + mate)
print(get_web_index(mate)[0:79])
# I think 80 characters is enough to print
print("")

try:
	print("Adding " + mate + " to hostfilter")
	add_host(mate)
except Exception as e:
	print("Exception: " + format(e))
else:
	print(mate + " added to hostfilter")
print("")

try:
	print("Adding " + mate + " to hostfilter")
	add_host(mate)
except Exception as e:
	print("Exception: " + format(e))
else:
	print(mate + " added to hostfilter")
print("")

print("Fetching index from " + twitter)
print(get_web_index(twitter)[0:79])
print("")

print("Fetching blacklist")
print(str(get_blacklist()))
print("")

try:
	print("Fetching index from " + mate)
	nginx = get_web_index(mate)
except Exception as e:
	print("Exception: " + format(e))
else:
	print(nginx)
print("")

try:
	print("Removing " + mate + " from hostfilter")
	remove_host(mate)
except Exception as e:
	print("Exception: " + format(e))
else:
	print(mate + " removed from hostfilter")

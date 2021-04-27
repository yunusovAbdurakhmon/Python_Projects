#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-i", "--interface", dest="interface", help="Interface to change its Mac address")
	parser.add_option("-m", "--macc", dest="new_mac", help="New Mac address")
	(options, arguments) = parser.parse_args()
	if not options.interface:
		parser.error("Please, specify the interface, --info for more information")
	elif not options.new_mac:
		parser.error("Please, specify a new_mac, --info for more information")
	return options

def change_mac(interface, new_mac):
	print("[+] Changing MAC address for " + interface + " to " + new_mac)

	subprocess.call(["ifconfig", interface, "down"])
	subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
	subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
	# Execute and Reading info from ifconfig
	ifconfig_result = subprocess.check_output(["ifconfig", interface])
	# Reading mac_address from output

	mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result)) #re.search(String, String) or re.search(Byte_like, byte_like)
	if mac_address_search_result:
		return mac_address_search_result.group(0)
	else:
		print("[-] Could not read MAC address")





options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))
change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
	print("[+] MAC address was successfully changed to " + current_mac)
else:
	print("[-] MAC address did not get changed.")



















#arser = optparse.OptionParser()
# parser is an instance of OptionParser class

#parser.add_option("-i", "--interface", dest="interface", help="Interface to change its Mac address")
#parser.add_option("-m", "--macc", dest="new_mac", help="New Mac address")

#(options, arguments) = parser.parse_args()


#interface = options.interface
# interface is  just a variable name. It can be anything!!!

#new_mac = options.new_mac





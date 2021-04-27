#!/usr/bin/env python

import scapy.all as scapy
import argparse


def get_ip_range():
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--target", dest="ip_range", help="IP range to go through and match")
	options = parser.parse_args()
	if not options.ip_range:
		parser.error("Please, specify the IP range, --info for more information")
	return options


def scan(ip):
	#scapy.arping(ip)
	#arp_request = scapy.ARP(pdst=ip)   ==	arp_request = scapy.ARP()
	#					arp_request.pdst = ip 	
	#scapy.ls(scapy.ARP())	 -- to list all the fields of the object
	#print(arp_request.summary())
	#arp_request.show() - shows info from the objects
	arp_request = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_request_broadcast = broadcast/arp_request
	answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0] #sends ARP request and receives ARP respond. [0] - taking 1st list from 2 answered and unanswered lists
	
	
	
	clients_list = []	
	for element in answered_list:
		client_dict = {"ip" : element[1].psrc, "mac" : element[1].hwsrc}
		clients_list.append(client_dict)  # list.append() - adds dictionary(treeList) to the list(array)
	
	return clients_list

def print_result(clients_list):
	print("IP\t\t\tMAC Address\n------------------------------------------------------")
	for client in clients_list:
		print(client["ip"] + "\t\t" + client["mac"])		
		

options = get_ip_range()	
scan_result = scan(options.ip_range) 
print_result(scan_result)

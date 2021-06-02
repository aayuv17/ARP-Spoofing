
# ARP-Spoofing
Simulating a man-in-the-middle attack using ARP Spoofing.

## Introduction
Our main objective here is to intercept TCP communications between a client & server node using the ARP Spoofing attack. We use three machines, a client, a TCP server & an attacker to carry out this attack. TCP packets exchanged between the client and the server are sniffed & logged by the attacker. Since the client and server are not communicating over an encrypted channel, we are easily able to obtain the actual data being transmitted by logging raw TCP packets from the stream. Wireshark can be used for verification & further analysis.

## Tools Used
- Python's Scapy module
- Wireshark

## Usage
- Run ARP_Spoof.py on your attacker machine
- Run server.py on your server machine
- Run client.py on your client machine and start communicating with the server

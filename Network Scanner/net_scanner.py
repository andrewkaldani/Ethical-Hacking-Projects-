#!/usr/bin/env python
import scapy.all as scapy
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP / IP range.")
    options, arguments = parser.parse_args()
    return options

def scan(ip):
    #specifies the IP field(ARP asks for specific IP ) 
    #creating an ARP packet using scapy class
    arp_request = scapy.ARP(pdst=ip)
    #Create an Ethernet frame that will be sent to Broadcast MAC address(set mac address to broadcast mac address) 
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #combines both frames 
    arp_request_broadcast = broadcast/arp_request
    #represent answered packets(scrapy.srp() prints two lists one which is answered devices and the other  IP addresses of those devices didnt respond)
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    #dictionary with ip addresses and mac addresses
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(results_list):
    print("IP\t\t\tMAC Address\n-------------------------------------")
    #iterate over the list
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)

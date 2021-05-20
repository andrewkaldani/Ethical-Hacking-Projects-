#!/usr/bin/env python
#MAC ADDRESS CHANGER FOR LINUX 

import subprocess
import optparse
import re

def get_arguments():
    #creates an option instance of optparse class
    parser = optparse.OptionParser()
    #which network interface user wishes to change
    parser.add_option("-i", "--interface", dest="interface", help="interface to change Mac Address ")
    #new mac address
    parser.add_option("-m", "--mac", dest="new_mac", help="New Mac Address ")
    #understand what the user enters
    (options, arguments) = parser.parse_args()
    if not options.interface:
       # code to handle error
       parser.error("[-]Please specify an interface! use --help")
    elif not options.new_mac:
       #code to handle error
       parser.error("[-]Please specify an interface! use --help")
    return options


def change_mac(interface,new_mac):
    print("[+] Changing Mac Address for " + interface + " changing to "+new_mac)
    #Execute instructions to change mac address
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    #regex to find and filter for mac address 
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    # code to check if the mac address was found 
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-]Could not read the mac address!")
        
#returns the value from get_arguments
options= get_arguments()
#returns the current mac address
current_mac=get_current_mac(options.interface)
#prints current mac addtess
print("[+]Current Mac = "+str(current_mac))
#calls the function to change the mac address
change_mac(options.interface, options.new_mac)
#assigns new mac address to current_mac
current_mac=get_current_mac(options.interface)
#check if the changed mac address equal to current one
if(current_mac==options.new_mac):
    print("[+]Mac address was changed "+current_mac)
else:
    print("[+]mac address could not be changed")


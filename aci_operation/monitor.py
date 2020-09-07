# This is a simple python library to make a REST API call to Cisco APIC
# and show interface throughput statistics

import json
from aci_operation import utils as utils

def print_header():
# Purpose: Print table header
    print ("|" + "Interface".ljust(24) + "|" + "Ing Bps".rjust(10) \
        +"|" + "Eg Bps".rjust(10) + "|" + "Ing Pps".rjust(10) \
        +"|" + "Eg Pps".rjust(10) + "|")

def print_break():
# Purpose: Print line break
    fmt_line = '+{:-<24}+{:->10}+{:->10}+{:->10}+{:->10}+'
    print (fmt_line.format("-", "-", "-", "-", "-"))

def show_port_stats(session, apic_ip, port_list):
# Purpose:  For each port in the port_list, send REST API call to APIC 
#           to query interface statistics
# Input:    session: a session from requests library
#           port_list: a list of port read from intf_list.json file
# Future:   This function will be made more generic.
    fmt = '|{:<24}|{:>10}|{:>10}|{:>10}|{:>10}|'  # Output format
    print_header()
    print_break()
    for port in port_list:
        pod = port['pod']
        node = port['node']
        interface = port['interface']
        # GET HDeqptIngrTotal5min-0.json (Ingress)
        # This can be supplied as a function parameter in later version
        response_body = session.get(apic_ip 
                        + '/api/mo/topology/pod-' + pod 
                        + '/node-' + node 
                        + '/sys/phys-[eth' + interface 
                        + ']/HDeqptIngrTotal5min-0.json'
                        , verify=False)
        # if apic return any errors, break
        if (response_body.status_code != 200):
            print ("REST call error")
            break
        
        # Load ingress values
        ingr_total = json.loads(response_body.text)["imdata"]
        # GET HDeqptEgrTotal5min-0.json (Egress)
        # This can be supplied as a function parameter in later version
        response_body = session.get(apic_ip 
                        + '/api/mo/topology/pod-' + pod 
                        + '/node-' + node 
                        + '/sys/phys-[eth' + interface 
                        + ']/HDeqptEgrTotal5min-0.json'
                        , verify=False)
        # if apic return any errors, break
        if (response_body.status_code != 200):
            print ("REST call error")
            break
        # Load egress values
        egr_total = json.loads(response_body.text)["imdata"]
        # If there's a query result, print in proper format.  
        if (json.loads(response_body.text)["totalCount"]=="1"):
            ingr_output = ingr_total[0]['eqptIngrTotalHist5min']["attributes"]["bytesRate"]
            ingr_output = utils.human_format(float(ingr_output))
            ingr_pkts_rate = utils.human_format(float(ingr_total[0]['eqptIngrTotalHist5min']["attributes"]["pktsRate"]))
            egr_output = egr_total[0]['eqptEgrTotalHist5min']["attributes"]["bytesRate"]
            egr_output = utils.human_format(float(egr_output))
            egr_pkts_rate = utils.human_format(float(egr_total[0]['eqptEgrTotalHist5min']["attributes"]["pktsRate"]))
            print (fmt.format(pod + '/' + node + '/' + interface, ingr_output, egr_output, ingr_pkts_rate, egr_pkts_rate))
    print_break()


'''
AUTHOR: Trevor Justice
DATE: 03-21-2024
DESCRIPTION: A program which takes a text file comprised of IP Addresses correlating to routers,
as well as a text file containing IP addresses to be forwarded. It constructs a routing table,
and determines which port each 'packet' should be forwarded to.
'''
from ipaddress import ip_interface
import ipaddress

def read_input_file(input_doc):
    '''
    Reads the file containing IP addresses to be forwarded. Iterates by each line, turning it into
    a list of IP addresses.
    :param input_doc: a text document containing one IP address per line
    :return given_ip_addresses: a list of IP addresses within the text document
    '''
    given_ip_addresses = []
    with open(input_doc) as file:
        for line in file:
            ip_address = ipaddress.IPv4Address(line.strip())
            given_ip_addresses.append(ip_address)
    return given_ip_addresses
def read_setup_file(setup_doc):
    '''
    Reads the text file containing the network info - IP addresses, ports, and prefixes. Extracts
    the information on every line, appending the correct information for each port to a dictionary.
    :param setup_doc: a text file containing information about the network
    :return routing_table: a dictionary containing each port, IP, prefix, and subnet mask respectively
    '''
    routing_table = []

    with open(setup_doc) as file:
        for line in file:
            parts = line.split(',')

            iso_prefix = parts[1].strip().split('/') # this splits the IP from the prefix
            port_number = parts[0].strip()
            ip_address = ipaddress.IPv4Address(iso_prefix[0].strip()) # this turns the string into a valid IP address

            if len(iso_prefix) != 2: # checks to see if there is a given prefix
                prefix = 32
            else:
                prefix = int(iso_prefix[1].strip())


            subnet_mask = calc_subnet_mask(prefix) # calculates a subnet mask based on prefix length


            routing_table.append({
                "Port": int(port_number),
                "IP Address": format(ip_address),
                "Prefix": prefix,
                "Subnet Mask": subnet_mask
            })


    return routing_table

def calc_subnet_mask(prefix):
    '''
    Calculates the subnet mask based on the size of a given prefix.
    :param prefix: an integer representing the prefix
    :return subnet_mask: an IPv4 address mask
    '''
    subnet_mask_sig_figs = prefix
    subnet_mask_length = 32
    subnet_mask = ''

    subnet_mask = subnet_mask.join(('1'*subnet_mask_sig_figs)+('0'*(subnet_mask_length-subnet_mask_sig_figs))) #calculates the subnet mask in binary
    subnet_mask = int(subnet_mask, 2) #turns the binary mask into an integer
    subnet_mask = ipaddress.IPv4Address(subnet_mask) #turns the integer representation into an IPv4 address
    return subnet_mask



def calc_dest_port(routing_table, given_ip):
    '''
    Calculates the destination port of a given IP address. If two ports are returned valid, it
    forwards to the port with the longer prefix.
    :param routing_table: a routing table as constructed above in the program.
    :param given_ip: an IPv4 address
    :return longest_prefix["Port"]: the correct Port number for the given IP to be forwarded to.
    '''
    matches = []

    for route in routing_table: #iterates through the ports in the routing table
        masked_given_ip = apply_subnet_mask(given_ip, route["Subnet Mask"]) #applies subnet mask to given IP

        if ip_interface(masked_given_ip) == ip_interface(route["IP Address"]): #checks to see if IP matches

            matches.append(route)

    longest_prefix = matches[0]

    for match in matches: # calculates which port has the longest prefix
        if match["Prefix"] > longest_prefix["Prefix"]:
            longest_prefix = match

    return longest_prefix["Port"]



def apply_subnet_mask(ip, mask):
    '''
    Applies a subnet mask to a given IP.
    :param ip: a given IPv4 address
    :param mask: a subnet mask in IPv4 format
    :return mask_applied: the given IP address with the mask applied
    '''
    mask_applied = int(ip) & int(mask)
    mask_applied = ipaddress.IPv4Address(mask_applied)
    return mask_applied


def format_routing_table(routing_table):
    '''
    Formats the routing table dictionary into something easier to read
    :param routing_table: a given routing table in the form of a dictionary
    :return:
    '''
    print(f"PORT{' ':14} IP ADDRESS{' ':15} PREFIX{' ':15} SUBNET MASK{' ':15}")
    for entry in routing_table:
        print(f"{entry['Port']}{' ':14} {entry['IP Address']}{' ':15} {entry['Prefix']}{' ':15} {entry['Subnet Mask']}")


def main():
    setup_doc = "routing_info2.txt" #establish which IP address info you would like to use for a routing table
    routing_table = read_setup_file(setup_doc)
    format_routing_table(routing_table)

    input_doc = input("Enter the location of the file containing IP Addresses you would like forwarded: ")
    ips_to_forward = read_input_file(input_doc)
    
    for ip in ips_to_forward:
        correct_port = calc_dest_port(routing_table, ip)
        print("The correct destination port for your given IP Address is: ", correct_port)


if __name__ == "__main__":
    main()


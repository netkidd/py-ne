#!/usr/bin/python

'''
Create a script that connects to two routers and prints out
both the MIB2 sysName and sysDescr.
'''

# Copy the snmp_helper library in the local directory, then import the functions
from snmp_helper import snmp_get_oid, snmp_extract


COMUNITY_STRING = 'galileo'
SNMP_PORT = 161
device_list = ['184.105.247.70', '184.105.247.71']

# A Tuple to identify the target
# a_device = (IP, COMUNITY_STRING, SNMP_PORT)


# Look for system description
sys_descr_OID = '1.3.6.1.2.1.1.1.0'
sys_name_OID = '1.3.6.1.2.1.1.5.0'


for ip in device_list:
    # Create a Tuple to identify the target
    a_device = (ip, COMUNITY_STRING, SNMP_PORT)

    # Query the device. The results is in hexadecimal
    snmp_data = snmp_get_oid(a_device, oid=sys_name_OID)

    # Transform the data in human readable form
    output = snmp_extract(snmp_data)

    print 'System name from ' + ip
    print output + '\n'

    snmp_data = snmp_get_oid(a_device, oid=sys_descr_OID)
    output = snmp_extract(snmp_data)
    print 'System description from ' + ip
    print output + '\n\n'

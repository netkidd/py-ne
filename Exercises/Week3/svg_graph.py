#!/usr/bin/env python
'''
2. Using SNMPv3 create two SVG image files.

The first image file should graph the input and output octets on interface FA4 on pynet-rtr1 every five minutes for an hour.
Use the pygal library to create the SVG graph file. Note, you should be doing a subtraction here (i.e. the input/output octets transmitted during this five minute interval).

The second SVG graph file should be the same as the first except graph the unicast packets received and transmitted.

'''
import time
from snmp_helper import snmp_get_oid, snmp_extract

oids = (
('ifDescr_fa4', '1.3.6.1.2.1.2.2.1.2.5')
('ifInOctets_fa4', '1.3.6.1.2.1.2.2.1.10.5')
('ifInUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.11.5')
('ifOutOctets_fa4', '1.3.6.1.2.1.2.2.1.16.5'),
('ifOutUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.17.5')
)

# SNMP parameters

COMUNITY_STRING = 'galileo'
SNMP_PORT = 161
IP1 = '10.2.52.32'

# A Tuple to identify the target
router1 = (IP1, COMUNITY_STRING, SNMP_PORT)


fa4_in_octects = []
fa4_out_octects = []

fa4_in_packets = []
fa4_out_packets = []

temp = []
counter = 0

# We do a cycle 12 times with a 5 min timeout in order to monitor the devide for one hour (3600 seconds)
while counter < 12:
    # Extract the output value from each OID and store them in a temporary list
    for descr, oid in oids:
        snmp_data = snmp_get_oid(router1, oid=oid)
        output = snmp_extract(snmp_data)
        temp.append(output)

    # Add each value in the correct list
    fa4_in_octects_temp, fa4_out_octects_temp, fa4_in_packets_temp, fa4_out_packets_temp = temp
    fa4_in_octects.append(fa4_in_octects_temp)
    fa4_out_octects.append(fa4_out_octects_temp)
    fa4_in_packets.append(fa4_in_packets_temp)
    fa4_out_packets.append(fa4_out_packets_temp)

    # Reset the temp list, timeout for 5 min and increment the counter
    temp = []
    time.sleep(300)
    counter += 1

# Create a pygal line chart
line_chart = pygal.Line()

# Give a title to the chart
line_chart.title = 'Input/Output Packets and Bytes'

# Specify the values on the x axe. In this case the data was sampled every 5 min for one hour
line_chart.x_labels = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]

# Add a line for each graph we want to draw. Each line will have a title and a list of values
line_chart.add('InPackets', fa4_in_packets)
line_chart.add('OutPackets', fa4_out_packets)
line_chart.add('InBytes', fa4_in_octects)
line_chart.add('OutBytes', fa4_out_octects)

# Save the output in a file. We can open the file with a Browser and display the result
line_chart.render_to_file('InOutPackets-InOutBytes.svg')

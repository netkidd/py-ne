#!/usr/bin/env python

# For python 2.7

'''
1. Using SNMPv3 create a script that detects router configuration changes.

If the running configuration has changed, then send an email notification to yourself identifying the router that changed and the time that it changed.

'''
import time
import email_helper
from snmp_helper import snmp_get_oid, snmp_extract


# Email template to send an email to ourselves in case the configuration changes
sender = 'user@email.com'
recipient = 'user@email.com'
subject = 'SNMP Notification - Configuration changed.'
message = '''

Hi,

The configuration of a monitored device has been changed. See below the details.

'''


# SNMP parameters

COMUNITY_STRING = 'galileo'
SNMP_PORT = 161
IP1 = '10.2.52.32'
IP2 = '10.2.52.33'

# A Tuple to identify the target
router1 = (IP1, COMUNITY_STRING, SNMP_PORT)
router2 = (IP2, COMUNITY_STRING, SNMP_PORT)


#System uptime
sysUptime_oid = '1.3.6.1.2.1.1.3.0'

# Uptime when running config last changed
ccmHistoryRunningLastChanged_oid = '1.3.6.1.4.1.9.9.43.1.1.1.0'

# Uptime when running config last saved (note any 'write' constitutes a save)
ccmHistoryRunningLastSaved_oid = '1.3.6.1.4.1.9.9.43.1.1.2.0'

# Uptime when startup config last saved
ccmHistoryStartupLastChanged_oid = '1.3.6.1.4.1.9.9.43.1.1.3.0'

oids = (sysUptime_oid, ccmHistoryRunningLastChanged_oid, ccmHistoryRunningLastSaved_oid, ccmHistoryStartupLastChanged_oid)


# Initialize the system uptime variable. All the timestamps in the first min will be compared to this value
sysUptime_data = snmp_get_oid(router1, oid=sysUptime_oid)
sysUptime = snmp_extract(sysUptime_data)



def is_config_changed (sysUptime, ccmHistoryRunningLastChanged, ccmHistoryRunningLastSaved, ccmHistoryStartupLastChanged):
    if sysUptime >= ccmHistoryRunningLastChanged:
        return False
    else:
        return True


# TO DO:
# Add loop to probe more than one router, fix print statements, check if config was saved.


while True:
    if time.time() % 60 == 0:
        ccmHistoryRunningLastChanged_data = snmp_get_oid(router1, oid=ccmHistoryRunningLastChanged_oid)
        ccmHistoryRunningLastSaved_data = snmp_get_oid(router1, oid=ccmHistoryRunningLastSaved_oid)
        ccmHistoryStartupLastChanged_data = snmp_get_oid(router1, oid=ccmHistoryStartupLastChanged_oid)

        ccmHistoryRunningLastChanged_output = snmp_extract(ccmHistoryRunningLastChanged_data)
        ccmHistoryRunningLastSaved_output = snmp_extract(ccmHistoryRunningLastSaved_data)
        ccmHistoryStartupLastChanged_output = snmp_extract(ccmHistoryStartupLastChanged_data)

        if is_config_changed(sysUptime, ccmHistoryRunningLastChanged_output, ccmHistoryRunningLastSaved_output, ccmHistoryStartupLastChanged_output):
            message = message + "Device: %s\nCurrent time: %s\nChange done %s seconds ago." % ('Router1', str(time.localtime()[3]) +':'+ str(time.localtime()[4]) +':'+ str(time.localtime()[5], ccmHistoryRunningLastChanged_output/6000)
            email_helper.send_mail(recipient, subject, message, sender)
        else:
            # For troubleshooting
            print 'No changes detected'

        # Reset the system uptime to have a new value to compare
        sysUptime_data = snmp_get_oid(router1, oid=sysUptime_oid)
        sysUptime = snmp_extract(sysUptime_data)

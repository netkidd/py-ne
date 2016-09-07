#!/usr/bin/env python

# For python 2.7

'''
1. Using SNMPv3 create a script that detects router configuration changes.

If the running configuration has changed, then send an email notification to yourself identifying the router that changed and the time that it changed.

'''
import time
import smtplib
from email.mime.text import MIMEText
from snmp_helper import snmp_get_oid, snmp_extract


# Email template to send an email to ourselves in case the configuration changes
sender = 'me@ciao.com'
recipient = 'jakkk.ikkk@yahoo.it'
subject = 'SNMP Notification - Configuration changed.'
message = '''

Hi,

The configuration of a monitored device has been changed. See below the details.

'''




# SNMP parameters

COMUNITY_STRING = 'galileo'
SNMP_PORT = 161
IP1 = '184.105.247.70'
IP2 = '184.105.247.71'

# A Tuple to identify the target
router1 = (IP1, COMUNITY_STRING, SNMP_PORT)
router2 = (IP2, COMUNITY_STRING, SNMP_PORT)
devices = [router1, router2]


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
sysUptimes = []
for device in devices:
    sysUptime_data = snmp_get_oid(device, oid=sysUptime_oid)
    sysUptime = snmp_extract(sysUptime_data)
    sysUptimes.append(sysUptime)



def is_config_changed (sysUptime, ccmHistoryRunningLastChanged, ccmHistoryRunningLastSaved, ccmHistoryStartupLastChanged):
    if sysUptime >= ccmHistoryRunningLastChanged:
        return False
    else:
        return True


# TO DO:
# Add loop to probe more than one router, fix print statements, check if config was saved.


while True:
    if time.time() % 60 == 0:
        for device, sysUptime in zip(devices, sysUptimes):
            ccmHistoryRunningLastChanged_data = snmp_get_oid(device, oid=ccmHistoryRunningLastChanged_oid)
            ccmHistoryRunningLastSaved_data = snmp_get_oid(device, oid=ccmHistoryRunningLastSaved_oid)
            ccmHistoryStartupLastChanged_data = snmp_get_oid(device, oid=ccmHistoryStartupLastChanged_oid)

            ccmHistoryRunningLastChanged_output = snmp_extract(ccmHistoryRunningLastChanged_data)
            ccmHistoryRunningLastSaved_output = snmp_extract(ccmHistoryRunningLastSaved_data)
            ccmHistoryStartupLastChanged_output = snmp_extract(ccmHistoryStartupLastChanged_data)

            if is_config_changed(sysUptime, ccmHistoryRunningLastChanged_output, ccmHistoryRunningLastSaved_output, ccmHistoryStartupLastChanged_output):
                message = message + "\n\nAffected Device: %s\nChanges done less than one minute ago." % (device[0])
                message = MIMEText(message)
                message['Subject'] = subject
                message['From'] = sender
                message['To'] = recipient
            

                # Create SMTP connection object towards the email server (localhost in this case)
                smtp_conn = smtplib.SMTP('localhost')

                # Send the email
                smtp_conn.sendmail(sender, recipient, message.as_string())

                # Close SMTP connection
                smtp_conn.quit()

                print 'Changes'

            else:
                # For troubleshooting
                print 'No changes detected'

        # Reset the system uptime to have a new value to compare
        sysUptimes = []
        for device in devices:
            sysUptime_data = snmp_get_oid(device, oid=sysUptime_oid)
            sysUptime = snmp_extract(sysUptime_data)
            sysUptimes.append(sysUptime)



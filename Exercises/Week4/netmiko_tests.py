from netmiko import ConnectHandler  
from getpass import getpass



'''
5. Use Netmiko to enter into configuration mode on pynet-rtr2. Also use Netmiko to verify your state (i.e. that you are currently in configuration mode).
6. Use Netmiko to execute 'show arp' on pynet-rtr1, pynet-rtr2, and juniper-srx.
7. Use Netmiko to change the logging buffer size (logging buffered <size>) on pynet-rtr2.
8. Use Netmiko to change the logging buffer size (logging buffered <size>) and to disable console logging (no logging console)
   from a file on both pynet-rtr1 and pynet-rtr2 (see 'Errata and Other Info, item #4).
'''

print 'Enter login password'
password = getpass()

print "Enter enable password (if not needed just press Enter)"
enable_secret = getpass()

# The devices are defined as dictionaries
rtr1 = {
    'device_type': 'cisco_ios',
    'ip': '184.105.247.70',
    'username': 'pyclass',
    'password': password,
    'secret': enable_secret
}

rtr2 = {
    'device_type': 'cisco_ios',
    'ip': '184.105.247.71',
    'username': 'pyclass',
    'password': password,
    'secret': enable_secret
}

juniper_srx = {
    'device_type': 'juniper',
    'ip': '184.105.247.76',
    'username': 'pyclass',
    'password': password,
    'secret': enable_secret
}



rtr1_conn = ConnectHandler(**rtr1)
rtr2_conn = ConnectHandler(**rtr2)
juniper_srx_conn = ConnectHandler(**juniper_srx)

print rtr1_conn.find_prompt()
print rtr2_conn.find_prompt()
print juniper_srx_conn.find_prompt()


rtr2_conn.config_mode()

print "On rtr1 are we in config mode?"
print rtr1_conn.check_config_mode()
print "On rtr2 are we in config mode?"
print rtr2_conn.check_config_mode()
print "On juniper_srx are we in config mode?"
print juniper_srx_conn.check_config_mode()

rtr2_conn.exit_config_mode()



show_commands = ['show arp']

output = rtr1_conn.send_command(show_commands[0])
print output

output = rtr2_conn.send_command(show_commands[0])
print output

output = juniper_srx_conn.send_command(show_commands[0])
print output


config_commands = ['logging buffered 64000']

output = rtr2_conn.send_config_set(config_commands)
print output


output = rtr2_conn.send_config_from_file(config_file='config_file.txt')
print output

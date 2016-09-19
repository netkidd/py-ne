
import pexpect
from getpass import getpass

'''
3. Use Pexpect to retrieve the output of 'show ip int brief' from pynet-rtr2.
4. Use PExpect to change the logging buffer size (logging buffered <size>) on pynet-rtr2. Verify this change by examining the output of 'show run'.
'''


rtr2_ip = '184.105.247.71'
rtr2_username = 'pyclass'
rtr2_password = getpass()


ssh_conn = pexpect.spawn('ssh -l {} {}'.format(rtr2_username, rtr2_ip))

ssh_conn.timeout = 5

try:
    ssh_conn.expect('ssword:')
    ssh_conn.sendline(rtr2_password)

    ssh_conn.expect('#')
    ssh_conn.sendline('terminal length 0')
    ssh_conn.expect('#')
    ssh_conn.sendline('show ip int brief')
    ssh_conn.expect('#')
    print ssh_conn.before

except pexpect.TIMEOUT:
    print "One pattern was not found and the connection timed out."




print "\n\n!! And now we change the buffer size !!\n\n"

try:
    ssh_conn.sendline('configure terminal')
    ssh_conn.expect('#')
    ssh_conn.sendline('logging buffered 64000')
    ssh_conn.expect('#')
    ssh_conn.sendline('end')
    ssh_conn.expect('#')
    ssh_conn.sendline('show run')
    ssh_conn.expect('#')
    print ssh_conn.before

except pexpect.TIMEOUT:
    print "One pattern was not found and the connection timed out."

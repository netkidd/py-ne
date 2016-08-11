#!/usr/bin/env python

'''
Write a script that connects using telnet to the router.
Execute the 'show ip int brief' command on the router and return the output.
'''

import telnetlib
import time


TELNET_PORT = 23
TELNET_TIMEOUT = 6


class Device(object):
    def __init__(self, ip_addr, TELNET_PORT=23, TELNET_TIMEOUT=6):
        self.remote_conn = telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)

    def login(self, username, password, TELNET_TIMEOUT=6):
        output = self.remote_conn.read_until("sername:", TELNET_TIMEOUT)
        self.remote_conn.write(username + '\n')
        output += self.remote_conn.read_until("assword:", TELNET_TIMEOUT)
        self.remote_conn.write(password + '\n')
        return output

    def send_command(self, cmd):
        cmd = cmd.strip()
        self.remote_conn.write(cmd + '\n')
        time.sleep(1)
        output = self.remote_conn.read_very_eager()
        return output

    def close_connection(self):
        self.remote_conn.close()


def main():
    ip_addr = '184.105.247.70'
    username = 'pyclass'
    password = '88newclass'

    router1 = Device(ip_addr)
    output = router1.login(username, password)
    print 'After login:'
    print output
    output = router1.send_command('show ip int brief')
    print 'After sending the command:'
    print output

    router1.close_connection()

if __name__ == "__main__":
    main()

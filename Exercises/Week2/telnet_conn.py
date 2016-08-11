#!/usr/bin/env python

'''
Write a script that connects using telnet to the router.
Execute the 'show ip int brief' command on the router and return the output.
'''

import telnetlib
import time


TELNET_PORT = 23
TELNET_TIMEOUT = 6


def login(remote_conn, username, password, TELNET_TIMEOUT):
    output = remote_conn.read_until("sername:", TELNET_TIMEOUT)
    remote_conn.write(username + '\n')
    output += remote_conn.read_until("assword:", TELNET_TIMEOUT)
    remote_conn.write(password + '\n')
    return output


def send_command(remote_conn, cmd):
    cmd = cmd.strip()
    remote_conn.write(cmd + '\n')
    time.sleep(1)
    output = remote_conn.read_very_eager()
    return output


def main():
    ip_addr = '184.105.247.70'
    username = 'pyclass'
    password = '88newclass'

    remote_conn = telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)
    output = login(remote_conn, username, password, TELNET_TIMEOUT)
    print 'After login:'
    print output
    output = send_command(remote_conn, 'show ip int brief')
    print 'After sending the command'
    print output

    remote_conn.close()

if __name__ == "__main__":
    main()

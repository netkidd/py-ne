import paramiko
from getpass import getpass
import time
'''
1. Use Paramiko to retrieve the entire 'show version' output from pynet-rtr2.
2. Use Paramiko to change the 'logging buffered <size>' configuration on pynet-rtr2. This will require that you enter into configuration mode.
'''

rtr2_ip = '184.105.247.71'
rtr2_username = 'pyclass'
rtr2_password = getpass()



def main():
    remote_conn_pre = paramiko.SSHClient()

    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    remote_conn_pre.connect(rtr2_ip, username=rtr2_username, password=rtr2_password, look_for_keys=False, allow_agent=False,)

    remote_conn = remote_conn_pre.invoke_shell()


    output = remote_conn.recv(5000)

    remote_conn.send("terminal length 0\n")
    time.sleep(1)

    remote_conn.send("show version\n")
    time.sleep(1)


    MAX_BUFFER = 65535
    while remote_conn.recv_ready():
        output += remote_conn.recv(MAX_BUFFER)
    print output

    print "\n\n!! And now we change the buffer size !!\n\n"

    remote_conn.send("configure terminal\n")
    time.sleep(1)

    remote_conn.send("logging buffered 64000\n")
    time.sleep(1)

    while remote_conn.recv_ready():
        output += remote_conn.recv(MAX_BUFFER)
    print output

    remote_conn.close()

if __name__ == "__main__":
    main()

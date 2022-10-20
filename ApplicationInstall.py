import asyncio
import time
import telnetlib
import re
import base64
import paramiko 
import csv

def ApplicationInstall(IP,GUESTSHELL_PORT):
    print("\n============================[ Running ApplicationInstall.py : Installing iperf application on Guestshell ]============================\n")

    # paramiko.util.log_to_file('ssh.log') 
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #client.load_system_host_keys()
    #client.connect('10.197.241.7', 5050, username='cisco123', password='Cisco12345678')
    client.connect(IP,GUESTSHELL_PORT, username='cisco123', password='Lm12345678')

    commands = [
    "whoami",
    "sudo yum install iperf -y",
    "iperf -v"
    ]

    #Printing output
    for command in commands:
        print("-"*10,command, "-"*10)
        stdin, stdout, stderr = client.exec_command(command)
        time.sleep(10)
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            print(err)
    
    print("Completed third script - ApplicationInstall.py\n")

import asyncio
import time
import telnetlib
import re
import base64
import paramiko 
import csv

def configure_device(telnet_ip,telnet_port,IP,GUESTSHELL_PORT,GUESTSHELL_INTERFACE):
    print("\n------------- Configuring the device -------------\n")
    tn = telnetlib.Telnet(telnet_ip,telnet_port)
    print (tn)

    tn.write(b'\r\n\r\n')
    tn.write(b'\r\nen\r\n')
    tn.write(b'\r\nconf t\r\n')

    #IOX
    tn.write(b'\r\niox\r\n')
    time.sleep(5)
    tn.write(b'do sh run | sec iox\r\n')
    
    #VPG
    tn.write(b'\r\nint virtualportgroup0\r\n')
    tn.write(b'ip address 192.168.35.1 255.255.255.0\r\n')
    tn.write(b'ip nat inside\r\n')
    tn.write(b'no shutdown\r\n')
    tn.write(b'exit\r\n')

    #App hosting
    tn.write(b'\r\napp-hosting appid guestshell\r\n')
    tn.write(b'app-vnic gateway1 virtualportgroup 0 guest-interface 0\r\n')
    tn.write(b'guest-ipaddress 192.168.35.2 netmask 255.255.255.0\r\n')
    tn.write(b'app-default-gateway 192.168.35.1 guest-interface 0\r\n')
    tn.write(b'name-server0 64.104.128.236\r\n')
    tn.write(b'exit\r\n')

    #NAT
    nat_command_1="\r\nip nat inside source static tcp 192.168.35.2 22 "+IP+" "+GUESTSHELL_PORT+" extendable\r\n"
    nat_command_2="ip nat inside source static tcp 192.168.35.2 8080 "+IP+" 8080 extendable\r\n"
    nat_command_3="ip nat inside source static tcp 192.168.35.2 8081 "+IP+" 8081 extendable\r\n"
    tn.write(nat_command_1.encode())
    tn.write(nat_command_2.encode())
    tn.write(nat_command_3.encode())
    nat_command_4="ip nat inside source list nat interface "+GUESTSHELL_INTERFACE+" overload\r\n"
    tn.write(nat_command_4.encode())
    tn.write(b'ip access-list extended nat\r\n')
    tn.write(b'10 permit ip 192.168.35.0 0.0.0.255 any\r\n')
    tn.write(b'exit\r\n')
    
    print(tn.read_until(b"10 permit ip 192.168.35.0 0.0.0.255",10).decode('utf-8'))

    #Gi0/0/3 - NAT outside
    #tn.write(b'\r\nint Gi0/0/3\r\n')
    int_command="\r\nint "+GUESTSHELL_INTERFACE+"\r\n"
    tn.write(int_command.encode())
    tn.write(b'ip nat outside\r\n')
    tn.write(b'exit\r\n')
    tn.write(b'exit\r\n')   
    print(tn.read_until(b"\r\noutside",2).decode('utf-8'))
   
    #Enable guestshell
    tn.write(b'\r\nguestshell enable\r\n')
    print("Sleep mode turned on for few seconds to enable guestshell\n")
    time.sleep(60) 
    #print("sleep over")
    if tn.read_until(b"The process for the command is not responding or is otherwise unavailable",2).decode('utf-8'):
        tn.write(b'guestshell enable\r\n')
        time.sleep(50)
    print(tn.read_until(b"Guestshell enabled successfully",2).decode('utf-8'))
    tn.write(b'sh app-hosting list\r\n')
    tn.write(b'exit\r\n')
    print(tn.read_until(b"exit",2).decode('utf-8'))

    tn.close()
    
def guestshell_enable(telnet_ip,telnet_port):
    print("\n------------- Enabling & Running Guestshell -------------\n")

    tn = telnetlib.Telnet(telnet_ip,telnet_port)

    print (tn)    
    tn.write(b'\r\n\r\n')
    tn.write(b'\r\nen\r\n')
    tn.write(b'\r\nguestshell enable\r\n')
    time.sleep(20)
    print(tn.read_until(b"Guestshell enabled successfully",2).decode('utf-8'))
    tn.write(b'sh app-hosting list\r\n')
    
    #Make sudo user cisco in guestshell bash to support ssh
    tn.write(b'\r\nguestshell run bash\r\n')
    time.sleep(10)
    tn.write(b'\r\nsudo -i\r\n')
    tn.write(b'\r\nwhoami\n')
    tn.write(b'\r\nadduser cisco123\n')
    tn.write(b'echo -e "Lm12345678\nLm12345678"| passwd cisco123\r\n')
    time.sleep(2)
    tn.write(b'\r\necho "cisco123 ALL=(ALL) NOPASSWD:ALL" | tee -a /etc/sudoers') 
    time.sleep(2)
    tn.write(b'\r\nexit\r\n')
    tn.write(b'\r\nexit\r\n')
    time.sleep(2)
    tn.write(b'\r\nexit\r\n')
    print(tn.read_until(b"\r\nsudoers",2).decode('utf-8'))
    tn.close()

def ConfigurationSetup(telnet_ip,telnet_port,IP,GUESTSHELL_PORT,GUESTSHELL_INTERFACE):
    print("\n============================[ Running ConfigurationSetup.py : Configuring and enabling Guestshell on device ]============================\n")

    configure_device(telnet_ip,telnet_port,IP,GUESTSHELL_PORT,GUESTSHELL_INTERFACE)
    time.sleep(10)
    guestshell_enable(telnet_ip,telnet_port)

    print("Completed second script - ConfigurationSetup.py\n")

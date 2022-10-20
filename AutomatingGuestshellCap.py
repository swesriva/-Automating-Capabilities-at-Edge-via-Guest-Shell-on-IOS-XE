import CompatabilityCheck
import ConfigurationSetup
import ApplicationInstall
import time

def main():

    # Taking input from file and assigning to variables
    inputs_list=[]
    inputs_file=input("Please enter inputs file complete path : \n")
    with open(inputs_file) as file:
        contents = file.readlines()
        for line in contents:
            var = line.strip()
            inputs_list.append(var)
    print("Inputs :")
    print(inputs_list[:-1])

    telnet_ip=inputs_list[0]
    telnet_port=int(inputs_list[1])
    IP=inputs_list[2]
    GUESTSHELL_PORT=inputs_list[3]
    GUESTSHELL_INTERFACE=inputs_list[4]
    
    if(CompatabilityCheck.CompatabilityCheck(telnet_ip,telnet_port)):
        time.sleep(10)
        ConfigurationSetup.ConfigurationSetup(telnet_ip,telnet_port,IP,GUESTSHELL_PORT,GUESTSHELL_INTERFACE)
        time.sleep(10)
        ApplicationInstall.ApplicationInstall(IP,GUESTSHELL_PORT)
        print("\n================================================================================================\n")
        print("================================================================================================\n")
        print("SUCCESSFULLY HOSTED APPLICATION ON IOS XE!!\n")
        print("================================================================================================\n")
        print("================================================================================================\n")


    else:
        print("Application cannot be installed further!")
    
main()

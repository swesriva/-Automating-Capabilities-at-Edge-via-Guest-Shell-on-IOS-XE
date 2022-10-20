import asyncio
import time
import telnetlib
import re
import base64
import paramiko 
import csv
import re

def CompatabilityCheck(telnet_ip,telnet_port):
    print("\n============================[ Running CompatabilityCheck.py : Checking if device is compatible ]============================\n")

    tn = telnetlib.Telnet(telnet_ip,telnet_port)

    print (tn)    
    tn.write(b'\r\n\r\n')
    tn.write(b'\r\nen\r\n')
    tn.write(b'\r\nterminal length 0\r\n')
    tn.write(b'\r\nsh version\r\n')
    tn.write(b'\r\nsh inventory\r\n')
    tn.write(b'\r\nsh platform\r\n')
    tn.write(b'\r\nsh run | sec app-hosting\r\n')
    tn.write(b'\r\nsh run | in iox\r\n')
    tn.write(b'\r\nsh clo\r\n')
    contents= tn.read_until(b"\r\nphysical memory",10).decode('utf-8')
    # print(contents)
    tn.write(b'\r\nex\r\n')
    tn.close()
    ISR4 = re.search('cisco ISR4\d\d\d', contents) #checking for ISR4 series.
    ASR1 = re.search('cisco ASR1\d\d\d', contents) #checking for ASR1 series.
    CAT93 = re.search('cisco C93\d\d', contents) #checking for CAT9 series
    CAT94 = re.search('cisco C94\d\d', contents)
    CAT95 = re.search('cisco C95\d\d', contents)
    strmsg=""
    finalFlag= False
    def dram_function(): #for calculating DRAM in gb
        dram1 = re.findall('\d+K bytes of physical memory', contents)
        strmem="".join(dram1)
        mem = re.split(' ', strmem)
        sum=0
        for e in range(1):
            n= re.sub("\D", "", mem[e])
            n_int=int(n)
            sum=sum+n_int
        size=sum/1000000
        return(size)

    def storage_function(str1): #for checking if required storage modules are present
        pid1= re.findall('PID: [A-Za-z0-9/\-= ]+', contents)
        
        l= len(pid1)
        final=False
        for e in range(l):
            if (str1 in pid1[e]):
            
                final=pid_state(str1)
                if final:
                    break
            # final=True
        return(final)

    def pid_state(str1): #for checking PID state

        # state=re.match('(.+)'+str1+'([A-Za-z0-9/\-= ]+[a-z]+)',contents)
        state= re.findall("%s[A-Za-z0-9/\-= ]+" % str1, contents)
        l=len(state)
        
        for e in range(l):
            if ('ok' in state[e]):
                return True
    
    def app_hosting(): #for checking App hosting 

        strapp= re.search("hosting[A-Za-z0-9/\-=#\n\r |]+(?=guest|iox)", contents)
        striox= re.search("iox[A-Za-z0-9/\-=#\n\r |]+(?=clo)", contents)
        print(strapp)
        print(striox)
        strapp1=""+strapp.group()
        striox1=""+striox.group()
        dict1 = re.split('\n', strapp1)
        dict2= re.split('\n', striox1)
        l1=len(dict1)
        l2=len(dict2)
        # print(l1)
        # print(l2)
        if(l1<=3 and l2<=3):
            return True
    

    if ASR1:
        size_ram=dram_function()
        
        if(size_ram<8) :
            strmsg="ASR SIZE NOT CAPABLE"
        else:
        
            st_check1=storage_function("NIM-SSD")
            st_check2=storage_function("NIM-SSD=")
            st_check3=storage_function("M-ASR1K-HDD-80GB")

            if(st_check1 or st_check2 or st_check3):
                if(app_hosting()):
                    strmsg="ASR Fully CAPABLE"
                    finalFlag= True
                else:
                    strmsg="An app is already being hosted"
            else:
                strmsg="ASR NOT CAPABLE- STORAGE MODULES MISSING"

    elif ISR4:
        
        size_ram=dram_function()
        
        if(size_ram<8) :
            strmsg="ISR SIZE NOT CAPABLE"
        else:
        
            st_check1=storage_function("NIM-SSD")
            st_check2=storage_function("NIM-HDD")
            st_check3=storage_function("SSD-MSATA-200G")
            

            if(st_check1 or st_check2 or st_check3 ):
                if(app_hosting()):
                    strmsg="ISR Fully CAPABLE"
                    finalFlag= True
                else:
                    strmsg="An app is already being hosted"
                
            else:
                strmsg="ISR NOt CAPABLE- STORAGE MODULES MISSING"

    elif CAT93:
        size_ram=dram_function()
        if(size_ram<8) :
            strmsg="CAT SIZE NOT CAPABLE"
        else:
        
            st_check1=storage_function("SSD-120G")
            # st_check2=storage_function("USB3.0")
            if(st_check1):
                
                if ('dna-essentials' in contents):
                    if(app_hosting()):
                        strmsg="CAT Fully CAPABLE"
                        finalFlag= True
                    else:
                        strmsg="An app is already being hosted"
                
                else:
                    strmsg="CAT NOT CAPABLE- DNA LICENCE MISING"
            else:
                strmsg="CAT NOT CAPABLE- STORAGE MODULES MISSING"

    elif CAT94:
        size_ram=dram_function()
        if(size_ram<8) :
            strmsg="CAT SIZE NOT CAPABLE"
        else:
        
            st_check1=storage_function("C9400-SSD-")
            # st_check2=storage_function("USB3.0")
            if(st_check1):
                
                if ('dna-essentials' in contents):
                    if(app_hosting()):
                        strmsg="CAT Fully CAPABLE"
                        finalFlag= True
                    else:
                        strmsg="An app is already being hosted"
                
                else:
                    strmsg="CAT NOT CAPABLE- DNA LICENCE MISING"
            else:
                strmsg="CAT NOT CAPABLE- STORAGE MODULES MISSING"


    elif CAT95:
        size_ram=dram_function()
        if(size_ram<8) :
            strmsg="CAT SIZE NOT CAPABLE"
        else:
        
            st_check1=storage_function("SSD-120G")
            st_check2=storage_function("C9K-F3-SSD-")
            st_check3=storage_function("C9K-F1-SSD-")
            
            if(st_check1 or st_check2 or st_check3):
                
                if ('dna-essentials' in contents):
                    if(app_hosting()):
                        strmsg="CAT Fully CAPABLE"
                        finalFlag= True
                    else:
                        strmsg="An app is already being hosted"
                
                else:
                    strmsg="CAT NOT CAPABLE- DNA LICENCE MISING"
            else:
                strmsg="CAT NOT CAPABLE- STORAGE MODULES MISSING"

        
    else:
        strmsg="DEVICE CLASS NOT FOUND"

    
    print (strmsg)
    print("Completed first script - CompatabilityCheck.py\n")
    return (finalFlag)

    

# Automating Capabilities at Edge via Guest Shell on IOS-XE

Guestshell is a virtualized Linux-based environment, designed to run custom Linux applications, including Python for automated control and management of Cisco devices. It also includes the automated provisioning (Day zero) of systems. This container shell provides a secure environment, decoupled from the host device, in which users can install scripts or software packages and run them.
 Using Guest Shell, customers can install, update, and operate third-party Linux applications. It is bundled with the system image and can be installed using the guestshell enable IOS command.

### The Guest Shell environment is intended for tools, Linux utilities, and manageability rather than networking.

Guest Shell shares the kernel with the host (Cisco switches and routers) system. Users can access the Linux shell of Guest Shell and update scripts and software packages in the container rootfs. However, users within the Guest Shell cannot modify the host file system and processes.

Guest Shell container is managed using IOx. IOx is Cisco's Application Hosting Infrastructure for Cisco IOS XE devices. IOx enables hosting of applications and services developed by Cisco, partners, and third-party developers in network edge devices, seamlessly across diverse and disparate hardware platforms.

### Hardware Requirements for the Guest Shell
This section provides information about the hardware requirements for supported platforms.
```
|================|=====|======================|=======================|================|=================================|
|   Devices      | RAM | Storage-modules PIDs | Storage-modules state | DNA License    |  App-Hosting status/ IOX status |
|================|=====|======================|=======================|================|=================================|
| ISR4k series   |     |     NIM-SSD          |                       |                |                                 |
|                |     |     NIM- HDD         |                       |                |                                 |
|                |     |   SSD-MSATA-200G     |                       |       NA       |                                 |
|----------------|     |----------------------|                       |                |                                 |
| ASR1k series   |     |     NIM-SSD          |                       |                |                                 |
|                |  >8 |  M-ASR1K-HDD-80GB    |        'ok'           |                | No prior apps should be running |
|----------------|     |----------------------|                       |----------------|                                 |
| CAT9300 series |     |    SSD-120G          |                       |                |                                 |
|----------------|     |----------------------|                       |                |                                 |
| CAT9400 series |     |    C9400-SSD         |                       |    Present     |                                 |
|----------------|     |----------------------|                       |                |                                 |
| CAT9500 series |     |    SSD-120G          |                       |                |                                 |
|                |     |   C9K-F3-SSD-C9K     |                       |                |                                 |
|                |     |    F1-SSD            |                       |                |                                 |
|================|=====|======================|=======================|================|=================================|

```

### Managing IOx

IOx is a Cisco-developed end-to-end application framework that provides application hosting capabilities for different application types on Cisco network platforms. The Cisco Guest Shell, a special container deployment, is one such application, that is useful in system deployment/use.

IOx facilitates the life-cycle management of app and data exchange by providing a set of services that helps developers to package pre-built apps, and host them on a target device. IOx life-cycle management includes distribution, deployment, hosting, starting, stopping (management), and monitoring of apps and data. IOx services also include app distribution and management tools that help users discover and deploy apps to the IOx framework.
```
***Configures IOx services***
Device(config)#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
Device(config)#iox
Device(config)#end

***Displays the status of the IOx service***
Device# show iox-service

***Displays the list of app-hosting services enabled on the device***
Device# show app-hosting list
```
### Managing the Guest Shell

VirtualPortGroups are supported only on routing platforms.

Before you begin
IOx must be configured and running for Guest Shell access to work. If IOx is not configured, a message to configure IOx is displayed. Removing IOx removes access to the Guest Shell, but the rootfs remains unaffected.
An application or management interface must also be configured to enable and operate Guest Shell. See "Configuring the AppGigabitEthernet Interface for Guest Shell" and "Enabling Guest Shell on the Management Interface" sections for more information on enabling an interface for Guest Shell.

```
***Enables the Guest Shell service.***
Device> enable
Enables privileged EXEC mode.
Enter your password if prompted.

Device# guestshell enable

Note :	
The guestshell enable command uses the management virtual routing and forwarding (VRF) instance for networking.

When using VirtualPortGroups (VPGs) for front panel networking, the VPG must be configured first.

The guest IP address and the gateway IP address must be in the same subnet.
```
### VirtualPortGroup Configuration
Note	
VirtualPortGroups are supported only on Cisco routing platforms.

When using the VirtualPortGroup interface for Guest Shell networking, the VirtualPortGroup interface must have a static IP address configured. The front port interface must be connected to the Internet and Network Address Translation (NAT) must be configured between the VirtualPortGroup and the front panel port.

```
Device(config)#int virtualportgroup0
    Device(config-int)#ip address 192.168.35.1 255.255.255.0
    Device(config-int)#ip nat inside
    Device(config-int)#no shutdown
    Device(config-int)#exit
```

### Enabling and Running the Guest Shell
The guestshell enable command installs Guest Shell. This command is also used to reactivate Guest Shell, if it is disabled.

When Guest Shell is enabled and the system is reloaded, Guest Shell remains enabled.

IOx must be configured before the guestshell enable command is used.

The guestshell run bash command opens the Guest Shell bash prompt. Guest Shell must already be enabled for this command to work.

```
***Executes or runs a Linux program in the Guest Shell.***
Device# guestshell run python
or
Device# guestshell run python3


Note 	:
In Cisco IOS XE Amsterdam 17.3.1 and later releases, only Python version 3 is supported.

***Starts a Bash shell to access the Guest Shell.***
Device# guestshell run bash
```

### Disabling and Destroying the Guest Shell
The guestshell disable command shuts down and disables Guest Shell. When Guest Shell is disabled and the system is reloaded, Guest Shell remains disabled.

The guestshell destroy command removes the rootfs from the flash filesystem. All files, data, installed Linux applications and custom Python tools and utilities are deleted, and are not recoverable.
```
***Disables the Guest Shell service.***
Device# guestshell disable

***Deactivates and uninstalls the Guest Shell service.***
Device# guestshell destroy
```
### [Learning lab URL](https://developer.cisco.com/learning/tracks/EN-Networking-v0/EN-Networking-Fundamentals-v0/intro-guestshell/enabling-guest-shell/)


### Steps to follow :-
```
Step 1 : Populate the inputs.txt file (order of inputs : telnet_ip,telnet_port,IP,GUESTSHELL_PORT,GUESTSHELL_INTERFACE)

Step 2 : Run "AutomatingGuestshellCap.py" and provide inputs.txt file's complete path as input to get the process started.

AutomatingGuestshellCap.py calls the other scripts and executes the project as a whole.The following process occurs:

   2.1 : "CapatabilityCheck.py" will be executed - which :
         - Checks if the device is capable or not for hosting the application, as per the criterias explained above.
   If 2.1 is False, the App cannot be hosted. 
   If 2.1 is True -
   2.2 : " ConfigurationSetup.py" will be executed -  which :
          - Configures IOx/ App Hosting on the device.
          - Enables the Guest Shell.
   2.3 : "ApplicationInstall.py" which be executed - which :
          - Installs the required application on Guestshell ( e.g. iperf )
          
Step 3 : Check the output.
```

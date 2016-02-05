#Setup client

The client is a python script (client.py) intended to run on a small device, receiving its testing schedule from the governor server. 

##client.cfg

Client.cfg contains the basic configuration information that client.py will use to request and receive a test schedule from the governor server. It also contains three IDs that define the device privately to the server.

```
[Addresses]

partnerID: 1
groupID: 3
deviceID: 7
server_address: 52.91.156.102
client_path: /home/odroid/ACPS/
```

*partnerID* is an indicator intended to distinguish different users of the governor/client system.
*groupID* distinguishes different groups of devices, for example at different locations.
*deviceID* is a unique number for each device deployed by a given partner.
*server_address* is the world routable IP address where your governor server is running.
*client_path* is the absolute path to the client code 

##Setting Variables in the Configuration File 

The client script depends on absolute paths. This path needs to be defined in the configuration file. If the absolute path to the client script (client.py) is /home/odroid/ACPS/client/client.py, then the client_path variable should be set to /home/odroid/ACPS. 

Make sure the group ID and device ID in the client configuration file (client.cfg) are what you intended for this device. The governor authenticates clients by checking that their client ID (the concatenation of its partner ID, group ID, and device ID) is in its database before assigning it a schedule. 

##Running NDT

To be able to run NDT, you need to make sure your version of libjansson4 is updated.  

```
$ sudo apt-get update
$ sudo apt-get install libjansson4 
```

##Timezone

Governor server schedules in relation to the local time. To be sure that the scheduled tests are being run when you expect. Explicitly set the timezone on your client devices to your local time zone. 

```
$ sudo dpkg-reconfigure tzdata  
```

##Setting static IPs

Put this stanza in /etc/network/interfaces - replacing the IPs with your network info:

```
auto eth0
iface eth0 inet static
address 10.10.1.171
netmask 255.255.0.0
gateway 10.10.254.254
broadcast 10.10.255.255
dns-nameservers 10.5.0.10 10.5.0.20
```

##Adding script as a startup service
1. Make sure the script is executable.
 	```
	$ sudo chmod +x 'acps-service' 
	```
2. Move 'acps-service' to /etc/init.d/. While in the client directory:
	```
	$ sudo move 'acps-service' to /etc/init.d/
	```
3. Enable it as a startup service.
	```
	$ sudo /etc/init.d/acps-service enable
	$ sudo update-rc.d acps-service defaults
	```

##Connect to the OTI governor server
```
ssh -i "oti-measuring-broadband.pem" ubuntu@52.91.156.102
```








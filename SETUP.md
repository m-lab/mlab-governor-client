## Setup client

The client is a python script (client.py) intended to run on a small device, receiving its schedule from the governor server.

### client.cfg

Client.cfg contains the basic configuration information that client.py will use to request and receive a test schedule from the governor server. It also contains three IDs that define the device privately to the server. 
```
[Addresses]

partnerID: 1
groupID: 3
deviceID: 7
server_address: 52.91.156.102
```

*partnerID* is an indicator intended to distinguish different users of the governor/client system. 

*groupID* distinguishes different groups of devices, for example at different locations.

*deviceID* is a unique number for each device deployed by a given partner.

*server_address* is the world routable IP address where your governor server is running.

### Setting static IPs

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

### Adding script as a startup service 

1) move 'acps-service' to /etc/init.d/
2) enable it as a startup service:
$ sudo update-rc.d acps-service defaults

### Connect to the OTI governor server

ssh -i "oti-measuring-broadband.pem" ubuntu@52.91.156.102


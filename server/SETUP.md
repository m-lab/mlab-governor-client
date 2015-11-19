#Setup governor
The governor is a python server (governor.py) intended to schedule tests run on small, remote devices.

##governor.cfg

Governor.cfg contains the basic configuration information that the governor server needs to assign schedules. 

```
[Timing]
runs_per_day: 96
database_name: ACPS 
```

*runs_per_day* is the mean of an exponential distribution that is used to schedule about *runs_per_day* tests per day.
*database_name* is the name for the database you specified when setting up mongodb

##Adding script as a startup service

The server requires two things to be run on startup. 
* Mongodb server in the background
* governor.py 

Instructions for how to run mongodb in the background can be found here: 
https://docs.mongodb.org/manual/tutorial/manage-mongodb-processes/

To make the governor.py script run on start up: 

1. Write a simple script calling the governor script and printing the output into a log file in the “server” folder. 
		
```
$ sudo vi governor_startup_script /etc/init.d/
```

Within the file: 

```python
#!/bin/sh -e
python absolute/path/to/governor.py > absolute/path/to/governor.log
```

2. Enable it as a startup service.

```
$ sudo update-rc.d acps-service defaults
```

##Setting up the database

By default the governor uses two collections: “devices” and “testIds”. Any device you want to be able to connect with the server should be put into the database.

Device Schema

```
{
   deviceID : ‘1’, 
   groupID : ‘1’, 
   partnerID : ‘1’
}
```

TestId Schema 

```
{
    deviceID : ‘1/1/1’, 
    testId: ‘91312284cca5bcb38a353ae8c8ec9d4d’
}
```

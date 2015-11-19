#About

This repository houses the server and client code of a distributed network performance testing framework. Clients receive a daily testing schedule from the central “governor” server, and run NDT tests accordingly. Test data becomes part of MLab’s open data set. 

More about MLab: 
http://www.measurementlab.net/
  
More about accessing MLab data: 
https://github.com/m-lab/mlab-wikis/blob/master/HowToAccessMLabData.md

##Original Use

This framework was originally developed to measure the network performance within Alexandria City Public Schools. This project focused on mapping quantitative data, created by odroid devices serving as clients and placed inside the classrooms, to qualitative descriptions of network conditions based on teacher reports. Analysis of this coupled data was then used to draw conclusions about how connectivity impacts effective use of technology in the classroom. 

##Intended Use

This testing framework is most effective in a situation that meets the following criteria: 
Users are interested measuring end-to-end network performance
There is sufficient bandwidth that the tests run will not affect the results
Users are interested in testing several different locations 

#Quickstart

##Requirements

####Server

*MongoDB 
*Static IP or hostname accessible to clients

####Clients

*Internet connection

##Process
To quickly begin creating performance data for your own network follow the steps below: 

1. Clone this repository. 
2. Copy “client” folder onto your devices acting as clients. Follow instructions in client/SETUP.md to properly configure the client.
3. Copy “governor” folder onto the server. Follow instructions in governor/SETUP.md to properly configure the governor server. 

##Accessing Data
Clients generate random 16 byte test ID’s associated with each test. These test ID’s are stored in the database on the server mapped to the client ID of the specific client that ran the test. These test ID’s can be used as special flags for querying MLab data. 





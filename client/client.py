#!/usr/bin/python

import sched, time, ConfigParser, subprocess, json, urllib2, socket, sys, random, shutil

mySchedule= []
governor = sched.scheduler(time.time, time.sleep)
config = ConfigParser.RawConfigParser()
configFile= "client.cfg" 



############################################ Helpers   #############################################################

def get_ndt_server():
   """Function to retrieve information about the closest ndt server 
   
   Returns: 
      (string) server url
   """
   mlabns=urllib2.urlopen('http://mlab-ns.appspot.com/ndt').read() #returns a JSON object referring to the closest mlab server
   server = json.loads(mlabns)['fqdn'].encode('ascii')
   return server

def run_ndt ():
   """Function that runs ndt on the client. Creates a log file 'client.log'
   and appends to the testID log file for today.
   """
   print "Running NDT test."
   
   ndt_server = get_ndt_server()
   ndt_testID= create_testID()

   print "Client "+str(clientID)+": Running ndt test at "+ time.strftime("%x,%H:%M:%S")+ " with test Id: "+ ndt_testID

   test_output = subprocess.Popen([clientPath+"web100clt", "-c", ndt_testID, "-n", ndt_server, "--disablesfw", "--disablemid"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   log_data(ndt_testID)  #saves the testID to the log file
   log_text = test_output.communicate()
   logfile = open( clientPath+"client.log", 'a')

   logfile.write(time.strftime("\n-------\n%x,%H:%M:%S\n" + ndt_server + "\n"))
   for line in log_text[0].split('\n'):
      print line
      logfile.write(line + "\n")
   logfile.close()

def schedule_one_task(start_time, function): 
   """Function that enters one test time into the scheduler. Checks to make 
   sure that the event is in the future

   Args: 
      start_time: (time_struct instance)
      function: function that will be executed at start_time

   """
   now= time.localtime()
   if start_time > now: 
      governor.enterabs(time.mktime(start_time), 1, function, ())

def scheduleTests(schedule): 
   """Function that enters all test times for one day into the scheduler
   
   Args: 
      schedule: (list) of time_struct instances to schedule ndt 
   """
   for task in schedule: 
      schedule_one_task(task, run_ndt)

def process_reply(string_schedule): 
   """Function to process the string reply from the server 
   containing the schedule. 

   Args: 
      string_schedule: (string) 

   Returns: 
      (list) of time_struct instances 
   """
   list_schedule=  string_schedule.split('/')
   now= time.localtime()
   
   schedule= []
   for start_time in list_schedule: 
      schedule.append(time.strptime(str(now.tm_year) + "," + str(now.tm_yday) + "," + str(start_time[0:2])+":"+str(start_time[2:4])+":"+str(start_time[4:6]), '%Y,%j,%H:%M:%S'))

   return schedule

def create_testID(): 
   """Function to create a random 16 byte string 

   Return: 
      (string) 16 bytes of entropy
   """
   proc = subprocess.Popen(["head -c 16 /dev/urandom |xxd -p"],stdout=subprocess.PIPE, shell=True)
   return proc.communicate()[0]

def log_data(testID): 
   """Function to append data to today's log of testIDs. Data
   will either be test ID's or confirmation of test ID's 
   being saved. 

   Args: 
      testID: (string) 
   """
   testlog = open( clientPath+"todays_testIDs.log", 'a')
   testlog.write(testID+"\n")
   testlog.close()

def start_new_testLog(): 
   """Function to clear yesterday's testID log, create a new blank log for today
   Only used after today and yesterday's logs have been sent to the governor server
   """

   shutil.copyfile(clientPath+"todays_testIDs.log", clientPath+"yesterdays_testIDs.log")
   today= open(clientPath+"todays_testIDs.log", 'w')
   today.write(time.strftime("%d/%m/%Y")+'\n')
   today.close()

def prepare_testIDs():
   """Function that collects and formats all the testId's used that day 
   and the day before to send to the server. Message will be in the 
   form: "clientID\nTESTIDS\nid1\nid2\nid3\nid4"
   """
   message= clientID+"\n"
   message+= "TESTIDS\n"  
   today= open(clientPath+"todays_testIDs.log", 'r')
   for line in today: 
      message+=line

   yesterday= today= open(clientPath+"yesterdays_testIDs.log", 'r')
   for line in yesterday:
      message+=line

   return message


##############################################   Socket code #############################################################

def talk_to_server(message): 
   """
   Function used to send and receive messages from the server. 
   
   Args: 
      message: (string)
   
   Only two types of messages should be sent. 1. A client ID
   to ask for a schedule or 2. a string of all test ID's to 
   be saved by the governor server. 

   Only three types of messages can be received. 1. a schedule
   2. ack indicating the test ID's were received 3. "Failed" 
   indicating client communication failed.
   """
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
   try: 
      s.connect((server_address, port))
   except socket.error: 
      print "Error connecting to the server. Closing connection..."
      sys.exit()
    
   print 'Socket connected to server'    
   
   try :
       s.sendall(message)
   except socket.error:
       print 'Send failed'
       sys.exit()

   reply = s.recv(4096)
   print "Completed communication."
   print "Server reply: "+str(reply)
   

   #if got a schedule
   if "/" in reply: 
      reply= process_reply(reply)
      print "Successfully received new schedule."

   #ack received after saving ids
   elif reply=="ack": 
      log_data("TestIDs successfully saved on server.")
      print "Test Id's successfully saved on server."

   #some failure
   elif reply=="Failed.": 
      log_data("Communication with server failed: "+message)
      print "ERROR: Could not communicate with server."

   
   s.close()
   return reply

def send_testIDs(): 
   """
   Function to be put into scheduler for just after midnight that tells the governor server
   of all the testIDs used today and yesterday
   Governor server DB deals with duplicates
   """
   new_message=prepare_testIDs()
   start_new_testLog()
   talk_to_server(new_message)


config.read(configFile) 
clientPath= config.get("Addresses", "client_path")
server_address=config.get("Addresses", "server_address")
deviceID= config.get("Addresses", "deviceID")
#clientID= "partnerID/groupID/deviceID"
clientID= config.get("Addresses", "partnerID")+"/"+config.get("Addresses", "groupID")+"/"+deviceID
port = 8888


######################################################################################################################

if __name__ == '__main__':
   
   print "Connecting to server address: "+str(server_address)
   print "clientID: "+str(clientID)

   #Constantly checks if scheduler is empty
   while 1: 
      if governor.empty(): 
         
         #ask for a new schedule
         message = str(clientID)
         new_sched= talk_to_server(message)
         
         #if received new schedule
         if type(new_sched)==list: 
            scheduleTests(new_sched)
            print "New tests scheduled."
            governor.run()

     
      #if almost midnight, send ids
      now= time.localtime()
      midnight= time.strptime(str(now.tm_mon)+"/"+str(now.tm_mday)+"/"+str(now.tm_year)+","+ "23,59,00",  '%m/%d/%Y,%H,%M,%S')
      if now>midnight: 
         send_testIDs()







 

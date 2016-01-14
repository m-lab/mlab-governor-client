import sched, time, random, ConfigParser, subprocess, json, urllib2, socket, thread, sys
from pymongo import MongoClient
config = ConfigParser.RawConfigParser()


############################### Variables that can be tweaked  #################################################################

configFile= "governor.cfg" 
test_duration=35 #seconds


######################### Defaults: will get set in refresh/init ##############################################################

devices= {} #dictionary of client objects, updated at midnight

config.read(configFile)
runs_per_day = int(config.get("Timing", "runs_per_day"))

re_scheduler = sched.scheduler(time.time, time.sleep)

####################################  Database Code #####################################################################

client = MongoClient('localhost', 27017)
db = client[config.get("Timing", "database_name")]
device_collection = db.devices
testID_collection= db.testIds

####################################  Client object #####################################################################

class Device: 
   """
   Class that will store all information relevant to an individual, real-life device
   """
   def __init__(self, deviceID, groupID, partnerID): 
     
      self.deviceID= deviceID  
      self.groupID= groupID
      self.partnerID= partnerID
      self.scheduled_runs= []  #runs for the next period

   def setSchedule(self, scheduled): 
      """
      Args: 
         scheduled: (list of string) representing testing times.
      """
      self.scheduled_runs= scheduled 
   
   def getSchedule(self): 
      """
      Returns: 
         (list) of time_struct instances
      """
      return self.scheduled_runs

####################################################  Helpers  #############################################################

def seconds_to_time(seconds_float): 
   """Function to convert a time in seconds into a time. 
   Args: 
      seconds_float: (float) time in seconds_to_time

   Returns: 
      (list of strings) [Hour, Minute, Second]
   """
   seconds= int(seconds_float)
   new_hour= str((seconds/3600))
   new_minute= str((seconds%3600)/60)
   new_second= str(((seconds%3600)%60))  
   return [new_hour, new_minute, new_second]  

def schedule_runs(): 
   """Function to schedule the runs for one day.
   Returns: 
      (list of string) runtimes in the form: [HMS, HMS, HMS, HMS]
   """
   global runs_per_day
   schedule=[]
   last_scheduled= (0,0,0)
   second_tally= random.expovariate(float(runs_per_day)/86400) 
  
   while second_tally < 86400: #86400 seconds in a day
      
      new_time = seconds_to_time(second_tally)
      
      #To maintain proper place value for the digits
      for i in range(0, 3): 
         elm= new_time[i]
         if len(elm) < 2: 
            new_time[i]= "0" + elm

      start_time= new_time[0]+new_time[1]+ new_time[2]
      schedule.append(start_time)
      last_scheduled= (int(new_time[0]), int(new_time[1]), int(new_time[2]))

      second_tally+= random.expovariate(float(runs_per_day)/86400)

   return schedule[:-1]

def schedule_refresh():
   """Function that adds refresh() to the scheduler at 23:59:00.
   """ 
   this_midnight= time.localtime()
   midnight= time.strptime(str(this_midnight.tm_year) + "," + str(this_midnight.tm_yday) + ",235900", "%Y,%j,%H%M%S")
   re_scheduler.enterabs(time.mktime(midnight), 1, refresh,())

def refresh(): 
   """Function that refreshes the configuration variables and
   dictionary of known devices/clients. Allows for incorporation of new devices.
   """
   global runs_per_day

   config.read(configFile)
   
   #1. Set variables from config file
   runs_per_day = int(config.get("Timing", "runs_per_day"))

   #2. Populate the client dictionary and schedule their runs for today
   deviceIDs= device_collection.find({})
   for one_device in deviceIDs: 

      partner= str(one_device["partnerID"])
      group= str(one_device["groupID"])
      device= str(one_device["deviceID"])

      newest_device= Device(device, group, partner)
      client_key= partner+"/"+group+"/"+device
      devices[client_key]= newest_device

      newest_device.setSchedule(schedule_runs())

   schedule_refresh()

def create_JSON_message(message_type, clientID, body=None): 
   """Function to create a JSON object to send to the server. 

   Args: 
      type: (string) 'testId' | 'schedule' | 'failed' | 'ack'
      clientID: (string) clientID
      body: (optional) if the type is testId, then body is a list of 
      string testId's


   Returns: 
      (JSON) JSON encoded message 

   {
      deviceID: deviceID, 
      
      : groupdID, 
      partnerID: partnerID, 
      type: testId | ack | fail | schedule
      body: [testId_string, testId_string]
   }

   """
   message= {"clientID" : clientID, "type" : message_type, "body" : body}
   return json.dumps(message)


###############################  Serve  ##############################################################

def save_testIDs(message): 
   """Function to save a client reported testIDS 

   Args: 
      ids: (list) of testId's
   Returns: 
      (Boolean) False if there's a problem saving id's
      (string) "ack", if id's are saved successfully
   """
   idArray= message["body"]
   
   for testid in idArray: 
      db.testID_collection.insert({ "deviceID": message["clientID"], "testID": testid})
   return create_JSON_message("ack", message["clientID"])

def schedule_request(client, clientID): 
   """Function to handle a client requesting a schedule.

   Args: 
      client: (Device instance) of the client requesting 
              a schedule.
   Returns: 
      (string) of new schedule in the form HMS/HMS/HMS
   """
   schedule= schedule_runs()  
   client.setSchedule(schedule)
   return create_JSON_message('schedule', clientID, schedule)

def handle_request(message):
   """General function to handle all requests.

   Args: 
      data: (dictionary) data received from client
   """  
   clientID= message["clientID"]

   try: 
      device= devices[clientID]   #client "authentication"
   except KeyError: 
      print "ClientID was not recognized."
      print "Closing connection..."
      return False
   
   #client is asking for a schedule
   if message["type"]=="schedule": 
      return schedule_request(device, message["clientID"])
   #client is reporting testIds
   elif message["type"]=="testId": 
      return save_testIDs(data)
   else: 
      print "Request was not recognized."
      print "Closing connection..."
      return False


def clientthread(connection, address):  

   data = connection.recv(1024) 
   data = json.loads(data)

   print "Received message from client: " + str(data)
   

   now= time.localtime()
   reply = handle_request(data)

   print "Time: " + str(now.tm_hour)+":" + str(now.tm_min)+ ":"+ str(now.tm_sec)
   
   if reply:
      connection.sendall(reply)
      if "schedule" in reply: 
         print "Sent the following schedule: "+ reply +" to client."
      else: 
         print "Responding with: "+ reply

   else: 
      connection.sendall(create_JSON_message("fail", "Unknown"))
      print "There was a problem processing client request."
      print "Closing connection..."

   connection.close()
   print "Connection closed."


###############################  Socket Code  ##############################################################

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if __name__ == '__main__':

   refresh()

   try:
       serversocket.bind((HOST, PORT))
   except socket.error , msg:
       print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
       sys.exit()
        
   print 'Socket bind complete'
    
   serversocket.listen(10)
   print 'Socket now listening'

   while 1:

       connection, addr = serversocket.accept()
       print 'Connected with ' + addr[0] + ':' + str(addr[1])
       thread.start_new_thread(clientthread ,(connection, addr))
    
   serversocket.close()











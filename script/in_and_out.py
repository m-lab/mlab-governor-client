import queries
import subprocess

def load_file(filepath):
	test_ids= []
	f=open(filepath, 'r')
	next_line= f.readline()
	
	while next_line:  
		if len(next_line) > 1: 
			test_ids.append(next_line[:-1])
		next_line= f.readline()

	return test_ids

class TestIdFile(object): 

	def __init__(self, device_id, input_file_path):
		self.device_id= device_id
		self.test_ids= load_file(input_file_path)


def get_query_all_ids(query_type, testIdFileObject): 
	query= queries.format_command(query_type, testIdFileObject.test_ids[0])
	add_id_string= " OR connection_spec.client_application = '{next_test_id}'"
	additional_ids= ""
	
	for i in range(1, len(testIdFileObject.test_ids)):
		test_id= testIdFileObject.test_ids[i]
		additional_ids+= add_id_string.format(next_test_id=test_id)

	return query+additional_ids+" )\""

def run_all_queries_one_device(testIdFileObject): 
	for query in ["client_lim_ratio_query", "net_lim_ratio_query", "packet_retrans_query", "rtt_query", "download_query", "upload_query"]: 
		command= get_query_all_ids(query, testIdFileObject)
		out_file= testIdFileObject.device_id+"_"+query+".csv" 
		subprocess.call(command+" > "+out_file, shell=True)

def run_all_queries_all_devices(all_File_objects): 
	for device in all_File_objects: 
		run_all_queries_one_device(device)
	
def make_all_device_objects(): 
	"""Chris: these were the only files that were in the tar? Also you'll have to change these paths """
	all_devices=[]
	#all_devices.append(TestIdFile("8", "/Users/LavalleF/Documents/mlab-governor-client/test_ids/desk_odroid_test.log"))
	all_devices.append(TestIdFile("1", "/Users/LavalleF/Documents/mlab-governor-client/test_ids/left_side_ids.log"))
	# all_devices.append(TestIdFile("1", "/Users/LavalleF/Documents/mlab-governor-client/test_ids/data_Nov-Dec_2015/tcwilliams/client-1_TC_testIDs.log"))
	# all_devices.append(TestIdFile("2", "/Users/LavalleF/Documents/mlab-governor-client/test_ids/data_Nov-Dec_2015/tcwilliams/client-2_TC_testIDs.log"))
	# all_devices.append(TestIdFile("3", "/Users/LavalleF/Documents/mlab-governor-client/test_ids/data_Nov-Dec_2015/tcwilliams/client-3_TC_testIDs.log"))
	# #all_devices.append(TestIdFile("4",  ))
	# all_devices.append(TestIdFile("5", "/Users/LavalleF/Documents/mlab-governor-client/test_ids/data_Nov-Dec_2015/hammond/client-5_hammond_testIDs.log"))
	# all_devices.append(TestIdFile("6", "/Users/LavalleF/Documents/mlab-governor-client/test_ids/data_Nov-Dec_2015/hammond/client-6_hammond_testIDs.log"))
	# #all_devices.append(TestIdFile("7",  ))
	# #all_devices.append(TestIdFile("8",  ))
	# #all_devices.append(TestIdFile("9",  ))
	# #all_devices.append(TestIdFile("10",  ))
	# #all_devices.append(TestIdFile("11",  ))
	# #all_devices.append(TestIdFile("12",  ))
	return all_devices 




all_devices= make_all_device_objects()
run_all_queries_all_devices(all_devices)




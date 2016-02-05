import ../client/client

def load_file(filepath):
	f=open(filepath, 'r')
	next_line= f.readline()
	
	while next_line:  
		if len(next_line) > 1: 
			#print next_line[0:16]
			print next_line[16:]
		next_line= f.readline()

	



#load_file("/Users/LavalleF/Documents/mlab-governor-client/test_ids/wednesday_testid_check.csv")


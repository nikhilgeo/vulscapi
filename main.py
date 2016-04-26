from defusedxml.ElementTree import parse
import nex 

#read access request from XML
def readAccessReq():
	tree = parse('access_request.xml')
	root = tree.getroot()
	for child in root.findall('user'):
		name = child.find('name').text
		print(name)
		email = child.find('email').text
		print(email)

#read the scanner details
def readScanner(scannerName):
	tree = parse('scanner_details.xml')
	root = tree.getroot()
	scanner = root.find(scannerName)
	#print(scanner)
	print(scanner.find('host').text)
	print(scanner.find('username').text)
	usr_passwd = input("Please enter your password for Nexpose: ")
	user_cred = {'uname':scanner.find('username').text,'passwd':usr_passwd,'host':scanner.find('host').text}
	return user_cred


scanner_info = readScanner('nexpose')
nexposeObj = nex.Nexpose(scanner_info)




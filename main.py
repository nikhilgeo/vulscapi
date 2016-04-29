from defusedxml.ElementTree import parse
import nex 
from util import PrintUtil

#read access request from XML
def readAccessReq():
	ip=""
	tree = parse('access_request.xml')
	root = tree.getroot()
	for child in root.findall('user'):
		name = child.find('name').text
		#print(name)
		email = child.find('email').text
		#print(email)
	asst_det = root.find('asset_details')
	for ipchild in asst_det.findall('ip'):
		ip = ip+","+ipchild.text
		#print(ip)
	access_req ={'name':name,'email':email,'ip':ip}
	print(access_req)

#read the scanner details
def readScanner(scannerName):
	tree = parse('scanner_details.xml')
	root = tree.getroot()
	scanner = root.find(scannerName)
	#print(scanner)
	print("Nexpose Host@:"+scanner.find('host').text)
	#print(scanner.find('username').text)
	usr_passwd = input("Please enter your password for Nexpose: ")
	user_cred = {'uname':scanner.find('username').text,'passwd':usr_passwd,'host':scanner.find('host').text}
	return user_cred


access_details = readAccessReq()
scanner_info = readScanner('nexpose')
nexposeObj = nex.Nexpose(scanner_info)




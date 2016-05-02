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
	site_det = root.find('site')
	site_name = site_det.get('name')
	site_desc = site_det.get('desc')
	for ipchild in asst_det.findall('ip'):
		ip = ip+","+ipchild.text
		#print(ip)
	ip = ip.strip(',')
	access_req ={'name':name,'email':email,'ip':ip,'site_name':site_name,'site_desc':site_desc}
	print(access_req)
	return access_req
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


#Reading the Access Request
access_details = readAccessReq()
#******NEXPOSE******
#Read Nexpose Scanner Info, from config file
scanner_info = readScanner('nexpose')
#Initilize the Nexpose connection
nexposeObj = nex.Nexpose(scanner_info)
nexposeObj.handleAccessReq(access_details)
#SaveSite and Add User
#TBD




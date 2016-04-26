from defusedxml.ElementTree import parse

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


readScanner('nexpose')	

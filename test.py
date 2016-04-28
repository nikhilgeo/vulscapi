from defusedxml.ElementTree import parse


tree = parse('textXML.xml')
root = tree.getroot()
loginResponse = root.get('success')
if(loginResponse==1):
	self.session_id = root.get('session-id')
else:
	fa=root.find('Failure')
	ex=fa.find('Exception')
	msg=ex.find('message').text
	print('\033[93m'+"Login Failure: "+msg+'\033[0m')



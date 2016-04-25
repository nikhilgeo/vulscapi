from defusedxml.ElementTree import parse

tree = parse('access_request.xml')
root = tree.getroot()
for child in root.findall('user'):
	name = child.find('name').text
	print(name)
	email = child.find('email').text
	print(email)
	

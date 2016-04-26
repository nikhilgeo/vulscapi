from xml.etree.ElementTree import Element, SubElement, ElementTree
import requests
from io import BytesIO
#Have not used the diffusedXML library as the XML construction functions is only done here and they are not supported.
class Nexpose:
	'''All the Nexpose API are handled here'''
	#self. - for all members that are common to the object without self scope is limited to the block
	#self must the default mandatory parameter in all member functions	
	#Caution !!: __init__ have two underscores on each side
	
	def __init__(self,scanner_info):
		# API v1.1 Login and get the session here
		xmlReq = Element('LoginRequest',attrib={'user-id':scanner_info['uname'],'password':scanner_info['passwd']})
		self.nexpose_host = scanner_info['host']
		xmlTree = ElementTree(xmlReq)
		f=BytesIO()
		xmlTree.write(f,encoding='utf-8',xml_declaration=True)# required so that xml declarations will come up in generated XML
		self.loginReqXML=f.getvalue().decode("utf-8")# converts bytes to string
		print(self.loginReqXML)
		self.makeRequest()
	def makeRequest(self):
		headers = {'Content-Type': 'text/xml'}	
		response=requests.post(self.nexpose_host+"/api/1.1/xml",data=self.loginReqXML,headers=headers,verify=False)
		print(response.text)
		
	def siteManagement():
		print("TestModule")
	
	# API v1.1 SiteConfig- Provide the configuration of the site, including its associated assets.
	# API v1.1 SiteSave- Save changes to a new or existing site.
	#def userManagement():
	# API v1.1 UserSave- Create a new user account, or update the settings for an existing account. 
	#def _del_(self):
	# API v1.1 Logout and close the session

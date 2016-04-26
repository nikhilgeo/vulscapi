from xml.etree.ElementTree import Element, SubElement, dump, ElementTree
import requests
#Have not used the diffusedXML library as the XML construction functions is only done here and they are not supported.
class Nexpose:
	'''All the Nexpose API are handled here'''
	def __init__(self,scanner_info):
		# API v1.1 Login and get the session here
		root= Element('LoginRequest',attrib={'user-id':scanner_info['uname'],'password':scanner_info['passwd']})
		self.nexpose_host = scanner_info['host']
		dump(root)
		makeRequest(root)
		#LoginReqXML = ElementTree(root)
		#LoginReqXML.write
	def siteManagement():
		print("TestModule")
	def makeRequest():
		headers = {'Content-Type': 'text/xml'}	
	# API v1.1 SiteConfig- Provide the configuration of the site, including its associated assets.
	# API v1.1 SiteSave- Save changes to a new or existing site.
	#def userManagement():
	# API v1.1 UserSave- Create a new user account, or update the settings for an existing account. 
	#def _del_(self):
	# API v1.1 Logout and close the session

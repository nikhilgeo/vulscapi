from xml.etree.ElementTree import Element, SubElement, ElementTree
from defusedxml.ElementTree import parse, fromstring
import requests
from io import BytesIO
from util import PrintUtil


# Have not used the diffusedXML library as the XML construction functions is only done here and they are not supported.
class Nexpose:
    '''All the Nexpose API are handled here'''

    # self. - for all members that are common to the object without self scope is limited to the block
    # self must the default mandatory parameter in all member functions
    # Caution !!: __init__ have two underscores on each side

    def __init__(self, scanner_info):
        try:
            # API v1.1 Login and get the session here
            xmlReq = Element('LoginRequest',
                             attrib={'user-id': scanner_info['uname'], 'password': scanner_info['passwd']})
            self.nexpose_host = scanner_info['host']
            xmlTree = ElementTree(xmlReq)
            f = BytesIO()
            xmlTree.write(f, encoding='utf-8',
                          xml_declaration=True)  # required so that xml declarations will come up in generated XML
            loginReqXML = f.getvalue().decode("utf-8")  # converts bytes to string
            # print(self.loginReqXML)
            responseXML = self.makeRequest(loginReqXML)
            tree = ElementTree(fromstring(responseXML))
            root = tree.getroot()
            loginResponse = root.get('success')
            if (loginResponse == "1"):
                self.session_id = root.get('session-id')
                PrintUtil.printSuccess("Logged in to Nexpose Scanner")
            else:
                fa = root.find('Failure')
                ex = fa.find('Exception')
                msg = ex.find('message').text
                PrintUtil.printError("Login Failure: " + msg)
        except Exception as e:
            PrintUtil.printException(str(e))

    def makeRequest(self, requestXML):
        headers = {'Content-Type': 'text/xml'}
        response = requests.post(self.nexpose_host + "/api/1.1/xml", data=requestXML, headers=headers, verify=False)
        print(response.text)
        return (response.content)

    def addSite(self, access_req):
        # print("TestModule:SiteManagement")
        siteSaveRequest = Element('SiteSaveRequest', attrib={'session-id': self.session_id})
        # print(access_req['site_name'])
        # Site element have 'S' in caps !!--lost a day on this !!
        site_elem = SubElement(siteSaveRequest, 'Site', attrib={'name': access_req['site_name'], 'id': '-1'})
        host_elem = SubElement(site_elem, 'Hosts')
        for ip in access_req['ip'].split(','):
            range_elem = SubElement(host_elem, 'range', attrib={'from': ip, 'to': ''})
        scanConfig_elem = SubElement(site_elem, 'ScanConfig', attrib={'name': 'Full audit', 'templateID': 'full-audit'})
        xmlTree = ElementTree(siteSaveRequest)
        f = BytesIO()
        xmlTree.write(f, encoding='utf-8',
                      xml_declaration=True)  # required so that xml declarations will come up in generated XML
        saveSiteReqXML = f.getvalue().decode("utf-8")  # converts bytes to string
        # print(saveSiteReqXML)
        responseXML = self.makeRequest(saveSiteReqXML)
        tree = ElementTree(fromstring(responseXML))
        root = tree.getroot()
        addSiteResponse = root.get('success')
        if (addSiteResponse == "1"):
            self.site_id = root.get('site-id')
            PrintUtil.printSuccess("Created site with site-id: " + self.site_id)
        else:
            fa = root.find('Failure')
            ex = fa.find('Exception')
            msg = ex.find('message').text
            PrintUtil.printError("Site creation failed: " + msg)

    def addUser(self, access_req):
        # print("addUser Module")
        usrLst = access_req['userList']
        for user in usrLst:
            usrSaveRequest = Element('UserSaveRequest', attrib={'session-id': self.session_id})
            userinfo = user.split(',')  # uname,name,email
            pswd = userinfo[0] + '!vul5c4p1'
            usrConfig_elem = SubElement(usrSaveRequest, 'UserConfig',
                                        attrib={'id': '-1', 'role-name': 'user', 'authsrcid': '-1', 'enabled': '1',
                                                'name': userinfo[0], 'fullname': userinfo[1], 'email': userinfo[2],
                                                'password': pswd})
            sites_elem = SubElement(usrConfig_elem, 'UserSite')
            site_elem = SubElement(sites_elem, 'site', attrib={'id': self.site_id})
            site_elem.text = access_req['site_name']
            xmlTree = ElementTree(usrSaveRequest)
            f = BytesIO()
            xmlTree.write(f, encoding='utf-8',
                          xml_declaration=True)  # required so that xml declarations will come up in generated XML
            usrSaveReqXML = f.getvalue().decode("utf-8")  # converts bytes to string
            # print(usrSaveReqXML)
            responseXML = self.makeRequest(usrSaveReqXML)
            # print(responseXML)
            tree = ElementTree(fromstring(responseXML))
            root = tree.getroot()
            addUserReq = root.get('success')
            if (addUserReq == "1"):
                PrintUtil.printSuccess("Created user: " + userinfo[0])
            else:
                fa = root.find('Failure')
                ex = fa.find('Exception')
                msg = ex.find('message').text
                PrintUtil.printError("User creation failed: " + msg)

    def handleAccessReq(self, access_req):
        # print("TestMofule")
        self.addSite(access_req)
        self.addUser(access_req)
        self.logoutOperation()

    def logoutOperation(self):
        print("Executing del")
        xmlReq = Element('LogoutRequest', attrib={'session-id': self.session_id})
        xmlTree = ElementTree(xmlReq)
        f = BytesIO()
        xmlTree.write(f, encoding='utf-8',
                      xml_declaration=True)  # required so that xml declarations will come up in generated XML
        logoutReqXML = f.getvalue().decode("utf-8")  # converts bytes to string
        print(logoutReqXML)
        responseXML = self.makeRequest(logoutReqXML)
        tree = ElementTree(fromstring(responseXML))
        root = tree.getroot()
        logoutResponse = root.get('success')
        if (logoutResponse == "1"):
            self.session_id = root.get('session-id')
            PrintUtil.printSuccess("Logged out of Nexpose Scanner")
        else:
            fa = root.find('Failure')
            ex = fa.find('Exception')
            msg = ex.find('message').text
            PrintUtil.printError("Logout Failure: " + msg)


            # API v1.1 SiteConfig- Provide the configuration of the site, including its associated assets.
            # API v1.1 SiteSave- Save changes to a new or existing site.
            # def userManagement():
            # API v1.1 UserSave- Create a new user account, or update the settings for an existing account.
            # def _del_(self):
            # API v1.1 Logout and close the session

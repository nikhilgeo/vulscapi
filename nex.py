from xml.etree.ElementTree import Element, SubElement, ElementTree
from defusedxml.ElementTree import parse, fromstring
from io import BytesIO
import requests

import util
from util import Utilities


# Have not used the diffusedXML library as the XML construction functions is only done here and they are not supported.
class Nexpose:
    """All the Nexpose API are handled here"""

    # Payload type XML
    # self. - for all members that are common to the object without self scope is limited to the block
    # self must the default mandatory parameter in all member functions
    # Caution !!: __init__ have two underscores on each side

    def makeRequest(self, url, payload, headers):
        response = requests.post(url, data=payload, headers=headers, verify=False)
        # print(response.text)
        return response.content

    def __init__(self, scanner_info):
        try:
            self.nexpose_host = scanner_info['host']
            self.reqURL = self.nexpose_host + "/api/1.1/xml"
            self.headers = {'Content-Type': 'text/xml'}
            self.login_try = 0
        except Exception as e:
            Utilities.printException(str(e))

    def login_nexpose(self, scanner_info):
        # API v1.1 Login and get the session here
        max_login_try_limit = 2

        while True:
            if self.login_try == 0:
                xmlReq = Element('LoginRequest', attrib={'user-id': scanner_info['uname'], 'password': scanner_info['passwd']})
            elif self.login_try > 0 and self.login_try < max_login_try_limit:
                usr_name = input("Please enter your username for " + " Nexpose" + ": ")
                usr_passwd = input("Please enter your password for " + " Nexpose" + ": ")
                xmlReq = Element('LoginRequest', attrib={'user-id': usr_name, 'password': usr_passwd})
            else:
                Utilities.printError("Nexpose login attemts exceded maximum limit, skipping Nexpose tasks..")
                return False

            xmlReq = Element('LoginRequest', attrib={'user-id': scanner_info['uname'], 'password': scanner_info['passwd']})
            xmlTree = ElementTree(xmlReq)
            f = BytesIO()
            xmlTree.write(f, encoding='utf-8', xml_declaration=True)  # required so that xml declarations will come up in generated XML
            loginReqXML = f.getvalue().decode("utf-8")  # converts bytes to string
            # print(self.loginReqXML)
            responseXML = self.makeRequest(self.reqURL, loginReqXML, self.headers)
            tree = ElementTree(fromstring(responseXML))
            root = tree.getroot()
            loginResponse = root.get('success')
            if (loginResponse == "1"):
                self.session_id = root.get('session-id')
                Utilities.printSuccess("Logged in to Nexpose Scanner")
                return True
            else:
                fa = root.find('Failure')
                ex = fa.find('Exception')
                msg = ex.find('message').text
                Utilities.printError("Login Failure: " + msg)
                self.login_try += 1


    # API v1.1 SiteSave- Save changes to a new or existing site.
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
        responseXML = self.makeRequest(self.reqURL, saveSiteReqXML, self.headers)
        tree = ElementTree(fromstring(responseXML))
        root = tree.getroot()
        addSiteResponse = root.get('success')
        if (addSiteResponse == "1"):
            self.site_id = root.get('site-id')
            Utilities.printSuccess("Created site with site-id: " + self.site_id)
            return True
        else:
            fa = root.find('Failure')
            ex = fa.find('Exception')
            msg = ex.find('message').text
            Utilities.printError("Site creation failed: " + msg)
            return False

    # API v1.1 UserSave- Create a new user account, or update the settings for an existing account.
    def addUser(self, access_req):
        # print("addUser Module")
        usrLst = access_req['userList']
        for user in usrLst:
            usrSaveRequest = Element('UserSaveRequest', attrib={'session-id': self.session_id})
            userinfo = user.split(',')  # uname,name,email
            pswd = Utilities.gen_code()
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
            responseXML = self.makeRequest(self.reqURL, usrSaveReqXML, self.headers)
            # print(responseXML)
            tree = ElementTree(fromstring(responseXML))
            root = tree.getroot()
            addUserReq = root.get('success')
            if (addUserReq == "1"):
                Utilities.printSuccess("Created user: " + userinfo[0])
            else:
                fa = root.find('Failure')
                ex = fa.find('Exception')
                msg = ex.find('message').text
                Utilities.printError("User creation failed: " + msg)

    def handleAccessReq(self, access_req, scanner_info):
        # print("TestMofule")
        if self.login_nexpose(scanner_info):
            addSiteStatus = self.addSite(access_req)
            if addSiteStatus:
                self.addUser(access_req)
            else:
                Utilities.printError("Site creation failed, aborting user creation..")
            self.logoutOperation()

    # API v1.1 Logout and close the session
    def logoutOperation(self):
        xmlReq = Element('LogoutRequest', attrib={'session-id': self.session_id})
        xmlTree = ElementTree(xmlReq)
        f = BytesIO()
        xmlTree.write(f, encoding='utf-8',
                      xml_declaration=True)  # required so that xml declarations will come up in generated XML
        logoutReqXML = f.getvalue().decode("utf-8")  # converts bytes to string
        # print(logoutReqXML)
        responseXML = self.makeRequest(self.reqURL, logoutReqXML, self.headers)

        tree = ElementTree(fromstring(responseXML))
        root = tree.getroot()
        logoutResponse = root.get('success')
        if (logoutResponse == "1"):
            self.session_id = root.get('session-id')
            Utilities.printSuccess("Logged out of Nexpose Scanner")
        else:
            fa = root.find('Failure')
            ex = fa.find('Exception')
            msg = ex.find('message').text
            Utilities.printError("Logout Failure: " + msg)

import requests
from defusedxml.ElementTree import fromstring
from xml.etree.ElementTree import ElementTree

from util import PrintUtil


class Qualys:
    ''' All Qualys related functions are handled here '''

    # Account Location Qualys US Platform 1 | API Server URL: https://qualysapi.qualys.com
    # URL encode variables when using the Qualys API.
    # URL elements are case sensitive.
    # Concurrency Limit, Rate Limit, Maximum number of API calls per Subscription (per API).

    # Bloody Qualys, why can't u have a single API interface & both with different authentication methods !! F#@$
    # API v2 -- Asset Management, Session Based Login & Basic HTTP auth also
    # Required Header Parameter  "X-Requested-With: <user description, like a user agent>"
    # Login request returns a session ID in the Set-Cookie HTTP header
    # Include the session ID in the cookie header for each request
    # API v1 -- User Management, Basic HTTP Authentication
    # Qualys account credentials are transmitted over HTTPS for each API call

    def __init__(self, scanner_info):
        self.qualys_host = scanner_info['host']
        self.headers = {'X-Requested-With': 'vulscapi'}
        self.uname = scanner_info['uname']
        self.passwd = scanner_info['passwd']
        self.login_try = 0


    def add_asset(self, access_req):
        self.url = self.qualys_host + "/api/2.0/fo/asset/ip/"
        params = {'action': 'add', 'ips': access_req['ip'], 'enable_vm': '1'}
        max_login_try_limit = 2

        while True:  # Login check done here, if it fails here then rest all task is skipped
            if (self.login_try > 0) and (self.login_try < max_login_try_limit):
                self.uname = input("Please enter your username for " + " Qualys" + ": ")
                self.passwd = input("Please enter your password for " + " Qualys" + ": ")
            elif self.login_try >= max_login_try_limit:
                PrintUtil.printError("Qualys login attemts exceded maximum limit, skipping Qualys tasks..")
                return False
            response_aasset_add = self.makeRequest(params)
            # print(response_aasset_add.content)
            responseXML = response_aasset_add.content
            tree = ElementTree(fromstring(responseXML))
            root = tree.getroot()
            asset_response = root.find('RESPONSE')
            asset_status = asset_response.find('TEXT').text
            if asset_status == "IPs successfully added to Vulnerability Management":
                PrintUtil.printSuccess("Asset added to Qualys Scanner")
                return True
            elif asset_status == "Bad Login/Password":
                PrintUtil.printError("Qualys login failed..")
                self.login_try += 1
            else:
                PrintUtil.printError("Asset adition Failure: " + asset_status)
                PrintUtil.printLog("Skipping remaning Qualys tasks..")
                return False

    def add_asset_grp(self, access_req):
        scanner_id = self.get_scanners()
        self.url = self.qualys_host + "/api/2.0/fo/asset/group/"
        if scanner_id is not None:
            params = {'action': 'add', 'ips': access_req['ip'], 'title': access_req['site_name'], 'appliance_ids':scanner_id}
            # print(self.url)
            response_asset_grp_add = self.makeRequest(params)
            # print(response_asset_grp_add.content)
            responseXML = response_asset_grp_add.content
            tree = ElementTree(fromstring(responseXML))
            root = tree.getroot()
            asset_response = root.find('RESPONSE')
            asset_status = asset_response.find('TEXT').text
            if asset_status == "Asset Group successfully added.":
                PrintUtil.printSuccess("Asset group added to Qualys Scanner")
                return True
            else:
                PrintUtil.printError("Asset group addition Failure: " + asset_status)
                PrintUtil.printLog("Skipping remaning Qualys tasks..")
                return False
        else:
            PrintUtil.printError("Asset Group adition Failure: Scanner id not found")
            return False

    def get_scanners(self):

        self.url = self.qualys_host + "/api/2.0/fo/appliance/"
        parms = {'action': 'list'}
        response_get_scanners = self.makeRequest(parms)
        # print(response_get_scanners.content)
        responseXML = response_get_scanners.content
        tree = ElementTree(fromstring(responseXML))
        root = tree.getroot()
        if root.find('RESPONSE') is not None:
            response = root.find('RESPONSE')
        if response.find('APPLIANCE_LIST') is not None:
            appliance_list = response.find('APPLIANCE_LIST')
            appliance = appliance_list.findall('APPLIANCE')  # we take only the first appliance, coz no multiple appliance nw.
            appliance_id = appliance[0].find('ID').text
        if response.find('TEXT') is not None: # Error condition
            PrintUtil.printError("Failure to get the scanner list: "+ response.find('TEXT').text)
            appliance_id = None
        # print(appliance_id)
        return appliance_id

    def makeRequest(self, parms):
        response = requests.post(self.url, headers=self.headers, params=parms, verify=False,
                                 auth=(self.uname, self.passwd))
        # print(response.headers)
        # print(response.url)
        return response

    def add_user(self, access_req):
        self.url = self.qualys_host + "/msp/user.php"

        usrLst = access_req['userList']
        for user in usrLst:
            userinfo = user.split(',')  # uname,name,email
            pswd = userinfo[0] + '!vul5c4p1'
            parms = {'action': 'add', 'user_role': 'scanner', 'business_unit': 'Unassigned',
                     'asset_groups': access_req['site_name'], 'first_name': userinfo[1].split(' ')[0],
                     'last_name': userinfo[1].split(' ')[1], 'title': 'Scanner User', 'phone': '0000000000',
                     'email': userinfo[2], 'address1': '3401 Hillview Ave', 'city': 'Palo Alto',
                     'country': 'United States of America', 'state': 'California', 'zip_code': '94304',
                     'send_email': '1'}
            response_user_add = self.makeRequest(parms)
            # print(response_user_add.content)
            responseXML = response_user_add.content
            tree = ElementTree(fromstring(responseXML))
            root = tree.getroot()
            asset_response = root.find('RETURN')
            user_add_status = asset_response.get('status')
            user_add_status_msg = asset_response.find('MESSAGE').text
            # print(user_add_status + user_add_status_msg)
            if user_add_status == "SUCCESS":
                PrintUtil.printSuccess( user_add_status_msg +" for " + userinfo[1])
                return True
            else:
                PrintUtil.printError("User addition Failure: " + user_add_status_msg)
                return False

    def handleAccessReq(self, access_req, scanner_info):
        try:
            asset_adittion_success = self.add_asset(access_req)
            if asset_adittion_success:
                asset_grp_add_status = self.add_asset_grp(access_req)
                if asset_grp_add_status:
                    create_user_status = self.add_user(access_req)
                # self.logout_user()
        except Exception as e:
            PrintUtil.printException(str(e))

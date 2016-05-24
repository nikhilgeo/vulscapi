import requests
from defusedxml.ElementTree import parse, fromstring
from xml.etree.ElementTree import Element, SubElement, ElementTree

from util import PrintUtil


class Qualys:
    '''All Qualys related functions are handled here'''

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


    def login(self, scanner_info):
        self.qualys_host = scanner_info['host']
        self.url = self.qualys_host + "/api/2.0/fo/session/"
        self.cookie = ""
        self.headers = {'X-Requested-With': 'vulscapi'}
        self.payload = {"action": "login", "username": scanner_info['uname'], "password": scanner_info['passwd']}
        response = self.makeRequest()
        if 'Set-Cookie' in response.headers:  # check if Set-Cookie is header is returned or not
            # print(response.headers['Set-Cookie'])  # QualysSession=XXXXXXXXXXXXXXXXXXX; path=/api; secure
            split1 = response.headers['Set-Cookie'].split(';')
            QualysSession = split1[0].split('=')
            self.cookie = {'QualysSession': QualysSession[1]}
            # print(self.cookie)
        print(response.text)
        responseXML = response.content
        tree = ElementTree(fromstring(responseXML))
        root = tree.getroot()
        login_response = root.find('RESPONSE')
        login_status = login_response.find('TEXT').text
        if login_status == "Logged in":
            PrintUtil.printSuccess("Logged in to Qualys Scanner")
            return True
        else:
            PrintUtil.printError("Login Failure: " + login_status)
            return False

    def add_asset(self, access_req):


    def makeRequest(self):
        response = requests.post(self.url, data=self.payload, cookies=self.cookie, headers=self.headers, verify=False)
        print(response.headers)
        return response

    def handleAccessReq(self, access_req, scanner_info):
        try:
            login_success = self.login(scanner_info)
            if login_success:
                asset_adittion_success = self.add_asset(access_req)
                if asset_adittion_success:
                    # create_user_status = self.create_user(access_req, )
                    # self.logout_user()
        except Exception as e:
            PrintUtil.printException(str(e))

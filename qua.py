import requests
from defusedxml.ElementTree import parse, fromstring
from xml.etree.ElementTree import Element, SubElement, ElementTree
from requests.auth import HTTPBasicAuth

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


    def __init__(self, scanner_info):
        self.qualys_host = scanner_info['host']
        self.headers = {'X-Requested-With': 'vulscapi'}
        self.uname = scanner_info['uname']
        self.passwd = scanner_info['passwd']


    def add_asset(self, access_req):
        self.url = self.qualys_host + "/api/2.0/fo/asset/ip/?action=add"
        self.url = self.url + "&ips=" +access_req['ip'] +"&enable_vm=1"
        response_aasset_add = self.makeRequest()
        print(response_aasset_add.content)
        responseXML = response_aasset_add.content
        tree = ElementTree(fromstring(responseXML))
        root = tree.getroot()
        asset_response = root.find('RESPONSE')
        asset_status = asset_response.find('TEXT').text
        if asset_status == "IPs successfully added to Vulnerability Management":
            PrintUtil.printSuccess("Asset added to Qualys Scanner")
            return True
        else:
            PrintUtil.printError("Asset adition Failure: " + asset_status)
            return False


    def makeRequest(self):
        response = requests.post(self.url, headers=self.headers, verify=False, auth=(self.uname, self.passwd))
        print(response.headers)
        return response

    def handleAccessReq(self, access_req, scanner_info):
        try:
            asset_adittion_success = self.add_asset(access_req)
                # if asset_adittion_success:
                # create_user_status = self.create_user(access_req, )
                # self.logout_user()
        except Exception as e:
            PrintUtil.printException(str(e))

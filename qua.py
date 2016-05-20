import requests
from util import PrintUtil
class Qualys:
    '''All Qualys related functions are handled here'''
    # Account Location Qualys US Platform 1 | API Server URL: https://qualysapi.qualys.com
    # URL encode variables when using the Qualys API.
    # URL elements are case sensitive.
    # Concurrency Limit, Rate Limit, Maximum number of API calls per Subscription (per API).
    # Required Header Parameter  "X-Requested-With: <user description, like a user agent>"
    # Login request returns a session ID in the Set-Cookie HTTP header
    # Include the session ID in the cookie header for each request

    def __init__(self, scanner_info):
        # log in to Qualys
        # Get the session
        self.qualys_host = scanner_info['host']
        self.url = self.qualys_host + "/api/2.0/fo/session/"
        self.headers = {'X-Requested-With': 'vulscapi'}
        self.payload = {"action":"login","username":scanner_info['uname'],"password":scanner_info['passwd']}
        self.makeRequest()


    def makeRequest(self):
        response = requests.post(self.url, data=self.payload, headers=self.headers, verify=False)
        print(response.headers)
        print(response.headers['Set-Cookie'])
        print(response.text)
        return response.content
'''
    def handleAccessReq(self, access_req):
        try:
            #create_user_status = self.create_user(access_req)
            #self.logout_user()
        except Exception as e:
            PrintUtil.printException(str(e))
'''
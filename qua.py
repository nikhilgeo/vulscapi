import requests
class qualys:
    '''All Qualys related functions are handled here'''
    # Account Location Qualys US Platform 1 | API Server URL: https://qualysapi.qualys.com
    # URL encode variables when using the Qualys API.
    # URL elements are case sensitive.
    # Concurrency Limit, Rate Limit, Maximum number of API calls per Subscription (per API).
    # Required Header Parameter  "X-Requested-With: <user description, like a user agent>"
    # Login request returns a session ID in the Set-Cookie HTTP header

    def __init__(self, scanner_info):
        # log in to Qualys
        # Get the session
        self.qualys_host = scanner_info['host']
        self.headers = {'X-Requested-With': 'vulscapi'}
        self.payload = "action=login&username="+scanner_info['uname']+"&password="+scanner_info['passwd']


    def makeRequest(self):
        response = requests.post(self.url, data=self.payload, headers=self.headers, verify=False)
        #print(response.text)
        return response.content

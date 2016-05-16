import json
import util
from util import PrintUtil

class Nessus:
    """All Nessus related functions are handled here"""

    # Payload type JSON
    # Login:Nessus.session: create
    # Create User: Nessus.users: create
    # Logout:Nessus.session: destroy

    def __init__(self, scanner_info):
        try:
            # Login and get the session here
            self.nessus_host = scanner_info['host']
            sessionreqURL = self.nessus_host + "/session"
            payload = {'username': scanner_info['uname'], 'password': scanner_info['passwd']}
            response = util.makeRequest(sessionreqURL, json.dumps(payload), "json")
            print(json.dumps(response))
            '''
            loginResponse = root.get('success')
            if (loginResponse == "1"):
                self.session_id = root.get('session-id')
                PrintUtil.printSuccess("Logged in to Nexpose Scanner")
            else:
                fa = root.find('Failure')
                ex = fa.find('Exception')
                msg = ex.find('message').text
                PrintUtil.printError("Login Failure: " + msg)
            '''
        except Exception as e:
            PrintUtil.printException(str(e))

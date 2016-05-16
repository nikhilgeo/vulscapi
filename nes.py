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
            json_rep = json.loads(response.decode("utf-8"))  # convert to string then convert to json
            #print(json_rep)
            if 'error' in json_rep:
                PrintUtil.printError("Login Failure: " + json_rep['error'])
                return
            if 'token' in json_rep:
                PrintUtil.printSuccess("Logged in to Nessus Scanner")
                self.session_token = json_rep['token']
        except Exception as e:
            PrintUtil.printException(str(e))

import json
import util
from util import Utilities
import requests


class Nessus:
    """All Nessus related functions are here"""

    # Payload type JSON
    # Login:Nessus.session: create | Add it to your request using the following HTTP header: X-Cookie: token={token};
    # Create User: Nessus.users: create
    # Logout:Nessus.session: destroy

    def __init__(self, scanner_info):
        try:
            # Login and get the session here
            self.nessus_host = scanner_info['host']
            self.headers = {'Content-Type': 'application/json'}
            self.login_try = 0
        except Exception as e:
            PrintUtil.printException(str(e))

    def makeRequest(self, url, payload, headers, method="POST"):
        if method == "POST":
            response = requests.post(url, data=payload, headers=headers, verify=False)
            self.status_code = response.status_code
        if method == "DELETE":
            response = requests.delete(url, headers=headers, verify=False)
            self.status_code = response.status_code
            # print(response.text)
        return response.content

    def login_nessus(self, scanner_info):
        sessionreqURL = self.nessus_host + "/session"
        max_login_try_limit = 2
        while True:
            if self.login_try == 0:
                payload = {'username': scanner_info['uname'], 'password': scanner_info['passwd']}
            elif self.login_try > 0 and self.login_try < max_login_try_limit:
                usr_name = input("Please enter your username for " + " Nessus" + ": ")
                usr_passwd = input("Please enter your password for " + " Nessus" + ": ")
                payload = {'username': usr_name, 'password': usr_passwd}
            else:
                Utilities.printError("Nessus login attemts exceded maximum limit, skipping Nessus tasks..")
                return False

            response = self.makeRequest(sessionreqURL, json.dumps(payload), self.headers)
            json_rep = json.loads(response.decode("utf-8"))  # convert to string then convert to json
            # print(json_rep)
            if self.status_code == 200:
                self.session_token = json_rep['token']
                self.headers.update({'X-Cookie': 'token=' + self.session_token})  # session token added to HTTP header
                # print(self.headers)
                Utilities.printSuccess("Logged in to Nessus Scanner")
                return True
            elif self.status_code == 400:
                Utilities.printError("Login Failure: username format is not valid")
                self.login_try += 1
            elif self.status_code == 401:
                Utilities.printError("Login Failure: username or password is invalid")
                self.login_try += 1
            elif self.status_code == 500:
                Utilities.printError("Login Failure:  too many users are connected")
                self.login_try += 1

    def create_user(self, access_req):
        try:
            # Create User
            create_user_URL = self.nessus_host + "/users"
            usrLst = access_req['userList']
            for user in usrLst:
                userinfo = user.split(',')  # uname,name,email
                pswd = Utilities.gen_code()
                payload = {'username': userinfo[0], 'password': pswd, 'permissions': '32',
                           'name': userinfo[1], 'email': userinfo[2], 'type': 'local'}
                response = self.makeRequest(create_user_URL, json.dumps(payload), self.headers)
                json_rep = json.loads(response.decode("utf-8"))
                # print(json_rep)
                if self.status_code == 200:
                    Utilities.printSuccess("Created user: " + userinfo[1])
                if self.status_code == 400:
                    Utilities.printError("User creation Failure: Invalid field request")
                if self.status_code == 403:
                    Utilities.printError("User creation Failure: No permission to create a user")
                if self.status_code == 409:
                    Utilities.printError("User creation Failure: Duplicate username")

        except Exception as e:
            Utilities.printException(str(e))

    def logout_user(self):
        try:
            # destroy the user session
            logoutURL = self.nessus_host + "/session"
            response = self.makeRequest(logoutURL, {}, self.headers, "DELETE")
            if self.status_code == 200:
                Utilities.printSuccess("Logged out of Nessus Scanner")
            if self.status_code == 401:
                Utilities.printSuccess("Logged out failure: No session exists")
        except Exception as e:
            Utilities.printException(str(e))

    def handleAccessReq(self, access_req, scanner_info):
        try:
            if self.login_nessus(scanner_info):
                create_user_status = self.create_user(access_req)
                self.logout_user()
        except Exception as e:
            Utilities.printException(str(e))

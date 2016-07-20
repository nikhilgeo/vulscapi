import requests
from defusedxml.ElementTree import fromstring
import xml.etree.ElementTree as ET
from util import Utilities
import shutil
import time
import datetime
import sys


class Qualys:
    """ All Qualys related functions are handled here """

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

    def __init__(self): #for scan 
        print()

    def add_asset(self, access_req):
        self.url = self.qualys_host + "/api/2.0/fo/asset/ip/"
        params = {'action': 'add', 'ips': access_req['ip'], 'enable_vm': '1'}
        max_login_try_limit = 2

        while True:  # Login check done here, if it fails here then rest all task is skipped
            if (self.login_try > 0) and (self.login_try < max_login_try_limit):
                self.uname = input("Please enter your username for " + " Qualys" + ": ")
                self.passwd = input("Please enter your password for " + " Qualys" + ": ")
            elif self.login_try >= max_login_try_limit:
                Utilities.printError("Qualys login attemts exceded maximum limit, skipping Qualys tasks..")
                return False
            response_aasset_add = self.makeRequest(params)
            # print(response_aasset_add.content)
            responseXML = response_aasset_add.content
            tree = ElementTree(fromstring(responseXML))
            root = tree.getroot()
            asset_response = root.find('RESPONSE')
            asset_status = asset_response.find('TEXT').text
            if asset_status == "IPs successfully added to Vulnerability Management":
                Utilities.printSuccess("Asset added to Qualys Scanner")
                return True
            elif asset_status == "Bad Login/Password":
                Utilities.printError("Qualys login failed..")
                self.login_try += 1
            else:
                Utilities.printError("Asset adition Failure: " + asset_status)
                Utilities.printLog("Skipping remaning Qualys tasks..")
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
                Utilities.printSuccess("Asset group added to Qualys Scanner")
                return True
            else:
                Utilities.printError("Asset group addition Failure: " + asset_status)
                Utilities.printLog("Skipping remaning Qualys tasks..")
                return False
        else:
            Utilities.printError("Asset Group adition Failure: Scanner id not found")
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
            Utilities.printError("Failure to get the scanner list: "+ response.find('TEXT').text)
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
                Utilities.printSuccess( user_add_status_msg +" for " + userinfo[1])
                return True
            else:
                Utilities.printError("User addition Failure: " + user_add_status_msg)
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
            Utilities.printException(str(e))

#----------------------scan related methods start here--------------------------

    def login(self, s, username, password):
        payload = {
               'action':'login',
               'username':username,
               'password':password
              }

        r = s.post('https://qualysapi.qualys.com/api/2.0/fo/session/', data=payload)
        xmlreturn = ET.fromstring(r.text)
        for elem in xmlreturn.findall('.//TEXT'):
            Utilities.printLog(elem.text)

        Utilities.printLog("Cookie: QualysSession = " + r.cookies['QualysSession'])

    def logout(self, s):
        payload = {
                 'action':'logout'
                }

        r = s.post('https://qualysapi.qualys.com/api/2.0/fo/session/', data=payload)
        xmlreturn = ET.fromstring(r.text)
        for elem in xmlreturn.findall('.//TEXT'):
            Utilities.printLog(elem.text)

    def add_IP(self, s, target_IP):
        #set up host authentication
        payload = {
                   'action':'add',
                   'ips':target_IP,
                   'enable_vm':1,
                   'enable_pc':0,
                   }

        r = s.post('https://qualysapi.qualys.com/api/2.0/fo/asset/ip/', data=payload)
        xmlreturn = ET.fromstring(r.text)
        for elem in xmlreturn.findall('.//TEXT'):
            if "action has invalid value" in elem.text:
                Utilities.printError("You do not have permissions do add IP(s)")
            else:
                Utilities.printSuccess(elem.text)

    def setup_auth(self, s, target_IP, username, password, title):
        #set up host authentication
        status = "Success"
        payload = {
                   'action':'create',
                   'title':title+'_'+target_IP,
                   'ips':target_IP,
                   'username':username,
                   'password':password,
                   }

        r = s.post('https://qualysapi.qualys.com/api/2.0/fo/auth/unix/', data=payload)
        xmlreturn = ET.fromstring(r.text)
        for elem in xmlreturn.findall('.//TEXT'):
            if "action has invalid value" in elem.text:
                Utilities.printError("You do not have permissions do add authentication records")
            else:
                Utilities.printSuccess("Authentication Record " + elem.text)

            if "existing scan auth record has the specified title" in elem.text:
                #delete the auth record
                payload = {
                           'action':'list',
                           'title':target_IP
                           }
                r = s.post('https://qualysapi.qualys.com/api/2.0/fo/auth/unix/', data=payload)
                xmlreturn = ET.fromstring(r.text)
                for elem in xmlreturn.findall('.//AUTH_UNIX'):
                    title_id = elem[0].text

                payload = {
                           'action':'delete',
                           'ids':title_id,
                           }
                r = s.post('https://qualysapi.qualys.com/api/2.0/fo/auth/unix/', data=payload)
                xmlreturn = ET.fromstring(r.text)
                for elem in xmlreturn.findall('.//TEXT'):
                    status = elem.text
                    Utilities.printLog("Authentication Record " + status)
                    self.setup_auth(s, target_IP, username, password, title)
            elif "one or more of the specified IPs" in elem.text:
                #delete the auth record
                status = "Failure"
                Utilities.printError("---\nPlease note:\nIP exists in another authentication record\nQualys doesn't support multiple authentication record of same type for any IP\nPlease delete the existing authentication record manually to proceed.\n---")
        return status

    def launch_scan(self, s, target_IP, scan_option_id):
        # launching the scan
        scan_ref = ""
        payload = {
                   'action':'launch',
                   'ip':target_IP,
                   'iscanner_name':'is_vmwar_as',
                   'option_id':scan_option_id, #'797901',
                   'scan_title':target_IP,
                   }

        r = s.post('https://qualysapi.qualys.com/api/2.0/fo/scan/', data=payload)
        xmlreturn = ET.fromstring(r.text)
        for elem in xmlreturn.findall('.//ITEM'):
            if (elem[0].text == 'REFERENCE'):
                scan_ref = elem[1].text

        for elem in xmlreturn.findall('.//TEXT'):
            if "none of the specified IPs are eligible" in elem.text:
                Utilities.printError("You do not have permissions to run scans on IP " + target_IP)
            else:
                Utilities.printLog(elem.text)

        if "scan" in scan_ref:
            Utilities.printLog("Scan Reference Number: " + scan_ref)
        else:
            scan_ref = "SCAN_NOT_STARTED"
        return scan_ref

    def check_scan(self, s, scan_ref):
        # checks the status of the scan
        state = "Default"
        payload = {
                   'action':'list',
                   'scan_ref':scan_ref,
                   }
        r = s.post('https://qualysapi.qualys.com/api/2.0/fo/scan/', data=payload)
        xmlreturn = ET.fromstring(r.text)
        code = xmlreturn.find('.//CODE')
        status = xmlreturn.find('.//STATUS')
        text = xmlreturn.find('.//TEXT')

        if status != None:
            state = status[0].text

        if code != None:
            if text != None:
                Utilities.printError("Error Text: " + text.text)

        Utilities.printLog("Scan status: " + state)
        return state

    def launch_report(self, s, scan_ref, report_type, target_IP, report_template_id):
        # launching report
        report_ID = ""
        payload = {
                   'action':'launch',
                   'report_type':'Scan',
                   'template_id':report_template_id,#'991466',
                   'output_format':report_type,
                   'report_refs':scan_ref,
                   'report_title':target_IP,
                   }

        r = s.post('https://qualysapi.qualys.com/api/2.0/fo/report/', data=payload)
        xmlreturn = ET.fromstring(r.text)
        for elem in xmlreturn.findall('.//ITEM'):
            if (elem[0].text == 'ID'):
                report_ID = elem[1].text

        Utilities.printLog("Report ID: " + report_ID)
        return report_ID

    def check_report(self, s, report_ID):
        # check reports
        status = ""
        payload = {
                   'action':'list',
                   'id':report_ID,
                   }
        r = s.post('https://qualysapi.qualys.com/api/2.0/fo/report/', data=payload)
        xmlreturn = ET.fromstring(r.text)
        for elem in xmlreturn.findall('.//STATUS'):
            status = elem[0].text

        return status

    def download_report(self, s, report_ID, target_IP):
        # downloading the reports
        ts = time.time()
        dt = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%dT%H%M%S')
        #file format: report folder, IP, date-time stamp
        filename = "qualys_scan_report_"+target_IP+"_"+dt+".pdf"
        payload = {
                   'action':'fetch',
                   'id':report_ID,
                   }

        r = s.post('https://qualysapi.qualys.com/api/2.0/fo/report/', data=payload, stream=True)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                Utilities.printLog("report downloaded")
        else:
            Utilities.printError("report failed to download with status code: " + r1.status_code)

        #this is another way to save report
        #if the above method fails to save report correctly, use the below method
        '''
        time.sleep(10)
        ts = time.time()
        dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S')
        filename2 = target_IP+"_"+dt+".pdf"

        r2 = s.post('https://qualysapi.qualys.com/api/2.0/fo/report/', data=payload, stream=True)
        if r2.status_code == 200:
            with open(filename2, 'wb') as f:
                r2.raw.decode_content = True
                shutil.copyfileobj(r2.raw, f)
                Utilities.printLog("report downloaded")
        else:
            Utilities.printError("report failed to download with status code: " + r1.status_code)
        '''

    def quick_scan(self, s, target_IP, username, password, title, scan_option_id, report_template_id):
        Utilities.printLog("Quick Scan: " + target_IP)
        #add IPs
        self.add_IP(s, target_IP)

        #add authentication record
        status = self.setup_auth(s, target_IP, username, password, title).lower()
        if status == "failure":
            return

        #start the scan
        scan_ref = self.launch_scan(s, target_IP, scan_option_id)
        if scan_ref == "SCAN_NOT_STARTED":
            Utilities.printError("Scan has not started for IP: " + target_IP)
            return

        #check the scan status after every 100 seconds
        #add a new if statement for various check_scan return value that is discovered
        while 1:
            #waiting for 5 mins = 300
            time.sleep(300)
            status = self.check_scan(s, scan_ref).lower()
            if status == "finished":
                break
            elif status == "queued" or status == "loading" or status == "running":
                continue
            else:
                return

        #generate report after scan has completed
        report_type = 'pdf'
        report_ID = self.launch_report(s, scan_ref, report_type, target_IP, report_template_id)

        #waiting for report generation; then download report
        time.sleep(25)
        self.download_report(s, report_ID, target_IP)

    def scan(self):
        try:
            #read data from config file
            tree = ET.parse('host_details.xml')
            root = tree.getroot()
            username = root[0][0].text
            password = root[0][1].text

            #setup connection
            s = requests.Session()
            s.headers.update({'X-Requested-With':'Qualys Vuln Api Scan'})
            self.login(s, username, password)

        #scan each host
            for host in root.iter('host'):
                self.quick_scan(s, host[0].text, host[1].text, host[2].text, host[3].text, host[4].text, host[5].text)
        except:
            Utilities.printException("Unexpected error: " + sys.exc_info()[0])
            Utilities.printException("sys.exc_info(): " + sys.exc_info())
        finally:
            #always log out and close the session
            self.logout(s)
            s.close()

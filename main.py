from defusedxml.ElementTree import parse
import nex
import nes
import qua
from util import Utilities
import argparse
import sys



# Global variables

msg = ""

#---------------------Access Request Handler functions: Start----------------------------------------------------------
def xml_error(msg):
    Utilities.printError(msg)
    raise SystemExit


def readAccessReq():
    # read access request from XML
    try:
        ip = ""
        usrlst = []
        tree = parse('access_request.xml')
        root = tree.getroot()
        for child in root.findall('user'):
            uname = child.find('uname').text
            name = child.find('name').text
            email = child.find('email').text
            if uname is None or name is None or email is None:
                xml_error("Data missing in access_request.xml")
            usrlst.append(uname + ',' + name + ',' + email)
        asst_det = root.find('asset_details')
        site_det = root.find('site')
        site_name = site_det.get('name')
        site_desc = site_det.get('desc')
        for ipchild in asst_det.findall('ip'):
            if ipchild.text is None:
                xml_error("IP missing in access_request.xml")
            ip = ip + "," + ipchild.text

        # print(ip)
        ip = ip.strip(',')
        access_req = {'userList': usrlst, 'ip': ip, 'site_name': site_name, 'site_desc': site_desc}
        # print(access_req)
        return access_req
    except Exception as e:
            Utilities.printException("Error with access_request.xml."+ str(e))


def access_request_handler():
    access_details = readAccessReq()  # Reading the Access Request
    try:
        tree = parse('scanner_details.xml')  # Reading the Scanner Details
        root = tree.getroot()

        # Access request handler for scanners
        # Read Nessus scanner details
        scanner = root.find('nessus')
        execute_nessus = scanner.get('enabled')
        if execute_nessus == '1':
            # print(scanner)

            if scanner.find('host').text is None or scanner.find('username').text is None or scanner.find('host').text is None:
                xml_error("Nessus data missing in scanner_details.xml")
            print("Nessus" + " host@:" + scanner.find('host').text)
            # print(scanner.find('username').text)
            usr_passwd = input("Please enter your password for " + " Nessus" + ": ")
            nessus_details = {'uname': scanner.find('username').text, 'passwd': usr_passwd, 'host': scanner.find('host').text}
            # Scanner task calls from here
            Utilities.printLog("Executing Nessus tasks")
            nessusObj = nes.Nessus(nessus_details)  # Create Nessus scanner class obj
            msg = nessusObj.handleAccessReq(access_details, nessus_details)  # Login | Add User | Logout

        # Read Nexpose scanner details
        scanner = root.find('nexpose')
        execute_nexpose = scanner.get('enabled')
        if execute_nexpose == '1':
            # print(scanner)
            if scanner.find('host').text is None or scanner.find('username').text is None or scanner.find('host').text is None:
                xml_error("Nexpose data missing in scanner_details.xml")
            print("Nexpose" + " host@:" + scanner.find('host').text)
            # print(scanner.find('username').text)
            usr_passwd = input("Please enter your password for " + " Nexpose" + ": ")
            nexpose_details = {'uname': scanner.find('username').text, 'passwd': usr_passwd, 'host': scanner.find('host').text}
            # Scanner task calls from here
            Utilities.printLog("Executing Nexpose tasks")
            nexposeObj = nex.Nexpose(nexpose_details)  # Create Nexpose scanner class obj
            msg += "\n"+nexposeObj.handleAccessReq(access_details, nexpose_details)  # Login | SaveSite | Add User | Logout

        # Read Qualys scanner details
        scanner = root.find('qualys')
        execute_qualys = scanner.get('enabled')
        if execute_qualys == '1':
            # print(scanner)
            if scanner.find('host').text is None or scanner.find('username').text is None or scanner.find('host').text is None:
                xml_error("Qualys data missing in scanner_details.xml")
            print("Qualys" + " host@:" + scanner.find('host').text)
            # print(scanner.find('username').text)
            usr_passwd = input("Please enter your password for " + " Qualys" + ": ")
            qualys_details = {'uname': scanner.find('username').text, 'passwd': usr_passwd, 'host': scanner.find('host').text}
            # Scanner task calls from here
            Utilities.printLog("Executing Qualys tasks")
            qualysObj = qua.Qualys(qualys_details)  # Create Qualys scanner class obj
            qualysObj.handleAccessReq(access_details, qualys_details)  # Login | Add Asset | Add Asset Grp | Add User
            msg +="\nQualys\nDetails send to email."

        Utilities.write_to_file(msg)
    except Exception as e:
                Utilities.printException("In fun access_request_handler():"+ str(e))
#---------------------Access Request Handler functions: End------------------------------------------------------------


''' Execution entry point: It all starts from here '''

# runtime python version check
if sys.version_info[0] < 3:
    print("\033[96m Sorry, must be using Python 3 or greater\033[0m")  # The Class are bit different in py 2.X
    raise SystemExit



# Command line parameter handling
parser = argparse.ArgumentParser()
parser.add_argument("action", help="Scanner tasks", choices=['adduser', 'scan'])
args = parser.parse_args()
if args.action == 'adduser':
    access_request_handler()
if args.action == 'scan':
        print("Scanner Functions: TBD")


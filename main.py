from defusedxml.ElementTree import parse
import nex
import nes
import qua
from util import PrintUtil


# Global Varibale

execute_nessus = 0
execute_nexpose = 0
execute_qualys = 0


# read access request from XML
def readAccessReq():
    ip = ""
    usrlst = []
    tree = parse('access_request.xml')
    root = tree.getroot()
    for child in root.findall('user'):
        uname = child.find('uname').text
        name = child.find('name').text
        email = child.find('email').text
        usrlst.append(uname + ',' + name + ',' + email)
    asst_det = root.find('asset_details')
    site_det = root.find('site')
    site_name = site_det.get('name')
    site_desc = site_det.get('desc')
    for ipchild in asst_det.findall('ip'):
        ip = ip + "," + ipchild.text
    # print(ip)
    ip = ip.strip(',')
    access_req = {'userList': usrlst, 'ip': ip, 'site_name': site_name, 'site_desc': site_desc}
    # print(access_req)
    return access_req


# read the scanner details
def readScanner():
    tree = parse('scanner_details.xml')
    root = tree.getroot()
    scanner_details = []  # 0- Nessus 1-Nexpose 2-Qualys

    # Read Nessus scanner details
    scanner = root.find('nessus')
    execute_nessus = scanner.get('enabled')
    if execute_nessus == 1:
        # print(scanner)
        print("Nessus" + " host@:" + scanner.find('host').text)
        # print(scanner.find('username').text)
        usr_passwd = input("Please enter your password for " + " Nessus" + ": ")
        user_cred_nessus = {'uname': scanner.find('username').text, 'passwd': usr_passwd, 'host': scanner.find('host').text}
        scanner_details.append(user_cred_nessus)

    # Read Nexpose scanner details
    scanner = root.find('nexpose')
    execute_nexpose = scanner.get('enabled')
    if execute_nexpose == 1:
        # print(scanner)
        print("Nexpose" + " host@:" + scanner.find('host').text)
        # print(scanner.find('username').text)
        usr_passwd = input("Please enter your password for " + " Nexpose" + ": ")
        user_cred_nexpose = {'uname': scanner.find('username').text, 'passwd': usr_passwd, 'host': scanner.find('host').text}
        scanner_details.append(user_cred_nexpose)

    # Read Qualys scanner details
    scanner = root.find('qualys')
    execute_qualys = scanner.get('enabled')
    if execute_qualys == 1:
        # print(scanner)
        print("Qualys" + " host@:" + scanner.find('host').text)
        # print(scanner.find('username').text)
        usr_passwd = input("Please enter your password for " + " Qualys" + ": ")
        user_cred_qualys = {'uname': scanner.find('username').text, 'passwd': usr_passwd, 'host': scanner.find('host').text}
        scanner_details.append(user_cred_qualys)

    return scanner_details

''' Execution entry point from here '''

# Reading the Access Request
access_details = readAccessReq()
scanner_info = readScanner()  # 0- Nessus 1-Nexpose 2-Qualys

''' Nessus Scanner '''
if execute_nessus == 1:
    PrintUtil.printLog("Executing Nessus tasks")
    # Login into Nexpose scanner
    # nessusObj = nes.Nessus(scanner_info)
    # Add User
    # nessusObj.handleAccessReq(access_details)

''' Nexpose Scanner '''
if execute_nessus == 1:
    PrintUtil.printLog("Executing Nexpose tasks")
    # Login into Nexpose scanner
    # nexposeObj = nex.Nexpose(scanner_info)
    # SaveSite and Add User
    # nexposeObj.handleAccessReq(access_details)


''' Qualys Scanner '''
if execute_qualys == 1:
    PrintUtil.printLog("Executing Qualys tasks")
    # Login into Nexpose scanner
    # qualysObj = qua.Qualys(scanner_info)
    # Add User
    # qualysObj.handleAccessReq(access_details, scanner_info)

from defusedxml.ElementTree import parse
import nex
import nes
import qua
from util import PrintUtil


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
    print(access_req)
    return access_req


# read the scanner details
def readScanner(scannerName):
    tree = parse('scanner_details.xml')
    root = tree.getroot()
    scanner = root.find(scannerName)
    # print(scanner)
    print(scannerName + " Host@:" + scanner.find('host').text)
    # print(scanner.find('username').text)
    usr_passwd = input("Please enter your password for " + scannerName + ": ")
    user_cred = {'uname': scanner.find('username').text, 'passwd': usr_passwd, 'host': scanner.find('host').text}
    return user_cred


# Reading the Access Request
access_details = readAccessReq()


'''
# ******NEXPOSE******
# Read Nexpose Scanner Info, from config file
scanner_info = readScanner('nexpose')
# Login into Nexpose scanner
nexposeObj = nex.Nexpose(scanner_info)
# SaveSite and Add User
nexposeObj.handleAccessReq(access_details)
'''

'''
# ******NESSUS******
# Read Nexpose Scanner Info, from config file
scanner_info = readScanner('nessus')
# Login into Nexpose scanner
nessusObj = nes.Nessus(scanner_info)
# Add User
nessusObj.handleAccessReq(access_details)

#nexposeObj.handleAccessReq(access_details)
'''


# ******Qualys******
# Read Qualys Scanner Info, from config file
scanner_info = readScanner('qualys')
# Login into Nexpose scanner
qualysObj = qua.Qualys(scanner_info)
# Add User
qualysObj.handleAccessReq(access_details, scanner_info)

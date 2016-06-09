# from defusedxml.ElementTree import parse
#
# tree = parse('textXML.xml')
# root = tree.getroot()
# loginResponse = root.get('success')
# if (loginResponse == 1):
#     self.session_id = root.get('session-id')
# else:
#     fa = root.find('Failure')
#     ex = fa.find('Exception')
#     msg = ex.find('message').text
#     print('\033[93m' + "Login Failure: " + msg + '\033[0m')

# from util import Utilities
#
#
#
# import string
# import random
#
#
# def gen_code(size=16, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
#     return ''.join(random.SystemRandom().choice(chars) for _ in range(size))
#
# Utilities.printError(gen_code())


# msg = "outside\nnew\n"
#
# if True:
#     msg += "insideZZZZ121212ZZ"
#
# f = open('User_details_toMail.txt', 'w')
# f.writ

#
#
# from StringIO import StringIO
# from lxml import etree
#
# dtd = etree.DTD(StringIO("""<!ELEMENT foo EMPTY>"""))
# root = etree.XML("<foo/>")
# print(dtd.validate(root))
# # True
#
# root = etree.XML("<foo>bar</foo>")
# print(dtd.validate(root))
# # False
# print(dtd.error_log.filter_from_errors())
# # <string>:1:0:ERROR:VALID:DTD_NOT_EMPTY: Element foo was declared EMPTY this one has content




import argparse
parser = argparse.ArgumentParser()
parser.add_argument("action",help="Scanner tasks to perform", choices=['adduser','scan'])
args = parser.parse_args()
if args.action == 'adduser':
        print("adduser")
if args.action == 'scan':
        print("scan")

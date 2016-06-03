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

from util import Utilities



import string
import random


def gen_code(size=16, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

Utilities.printError(gen_code())

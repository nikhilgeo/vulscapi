import requests


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    EXCEPTION = '\033[96m'


class PrintUtil:
    def printSuccess(msg):
        print(bcolors.OKGREEN + "[OK]" + msg + bcolors.ENDC)

    def printError(msg):
        print(bcolors.FAIL + "[ERROR]" + msg + bcolors.ENDC)

    def printException(msg):
        print(bcolors.FAIL + "[EXCEPTION]" + msg + bcolors.ENDC)
    def printLog(msg):
        print(bcolors.OKBLUE + "[LOG]" + msg + bcolors.ENDC)

        # Make APIv1.1 POST requests

'''
def makeRequest(url, payload, headers, method="POST"):
    if method == "POST":
        response = requests.post(url, data=payload, headers=headers, verify=False)
    # print(response.text)
    return response.content
'''
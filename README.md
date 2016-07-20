# vulscapi
Python scripts for Nessus, Nexpose &amp; Qualys API's. Below listed are the implemented API calls.

**Nessus**
* Add User

**Nexpose**
* Add Site
* Add User

**Qualys**
* Add asset
* Add asset group
* Add user
* Quick scan

All the add user, add asset & add asset group functions(User access request functions) can be invoked by providing the user details and asset detail in **_access_request.xml_**

```
<?xml version="1.0" encoding="UTF-8"?>
<new_accessInfo>
      <user>
        <uname>Uname1</uname>
         <name>First Name</name>
         <email>email@emailprovider.com</email>
      </user>
      <user>
        <uname>Uname2</uname>
         <name>First2 Name2</name>
         <email>email2@emailprovider.com</email>
      </user>
   <asset_details>
      <ip>X.X.X.X</ip>
      <ip>X2.X2.X2.X2</ip>
      <ip>X3.X3.X3.X3</ip>
   </asset_details>
   <site name='site name' desc='site description'>
</new_accessInfo>
```

Scanner appliance information must be provided in **_scanner_details.xml_**

```
<?xml version="1.0" encoding="UTF-8"?>
<scanner_details>
      <nessus enabled=(1,0)>
         <host>nessus_host</host>
         <username>nessus_uname</username>
      </nessus>
      <nexpose enabled=(1,0)>
         <host>nexpose_host</host>
         <username>nexpose_uname</username>
      </nexpose>
      <qualys enabled=(1,0)>
         <host>qualys_host</host>
         <username>qualys_uname</username>
      </qualys>
</scanner_details>
```

For scanning a host, information must be provided in **_host_details.xml_**

```
<?xml version="1.0" encoding="UTF-8"?>
<data>
   <scan_details>
      <username>vmwar_hs</username>
      <password>Test123#</password>
      <email></email>
   </scan_details>
   <host_details>
      <host>
         <ip>10.112.89.82</ip>
         <username>root</username>
         <password>VMware123!</password>
         <auth_record_title>nsx</auth_record_title>
         <scan_template>797901</scan_template>
         <report_template>991466</report_template>
      </host>
      <host>
         <ip>10.112.89.83</ip>
         <username>root</username>
         <password>VMware123!</password>
         <auth_record_title>nsx</auth_record_title>
         <scan_template>797901</scan_template>
         <report_template>991466</report_template>
      </host>
   </host_details>
</data>
```
**Dependency**
* python 3 or above.
* [Requests]  (http://docs.python-requests.org/en/master/)
* [defusedxml]  (https://pypi.python.org/pypi/defusedxml)
```
pip install requests defusedxml
```
**Project Structure**
```
Vulscapi
|-vulscapi.py -- The wrapper that calls all other files. Run this to execute tasks
|-nes.py -- Nessus tasks
|-nex.py -- Nexpose tasks
|-qua.py -- Qualys tasks
|-util.py -- Miscellaneous utility
|-access_request.xml -- Access request with user details and Asset details
|-scanner_details.xml -- All the scanner URL and unames
|-host_details.xml -- Host details for a scan
```
**About Qualys scan (Expected behaviour)**

* Non admin account user will not be able to add IPs or Authentication record
* Default template used for scans is **Authenticated Scan v.2 - (6)**. You can change this default template in host_details.xml file
* Default template used for generating report is **Full Scan Technical Report**. You can change this default template in host_details.xml file
* The code will check the status of the scan every five minutes. No activity will be seen on the screen during this time.
* The report will be downloaded in the directory where the python script is placed.
* Please note: Do not exit the python program before report gets downloaded.

**Run Vulscapi**

Make user you have relevent xml flies(**_scanner_details.xml_**, **_access_request.xml_**, **_host_details.xml_**) in your current directory, these files are from which vulscapi get the scanner details and user access info(if required)
```
python vulscapi.py {action}
```
Where action is either **adduser** or **scan** as per current implementation

**Adding a new task**

Add a new positional parameter like *adduser* in **_vulscapi.py_** file and add appropriate implementations, so that those can be invoked when vulscapi is run along with new parameter. e.g python vulscapi newpara

**Contributing to this repo**
To fix a bug or enhance an existing module or add new feature, follow these steps:

* Fork the repo
* Create a new branch (`git checkout -b new_task`)
* Make the appropriate changes in the required file or add new file
* Commit your changes (`git commit -am 'new_task details'`)
* Push to the branch (`git push origin new_task`)
* Create a Pull Request 

**Bug / Feature Request**

If you find a bug , kindly open an issue [here](https://github.com/nikhilgeo/vulscapi/issues/new) by including error/exception message, the expected result, steps to reproduce.

If you'd like to request a new functionality, feel free to do so by opening an issue [here](https://github.com/nikhilgeo/vulscapi/issues/new) with description of the functionality.

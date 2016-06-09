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
**Dependency**
* python 3 or above.
* [Requests]  (http://docs.python-requests.org/en/master/)
* [defusedxml] (https://pypi.python.org/pypi/defusedxml)
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
|_scanner_details.xml -- All the scanner URL and unames
```

**Run Vulscapi**

Make user you have relevent xml flies(**_scanner_details.xml_**, **_access_request.xml_** ) in your current directory, these files are from which vulscapi get the scanner details and user access info(if required)
```
python vulscapi.py action {adduser}
```
Currently implemented action is adduser.

**Adding a new scanner task**

Add a new positional parameter like *adduser* in **_vulscapi.py_** file and add appropriate implementations, so that those can be invoked when vulscapi is run along with new parameter. e.g python vulscapi newpara

**Contributing to this repo**
To fix a bug or enhance an existing module or add new feature, follow these steps:

1. Fork the repo
2. Create a new branch (`git checkout -b new_task`)
3. Make the appropriate changes in the required file or add new file
4. Commit your changes (`git commit -am 'new_task details'`)
5. Push to the branch (`git push origin new_task`)
6. Create a Pull Request 

**Bug / Feature Request**

If you find a bug , kindly open an issue [here](https://github.com/nikhilgeo/vulscapi/issues/new) by including error/exception message, the expected result, steps to reproduce.

If you'd like to request a new functionality, feel free to do so by opening an issue [here](https://github.com/nikhilgeo/vulscapi/issues/new) with description of the functionality.

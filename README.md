# vulscapi
Python scripts for Nessus, Nexpose &amp; Qualys API's. Below listed are the implements API calls.

Nessus:
* Add User

Nexpose:
* Add Site
* Add User

Qualys:
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
Dependency
```
pip install requests defusedxml
```

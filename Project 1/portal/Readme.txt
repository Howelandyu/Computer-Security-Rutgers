
I used python3 to write the code
1. I used relative command to compile and run my code at linux. 
AddUser:  python3 portal.py AddUser username password
Authenticate: python3 portal.py Authenticate username password
SetDomain: python3 portal.py SetDomain username domain_name
DomainInfo: python3 portal.py DomainInfo domain_name
SetType: python3 portal.py SetType objectname type_name
TypeInfo: python3 portal.py TypeInfo type_name
AddAccess: python3 portal.py AddAccess operation domain_name typename
CanAccess: python3 portal.py CanAccess operation username objectname

2.For save the each data, I used os.path and pickle for helping. And I save all of data into data.txt. The structure is dictionary of dictionary. When user excute my code first time, and execute python3 portal.py AddUser. It will create data.txt and storing username and password inside. 

3.  I got results for several case:
For AddUser: Success, Error: user missing or Error: username exist

For Authenticate: Success, Error: no such user or Error: bad password, and argparse error

SetDomain: Success, and arparse error with username or domain_name are empty

DomainInfo: list username when success, or nothing when domain not exist and the domain not user. And arparse error when domain_name is empty

SetType: Success or argparse error

TypeInfo: list od objectname, nothing when typename not exist or not objectname in this type, Error: missing type when type is missing

AddAccess: Success, arparse error when operation, domain_name or/and typename are missing 

CanAccess: Success, arparse error when operation, username or/and typname are missing, error:access denied when they are not appropriate.

The example of arparse error: 
usage: portal.py [-h] operation objectname typename/username/domain_name...
portal.py: error: the following arguments are required: typename/username/domain_name...

However, there is a problem, the arparse error only can show the last of argv. 
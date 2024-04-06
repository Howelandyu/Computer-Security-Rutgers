import argparse
import os.path
from sys import *
import pickle

FILE_NAME = 'data.txt'


def initialize_data():
    return {
        'user' : {},
        'domains' : {},
        'types' : {},
        'access_permission' : {},
        'user_domain': {},
        'object_type': {},
    }


def LoadData():
    if os.path.isfile(FILE_NAME):
        file = open(FILE_NAME, 'rb')
        all_data = pickle.load(file)
    else:
        all_data = initialize_data()
    return all_data


def SaveData(all_data):
    file = open(FILE_NAME, 'wb')
    pickle.dump(all_data, file)
    file.close()


def AddUser(user_name:str,password:str):
    if user_name.strip() == "":
        print("Error:username missing")
        return
    data = LoadData()
    if user_name in data['user'].keys():
        print("Error:user exists")
    else:
        data['user'][user_name] = password
        SaveData(data)
        print("Success")
    return


def Authenticate(user_name:str,password:str):
    data = LoadData()
    if user_name not in data['user']:
        print("Error: no such user")
        return
    elif data['user'][user_name] != password:
        print("Error: bad password")
        return
    SaveData(data)
    print("Success")
    return


def SetDomain(user_name,domain_name):
    if domain_name=="":
        print("Error: missing domain")
    else:
        data = LoadData()
        if user_name not in data['user'].keys():
            print("Error: no such user")
        else:
            if domain_name not in data['domains'].keys():
                data['domains'][domain_name] = [user_name]
            else:
                data['domains'][domain_name].append(user_name)
            # data['user_domain'][user_name] = domain_name
            SaveData(data)
            print("Success")


def DomainInfo(domain_name):
    if domain_name != "":
        data = LoadData()
        if domain_name in data['domains']:
            for user_in_domain in data['domains'][domain_name]:
                print(user_in_domain)
        else:
            print("Error: domain does not exist")
    else:
        print("Error: missing domain")


def SetType(objectname,typename):
    if objectname!="" and typename!="":
        data = LoadData()
        if typename not in data['types'].keys():
            data['types'][typename] = [objectname]
        else:
            data['types'][typename].append(objectname)
        # data['object_type'][objectname] = typename
        SaveData(data)
        print('Success')
    else:
        print("Error")


def TypeInfo(typename):
     if typename != "":
        data = LoadData()
        # print(data['types'])
        if typename in data['types'].keys():
            for object_name in data['types'][typename]:
                print(object_name)
     else:
         print("Error")


def AddAccess(operation, domainame, typename):
    """
        Allow users under domainname to operate objects under typename

        print("Error: missing operation")
        print("Error: missing domain")
        print("Error: missing type")
    """
    data = LoadData()
    entry = (domainame, typename)
    if operation not in data['access_permission'].keys():
        data['access_permission'][operation] = []

    if entry not in data['access_permission'][operation]:
        data['access_permission'][operation].append(entry)
        SaveData(data)
        print("Success")
    else:
        print('Error, already existed')


def CanAccess(operation, username, object):
    data = LoadData()
    # print(data)
    if operation in data['access_permission'].keys():
        # find domain of the username
        # domain_of_user = data['user_domain'][username]
        domain_of_user = ''
        for domain, user_list in data['domains'].items():
            if username in user_list:
                domain_of_user = domain
        # find type of the object
        # type_of_object = data['object_type'][object]
        type_of_object = ''
        for type, obj_list in data['types'].items():
            if object in obj_list:
                type_of_object = type
        if (domain_of_user, type_of_object) in data['access_permission'][operation]:
            print("Success")
        else:
            print("Error:access denied")
    else:
        print("Error:access denied")


def start_check():
    parser = argparse.ArgumentParser()
    parser.add_argument("operation")

    if(argv[0] != "portal.py"):
        print("Error")
    else:
        if (argv[1] == "AddUser"):
            if len(argv) < 3:
                print('Error: username missing')
            parser.add_argument("username", help="Please specify a username")
            parser.add_argument("password", help="Please specify a password")
            args = parser.parse_args()
            AddUser(args.username, args.password)
            """
            if len(argv) < 4:
                AddUser('', '')
            else:
                AddUser(argv[2], argv[3])
            """
        elif(argv[1]=="Authenticate"):
            if len(argv) < 4:
                if len(argv) == 3:
                    Authenticate(argv[2], '')
                else:
                    Authenticate('', '')
            else:
                Authenticate(argv[2], argv[3])
            parser.add_argument("username", help="Please specify a username")
            parser.add_argument("password", help="Please specify a password")
            args = parser.parse_args()
            Authenticate(args.username, args.password)
        elif(argv[1]=="SetDomain"):
            if len(argv) < 3:
                print('Error: missing domain')
            parser.add_argument("username", help="Please specify a username")
            parser.add_argument("domainame", help="Please specify a domainame")
            args = parser.parse_args()
            SetDomain(args.username, args.domainame)
        elif(argv[1]=="DomainInfo"):
            if len(argv) < 2:
                print('Error: missing domain')
            parser.add_argument("domainame", help="Please specify a domainame")
            args = parser.parse_args()
            DomainInfo(args.domainame)
        elif(argv[1]=="SetType"):
            # if len(argv) < 4:
            #     if len(argv) == 3:
            #         SetType(argv[2], '')
            #         print('Error: missing object')
            #
            #         SetType('',argv[3])
            #         print('Error: missing type')
            #     else:
            #         SetType('', '')
            #         print('Error: missing object')
            #         print('Error: missing type')
            # else:
            #     SetType(argv[2], argv[3])
            parser.add_argument("objectname", help="Please specify a objectname")
            parser.add_argument("typename", help="Please specify a typename")
            args = parser.parse_args()
            SetType(args.objectname,args.typename)
        elif (argv[1] == "TypeInfo"):
            if len(argv) < 3:
                print('Error: missing type')
            parser.add_argument("typename", help="Please specify a typename")
            args = parser.parse_args()
            TypeInfo(args.typename)
        elif (argv[1] == "AddAccess"):
            # if len(argv) < 5:
            #     if len(argv)<4:
            #         if len(argv)==3:
            #             AddAccess(argv[2],'','')
            #             print('Error: missing operation')
            #     elif len(argv)==4:
            #         AddAccess(argv[2],argv[3], '')
            #         print('Error: missing type')

            parser.add_argument("operation", help="Please specify a operation")
            parser.add_argument("domainame", help="Please specify a domainame")
            parser.add_argument("typename", help="Please specify a typename")
            args = parser.parse_args()
            AddAccess(args.operation,args.domainame,args.typename)
        elif (argv[1] == "CanAccess"):
            # if len(argv) < 5:
            #     if len(argv)<4:
            #         if len(argv[2])==0 and len(argv[3])==0:
            #             print('Error: missing operation')
            #             print('Error: missing username')
            #         elif len(argv[2])==0 and len(argv[4])==0:
            #             print('Error: missing operation')
            #             print('Error: missing objectname')
            #         elif len(argv[3])==0 and len(argv[4])==0:
            #             print('Error: missing username')
            #             print('Error: missing objectname')
            #     else:
            #         if len(argv[2])==0:
            #             print('Error: missing operation')
            #         elif len(argv[3])==0:
            #             print('Error: missing username')
            #         elif len(argv[4])==0:
            #             print('Error: missing objectname')
            parser.add_argument("operation", help="Please specify a operation")
            parser.add_argument("username", help="Please specify a domainame")
            parser.add_argument("objectname", help="Please specify a typename")
            args = parser.parse_args()
            CanAccess(args.operation,args.username,args.objectname)


if __name__ == "__main__":
    start_check()
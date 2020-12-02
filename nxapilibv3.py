#Script Name : nxapilibpv3.py
#Script Purpose or Overview : This python file contains basic nutanix api method to connect Nutanix Prism Element
#This file is developed by Taeho Choi(taeho.choi@nutanix.com) by referring below resources
#
#   disclaimer
#	This code is intended as a standalone example.  Subject to licensing restrictions defined on nutanix.dev, this can be downloaded, copied and/or modified in any way you see fit.
#	Please be aware that all public code samples provided by Nutanix are unofficial in nature, are provided as examples only, are unsupported and will need to be heavily scrutinized and potentially modified before they can be used in a production environment.  
#   All such code samples are provided on an as-is basis, and Nutanix expressly disclaims all warranties, express or implied.
#	All code samples are © Nutanix, Inc., and are provided as-is under the MIT license. (https://opensource.org/licenses/MIT)

import json,sys
import time
import requests
import base64
import urllib3
import ipaddress
import getpass
import os.path
from pathlib import Path
from urllib.parse import quote
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ========== DO NOT CHANGE ANYTHING UNDER THIS LINE =====
class my_api():
    def __init__(self,ip,username,password):

        # Cluster IP, username, password.
        self.ip_addr = ip
        self.username = username
        self.password = password

        # Base URL at which v3 REST services are hosted in Prism Central.
        base_urlpc = 'https://%s:9440/api/nutanix/v3/'
        self.base_urlpc = base_urlpc % self.ip_addr

        # Base Karbon URL at which v3 REST services are hosted in Prism Central.
        base_urlkb = 'https://%s:9440/karbon/'
        self.base_urlkb = base_urlkb % self.ip_addr

        # Base URL at which v1 REST services are hosted in Prism Central.
        base_urlv1 = 'https://%s:9440/PrismGateway/services/rest/v1/'
        self.base_urlv1 = base_urlv1 % self.ip_addr

        self.session = self.get_server_session(self.username, self.password)    

    def get_server_session(self, username, password):

        # Creating REST client session for server connection, after globally
        # setting authorization, content type, and character set.
        session = requests.Session()
        session.auth = (username, password)
        session.verify = False
        session.headers.update({'Content-Type': 'application/json; charset=utf-8'})
        return session

        # Get entity information.
    def get_single_ent_info(self,ent,uuid):
        if (ent == 'cluster'):
            cluster_url = self.base_urlpc + "clusters/"+uuid
        elif (ent == 'host'):
            cluster_url = self.base_urlpc + "hosts/"+uuid
        elif (ent == 'vm'):
            cluster_url = self.base_urlpc + "vms/"+uuid
        elif (ent == 'image'):
            cluster_url = self.base_urlpc + "images/"+uuid
        elif (ent == 'project'):
            cluster_url = self.base_urlpc + "projects/"+uuid
        elif (ent == 'subnet'):
            cluster_url = self.base_urlpc + "subnets/"+uuid
        elif (ent == 'directory_service'):
            cluster_url = self.base_urlpc + "directory_services/"+uuid
        elif (ent == 'role'):
            cluster_url = self.base_urlpc + "roles/"+uuid
        elif (ent == 'alert'):
            cluster_url = self.base_urlpc + "alerts/"+uuid
        elif (ent == 'user'):
            cluster_url = self.base_urlpc + "users/"+uuid
        else: 
            print("wrong entiry parsed")
        print(cluster_url)
        server_response = self.session.get(cluster_url)
        return server_response.status_code ,json.loads(server_response.text)

    # Post new ent.
    def post_new_ent(self,ent,body):
        if (ent == 'cluster'):
            cluster_url = self.base_urlpc + "clusters/list"
        elif (ent == "host"):
            cluster_url = self.base_urlpc + "hosts/list"       
        elif (ent == "vm"):
            cluster_url = self.base_urlpc + "vms/list"        
        elif (ent == 'image'):
            cluster_url = self.base_urlpc + "images/list"
        elif (ent == 'project'):
            cluster_url = self.base_urlpc + "projects/list"
        elif (ent == 'subnet'):
            cluster_url = self.base_urlpc + "subnets/list"
        elif (ent == 'directory_service'):
            cluster_url = self.base_urlpc + "directory_services/list"            
        elif (ent == 'role'):
            cluster_url = self.base_urlpc + "roles/list"       
        elif (ent == 'alert'):
            cluster_url = self.base_urlpc + "alerts/list"
        elif (ent == 'user'):
            cluster_url = self.base_urlpc + "users/list"
        elif (ent =='karbon_fla'):
            cluster_url = self.base_urlkb + "acs/k8s/cluster"
        elif (ent =='karbon_cal'):
            cluster_url = self.base_urlkb + "v1/k8s/clusters" 
        elif (ent =='eula'):
            cluster_url = self.base_urlv1 + "eulas/accept"  
        elif (ent =='pulse'):
            cluster_url = self.base_urlv1 + "pulse" 
        elif (ent =='pubkey'):
            cluster_url = self.base_urlv1 + "cluster/public_keys" 
        elif (ent =='ntp'):
            cluster_url = self.base_urlv1 + "cluster/ntp_servers/add_list"   
        elif (ent =='dns'):
            cluster_url = self.base_urlv1 + "cluster/name_servers/add_list"
        elif (ent == 'storage_auth') :
            cluster_url = self.base_urlkb + "v1-alpha.1/k8s/clusters/storage-auth"
        elif (ent == "passwd"):
            cluster_url = self.base_urlv1 + "users/change_password"         
        else:
            print("Wrong selection")
        print("API end point is {}".format(cluster_url))
        print("\n")
        if ent in ["pulse","storage_auth","passwd"]:
            server_response = self.session.put(cluster_url,data = json.dumps(body)) 
        else:
            server_response = self.session.post(cluster_url,data = json.dumps(body))       
        return server_response.status_code ,json.loads(server_response.text)
    
    def karbon_list(self):
        cluster_url = self.base_urlkb + "v1-beta.1/k8s/clusters"
        print("API end point is {}".format(cluster_url))
        print("\n")
        server_response = self.session.get(cluster_url)    
        return server_response.status_code ,json.loads(server_response.text)

    def del_single_ent(self,ent,cluster_name):
        if (ent == 'karbon'):
            cluster_url = self.base_urlkb + "v1/k8s/clusters/"+cluster_name    
        else:
            print("Wrong selection")
        print("API end point is {}".format(cluster_url))
        print("\n")
        server_response = self.session.delete(cluster_url)       
        return server_response.status_code ,json.loads(server_response.text)

    # print all ent list with pretty format    
    def print_all_ent(self,ent):       
        body = {"kind": ent,"length": 1000, "offset":0}         
        status,entlist = self.post_new_ent(ent,body)
        
        entName=[str(i["status"].get("name")) for i in entlist["entities"]]
        
        if len(entName) >= 1:
            maxfield = len(max(entName,key=len))
        else:
            maxfield = 0
        
        # Removing PC cluster info
        if ent == "cluster":
            entlist["entities"] = [i for i in entlist["entities"] if i["status"]["name"] != "Unnamed"]
        # Removing PC cluster node info
        elif ent == "host":
            entlist["entities"] = [i for i in entlist["entities"] if i["status"].get("name") is not None]
        # Sorting the list with entity name for better display
        entlist["entities"] = sorted(entlist["entities"], key=lambda a:str(a["status"].get("name")))
            
        for i,n in enumerate(entlist["entities"],1):
            try:
                cluster_uuid = str(n["status"]["cluster_reference"].get("uuid"))
            except KeyError:
                cluster_uuid = "NA"
            if ent == "alert":
                print("{}.{}_UUID:{}   Sev:{}   Last_updated_time:{}  TITLE:{} ".format(str(i),ent.upper(),n["metadata"]["uuid"],n["status"]["resources"]["severity"].ljust(8),n["status"]["resources"]["last_update_time"],n["status"]["resources"]["title"]))
            else:                 
                print( "{}.{}_NAME: {} {}_UUID: {}    Hosted_cluster_uuid: {}".format(str(i),ent.upper(),str(n["status"].get("name")).ljust(maxfield),ent,n["metadata"]["uuid"],cluster_uuid))
        if maxfield == 0:
            i = 0
        print("\nTotal {} number is {}".format(ent,i))
        # 3. Creating valid UUid list to validate user input
        UUid=[i["metadata"]["uuid"] for i in entlist["entities"]]
        return status,UUid

    def EntityPCMenu(self,clustername,ip,username):
        print('#'*80)
        print("Be aware you are in {} PC cluster({}) as {} user".format(clustername,ip,username))
        print("What kind of operation do you want?\n")
        print('#'*4 + " MENU " + '#'*4+'\n'  )
        print("Type 1: Cluster info")
        print("Type 2: Host info")
        print("Type 3: Vm info")
        print("Type 4: Image info")
        print("Type 5: Project info")
        print("Type 6: Network info")
        print("Type 7: Directory Service info")
        print("Type 8: Role info")
        print("Type 9: Alert info")
        print("Type 10: User info")
        print("Type 11: New cluster setup - EULA,Pulse,NTP etc")
        print("Type 12: Deploy Karbon Cluster(Not Working) - Flannel")
        print("Type 13: Deploy Karbon Cluster - Calico")
        print("Type 14: List Karbon Cluster ")
        print("Type 15: Delete Karbon Cluster ")
        print("Type 16: Change admin user password")
        #print("Type 16: Update Karbon docker volume plugin password ")
        print("Type q: Exit program \n")
        print('#'*80)
        seLection = input()
        return str(seLection)

    def GetUUid(self):
        uuid = input("\n\nEnter entity uuid(ex.vm,host,image...) to see the detail: \n")
        if uuid == "":
            print("You pressed enter")
            return str(1)
        else:
            print("You typed uuid: %s" %uuid)
            return uuid

    def NewPasswd(self,rawpass):
        home = str(Path.home())
        cluster_config = home+"/.nx/pcconfig"
        #Encoding passwd 
        benc_passwd                 =       base64.b64encode(rawpass.encode("utf-8"))
        #Convert byte format to string to send json
        newpass                     =       benc_passwd.decode("utf-8")
        #load config file from existing one
        with open(cluster_config,'r') as old_file:
            config = json.load(old_file)
        #update passwd
        config["password"] = newpass 
        #write passwd to config  
        with open(cluster_config,'w') as new_file:
            json.dump(config, new_file)
        return print("\n %s passwd has been updated !!\n" %config["cluster_name"])
 
# ========== DO NOT CHANGE ANYTHING ABOVE THIS LINE =====
    
def GetClusterDetail():
    #Get current user home directory
    home = str(Path.home())
    # .nx for configuration folder
    path = home+"/.nx"
    cluster_config = home+"/.nx/pcconfig"
        
    if os.path.exists(cluster_config) == False:
        print("\nNo cluster config file found, will create new config file now\n")
        try:
            os.mkdir(path)
        except OSError:
            print("%s directory creation failed if you have already ~/.nx directory ignore this error" %path)
        else:
            print("%s directory creation is suceeded" %path)

        config={}
        config["cluster_name"]      =       input("What is cluster name?: ")  
        while True:  
            config["ip"]            =       input("Prism Central  IP: ")
            try : 
                ipaddress.ip_address(config["ip"])
                break
            except ValueError:
                print ("it doens't look like right ip address format")

        config["username"]          =       input("Prism admin role username: ")
        raw_passwd                  =       getpass.getpass(prompt="Password for admin user?\n" , stream=None)
        #Encoding passwd 
        benc_passwd                 =       base64.b64encode(raw_passwd.encode("utf-8"))
        #Convert byte format to string to send json
        config["password"]          =       benc_passwd.decode("utf-8")
        with open(cluster_config,'w') as out_file:
            json.dump(config,out_file)
        print("\n %s config file has been created !!\n" %config["cluster_name"])
        return(config["cluster_name"],config["ip"],config["username"],raw_passwd)

    else :
        print("Reading your config...")
        with open(cluster_config) as in_file:
            config = json.load(in_file)
            ip = config["ip"]
            username = config["username"]
            enc_passwd = config["password"]
            password = base64.b64decode(enc_passwd).decode("utf-8")
            cluster_name = config["cluster_name"]
        print("Found {} cluster config file in {}\n".format(cluster_name,cluster_config))
        return (cluster_name,ip,username,password)
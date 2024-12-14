import subprocess
import threading
import zlib
from PIL import Image

def find_IP():
    string= subprocess.check_output(["ipconfig"]).decode()
    string= string.replace("\r","")
    lines= string.split("\n")
    ips= []
    networks= []
    submasks= []
    
    for l in lines:
        if l!="" and l[0]!=" " and len(networks)>len(ips):
            networks.pop(-1)
            in_zerotier=False
        if l!="" and l[0]!=" ":
            networks.append(l)
        if l[:15]=="   IPv4 Address":
            ips.append(l[39:])
        if l[:14]=="   Subnet Mask":
            submasks.append(l[39:])
    
    if len(networks)>len(ips):
        networks.pop(-1)
    
    if len(ips)!=len(networks):
        print("find ip error")

    netIDs= netID(ips,submasks)
        
    return (networks,ips,netIDs)

def ips_zip(ips):
    num= 0
    letters="0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    digit=1
    for ip in ips:
        splited= ip.split(".")
        print(splited)
        for n in splited:
            num+=int(n)*digit
            digit*=256
    print(num)
    ans=""
    while(num>0):
        ans+=letters[num%len(letters)]
        num= num//len(letters)
    return ans

def ips_unzip(string):
    letters="0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    num= 0
    digit=1
    for l in string:
        num+= letters.find(l)*digit
        digit*=len(letters)
    print(num)
    ans=[]
    while(num>0):
        ans.append([])
        for i in range(4):
            ans[-1].append(str(num%256))
            num= num//256

    for i in range(len(ans)):
        ans[i]= ".".join(ans[i])
    return ans

def ip_to_int_lst(ip):
    splited= ip.split(".")
    return (int(splited[0]),int(splited[1]),int(splited[2]),int(splited[3]))

def netID(ips,musks):
    """return list of the netIDs (in the same order as the ips). NOTE: usume that all the parameters entered corectly"""
    ans= []
    for i in range(len(ips)):
        ip_lst= ip_to_int_lst(ips[i])
        musk_lst= ip_to_int_lst(musks[i])
        netID= []
        for j in range(4):
            netID.append(ip_lst[j]&musk_lst[j])
            netID[-1]= str(netID[-1])
        ans.append(".".join(netID))
    return ans

ans= find_IP()

for i in range(len(ans[0])):
    print(ans[0][i],"*****",ans[1][i],"*****",ans[2][i])

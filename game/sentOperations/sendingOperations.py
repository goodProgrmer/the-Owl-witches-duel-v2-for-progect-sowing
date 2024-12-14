import socket
import global_var
from Crypto.Cipher import PKCS1_OAEP
import subprocess

def sendMesegTCP(sock,string): #can get veriable of tipe bytes or string in the veriable string
    """send TCP meseg to server acording to the basic protocol (appending length and length of the length and doing incription and digital signature)
    :param sock: the socket from which it need to be sent
    :param string: the meseg it need to send
    :type sock: socket.socket
    :type string: string or bytes"""
    try:
        string+= global_var.digital_signature
        print("send-",string)
        if type(string)!=bytes:
            string= string.encode()
        string= increption(string)
        length=str(len(string))
        lengthOfLength=str(len(length))
        lengthOfLength=(2-len(lengthOfLength))*"0"+lengthOfLength
        sock.send((lengthOfLength+length).encode()+string)
    except:
        global_var.last_Q_t=-10000

def unpucketMasegTCP(sock,check_q=True):
    """unpuck meseg that sended by TCP according to the basic protocol (appending length and length of the length, checking digital signuture (if it isn't correct, it will return "") and doing incription).
    can check first in global_var.unreaded_TCP_msg if it asked to do so.
    :param sock: the socket from which the meseg should arrive
    :param check_q: does it need to check in global_var.unreaded_TCP_msg before anpacking meseg from the socket
    :type sock: socket.socket
    :type check_q: bool
    :return: the string that arrived, if there was an error (like timeout), return ""
    :rtype: string """
    if check_q and not len(global_var.unreaded_TCP_msg)==0:
        ans= global_var.unreaded_TCP_msg.popleft()
        print("recv3-",ans)
        return ans
    try:
        lengthOfTheLength=int((recv_msg(sock,2)).decode())
        length= int((recv_msg(sock,lengthOfTheLength)).decode())
        msg= (recv_msg(sock,length))[:length]
        string= decreption(msg).decode()
        if string[-15:]!=global_var.digital_signature:
            return ""
        string= string[:-15]
        print("recv1-",string)
        if string=="?":
            print(string)
            sendMesegTCP(sock,"!")
            global_var.last_Q_t= global_var.t
            ans= unpucketMasegTCP(sock)
            print(ans)
            print("recv2-",ans)
            return ans
        
        return string
    except Exception as exc:
        #print("except:",exc)
        return ""

def recv_msg(sock,length):
    """reciveing TCP meseg that exactly in the length that asked. NOTE: it doesn't considerate the protocol or incription
    :param sock: the socket from which the meseg should arrive
    :param length: the length
    :type sock: socket.socket
    :type length: int
    :return: the meseg
    :rtype: bytes"""
    msg=b""
    while len(msg)<length:
        msg_append= sock.recv(length-len(msg))
        msg +=msg_append
        if msg_append==b"":
            raise Exception("socket is closed")

    if len(msg)>length:
        raise Exception("taked to mach")
    return msg

def increption(byts):
    """incript the byts using RSA increaption so only the server will be able to read it. it seperate the bytes into gropps of maximam 50 bytes in there order,
    for eatch groop doing increaption and then append them one to enother in the same order.
    :param byts: the bytes to incript
    :type byts: bytes
    :return: increapted bytes
    :rtype: bytes"""
    cipher = PKCS1_OAEP.new(key=global_var.server_key)
    ans="".encode()
    while len(byts)>0:
        ans+= cipher.encrypt(byts[:50])
        byts= byts[50:]
    return ans

def decreption(byts):
    """decript the byts (that was incripted by increption function with client public key) using RSA decription.
    it seperate the bytes into gropps of 128 (the size of RSA incription) bytes in there order,
    for eatch groop doing increaption and then append them one to enother in the same order.
    :param byts: the bytes to decript
    :type byts: bytes
    :return: decreapted bytes
    :rtype: bytes"""
    cipher = PKCS1_OAEP.new(key=global_var.private_key)
    ans="".encode()
    while len(byts)>0:
        ans+= cipher.decrypt(byts[:128])
        byts= byts[128:]
    return ans

#for init_data_send
def init_data_send(sock):
    """send it's public key to the server"""
    network_data= find_IP()
    sendMesegTCP(sock,"DATA|"+str(network_data[1])+"|"+str(network_data[2])+"|"+global_var.public_key.export_key().decode())

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
        
    return (networks,netIDs,ips)

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
        

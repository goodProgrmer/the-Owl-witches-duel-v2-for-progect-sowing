import socket
import os
import cv2
import shutil
from Crypto.Cipher import PKCS1_OAEP
import global_var

def sendMesegUDP(sock,string,addres,key):#key value isn't relevant enymore
    """send UDP meseg acording to the basic protocol (appending length and length of the length)
    :param sock: the socket from which it need to be sent
    :param string: the meseg it need to send
    :param addres: to which addres it need to send it
    :param key: the public key of the address
    :type sock: socket.socket
    :type string: string
    :type address: string (IP addres)
    :type key: RSA key"""
    #string= increption(string.encode(),key)
    if type(string)==str:
        string= string.encode()
    length=str(len(string))
    lengthOfLength=str(len(length))
    lengthOfLength=(2-len(lengthOfLength))*"0"+lengthOfLength
    sock.sendto((lengthOfLength+length).encode()+string,addres)

def sendMesegTCP(sock,string,key): #key value isn't relevant enymore
    """send TCP meseg acording to the basic protocol (appending length and length of the length)
    :param sock: the socket from which it need to be sent
    :param string: the meseg it need to send
    :param addres: to which addres it need to send it
    :param key: the public key of the address
    :type sock: socket.socket
    :type string: string or bytes
    :type address: string (IP addres)
    :type key: RSA key"""
    if type(string)!=bytes:
        string= string.encode()
    #string= increption(string, key)
    length=str(len(string))
    lengthOfLength=str(len(length))
    lengthOfLength=(5-len(lengthOfLength))*"0"+lengthOfLength
    #print("ll:",lengthOfLength)
    sock.send((lengthOfLength+length).encode()+string)
    print("game send:",string)

def unpucketMasegUDP(sock,decode=True):
    """unpuck meseg that sended by UDP according to the basic protocol (appending length and length of the length and doing incription)
    :param sock: the socket from which the meseg should arrive
    :type sock: socket.socket
    :return: the string that arrived, if there was an error (like timeout), return None
    :rtype: string or None"""
    string=None
    try:
        while True:
            MAX_MESEG_LENGTH=131072
            
            msg=((sock.recvfrom(MAX_MESEG_LENGTH))[0])
            #print("unpucketMasegUDP",1)
            #breakpoint()
            lengthOfTheLength=int(msg[:2].decode())
            msg=msg[2:]
            length= int(msg[:lengthOfTheLength].decode())
            msg=msg[lengthOfTheLength:]
            string= msg[:length]
            if decode:
                string= string.decode()
            
        
    except Exception as exc:
        if string=="":
            #print("except:",exc)
            pass
        return string

def unpucketMasegTCP(sock,decode=True):
    """unpuck meseg that sended by TCP according to the basic protocol (appending length and length of the length and doing incription)
    :param sock: the socket from which the meseg should arrive
    :param decode: does it supposed to return string or bytes
    :type sock: socket.socket
    :type decode: bool
    :return: the string (or bytes if it asked so) that arrived, if there was an error (like timeout), return None
    :rtype: string, bytes or None"""
    try:
        lengthOfTheLength=int(recv_msg(sock,5).decode())
        #print(lengthOfTheLength)
        length= int(recv_msg(sock,lengthOfTheLength).decode())
        #print(length)
        msg= recv_msg(sock,length)

        #print("unpucketMasegTCP 1,",type(msg),decode)
        if decode:
            msg= msg.decode()
        #print("unpucketMasegTCP 2,",type(msg),decode)
        
        #print("done")
        print("game recv:",msg)
        return msg
    except Exception as exc:
        if not exc.__str__!= "timed out":
            print("except:",exc,decode)
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
        msg+= sock.recv(length-len(msg))

    if len(msg)>length:
        raise Exception("taked to mach")
    return msg

def increption(byts,key):
    """incript the byts using RSA increaption. it seperate the bytes into gropps of maximam 50 bytes in there order,
    for eatch groop doing increaption and then append them one to enother in the same order.
    :param byts: the bytes to incript
    :param key: the public key of the adress
    :type byts: bytes
    :type key: RSA key
    :return: increapted bytes
    :rtype: bytes"""
    cipher = PKCS1_OAEP.new(key=key)
    ans="".encode()
    while len(byts)>0:
        ans+= cipher.encrypt(byts[:50])
        byts= byts[50:]
    return ans

def decreption(byts):
    """decript the byts (that was incripted by increption function with its public key) using RSA decription.
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

#usefull functions
def send_video(file,sock,key):
    """sending video.
    :param file: the path to the file to send. NOTE: the file need to be mp4 file and this paramter don't need to includ the ending .mp4
    :param sock: the socket from which it need to be sent
    :param key: the public key of the address
    :type file: string
    :type sock: socket.socket
    :type key: RSA key"""
    f= open(file+".mp4", "rb")
    msg= f.read()
    f.close()
    sendMesegTCP(sock,msg,key)
    
def videoToFram(file):
    """deviding video to frames. NOTE: it saves all the frames in new directory with the same name and directory as the file.
    :param file: the path to the file to divide. NOTE: the file need to be mp4 file and this paramter don't need to includ the ending .mp4
    :type file: string"""
    capture = cv2.VideoCapture(file+".mp4")

    os.mkdir(file)

    frNum=0
    cont=True

    while cont:
        cont, frame = capture.read()
        if cont:
            cv2.imwrite(file+"\\"+str(frNum)+".jpg", frame)
            frNum+=1

    capture.release()
    f=open(file+"\\frames num.txt","w")
    f.write(str(frNum))
    f.close()

def recv_video(directory,sock):
    """reciving video, saving it and dividing to frames. save the frames in the given directory.
    the video saved with the same directory and name as the directory parameter. if there is anything saved in the place where it trying to save its files, it delits it.
    :param directory: the place where it saves the frames
    :param sock: the socket from which the video should arrive
    :type directory: string
    :type sock: socket.socket"""
    print("recv_video")
    shutil.rmtree(directory, True)
    print("deleted")
    msg= unpucketMasegTCP(sock,False)
    print("recived")
    f= open(directory+".mp4", "wb")
    f.write(msg)
    f.close()
    print("saved")
    videoToFram(directory)
    print("divided to frames")

def temp_recv_video(pNum,character):
        shutil.rmtree("TheMainGame/images/montaz/p"+str(pNum), True)
        shutil.copytree("images/montaz/"+character, "TheMainGame/images/montaz/p"+str(pNum))
        shutil.copy("images/montaz/"+character+".mp4", "TheMainGame/images/montaz/p"+str(pNum)+".mp4")

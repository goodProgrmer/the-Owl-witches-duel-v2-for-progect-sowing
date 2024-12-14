import socket
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


def sending_data_init():
    """init all the needed veriables for this file"""
    global sending_sock_key
    global sending_sock_signature
    global private_key
    
    sending_sock_key={}
    sending_sock_signature= {}
    private_key= RSA.import_key(open('data/private_pem.pem', 'r').read())

def get_sending_sock_key():
    """used becouse other programs import this file by from ___ import*
    :return: the dictionery of the sock (as key) with it's public key (as value)"""
    return sending_sock_key

def get_sending_signature():
    """used becouse other programs import this file by from ___ import*
    :return: the dictionery of the sock (as key) with it's signature (as value)"""
    return sending_sock_signature

def sendMesegTCP(sock,string):
    """send TCP meseg to claint acording to the basic protocol (appending length and length of the length and doing incription)
    :param sock: the socket from which it need to be sent
    :param string: the meseg it need to send
    :type sock: socket.socket
    :type string: string or bytes"""
    string+= sending_sock_signature[sock]
    print("sent-",string)
    if type(string)!= bytes:
        string= string.encode()
    string= increption(string, sock)
    length=str(len(string))
    lengthOfLength=str(len(length))
    lengthOfLength=(2-len(lengthOfLength))*"0"+lengthOfLength
    sock.send((lengthOfLength+length).encode()+string)

def unpucketMasegTCP(sock):
    """unpuck meseg that sended by TCP according to the basic protocol (appending length and length of the length, checking digital signuture (if it isn't correct, it will return "") and doing incription).
    it also save user digital signature if he doesn't have one.
    :param sock: the socket from which the meseg should arrive
    :type sock: socket.socket
    :return: the string that arrived, if there was an error (like timeout), return ""
    :rtype: string """
    try:
        #breakpoint()
        lengthOfTheLength=int(((sock.recv(2))).decode())
        length= int(((sock.recv(lengthOfTheLength))).decode())
        msg= ((sock.recv(length)))[:length]
        string= decreption(msg).decode()
        if sock in sending_sock_signature:
            #sock is in sending_sock_signature dictionery
            if string[-15:]!=sending_sock_signature[sock]:
                return ""
        else:
            sending_sock_signature[sock]= string[-15:]
        string= string[:-15]
        return string
    except Exception as exc:
        print("except:",exc)
        return ""

def increption(byts,sock):
    """incript the byts using RSA increaption so only the right claint will be able to read it. it seperate the bytes into gropps of maximam 50 bytes in there order,
    for eatch groop doing increaption and then append them one to enother in the same order.
    :param byts: the bytes to incript
    :type byts: bytes
    :return: increapted bytes
    :rtype: bytes"""
    cipher = PKCS1_OAEP.new(key=sending_sock_key[sock])
    ans="".encode()
    while len(byts)>0:
        ans+= cipher.encrypt(byts[:50])
        byts= byts[50:]
    return ans

def decreption(byts):
    """decript the byts (that was incripted by increption function with server public key) using RSA decription.
    it seperate the bytes into gropps of 128 (the size of RSA incription) bytes in there order,
    for eatch groop doing increaption and then append them one to enother in the same order.
    :param byts: the bytes to decript
    :type byts: bytes
    :return: decreapted bytes
    :rtype: bytes"""
    cipher = PKCS1_OAEP.new(key=private_key)
    ans="".encode()
    while len(byts)>0:
        ans+= cipher.decrypt(byts[:128])
        byts= byts[128:]
    #print(ans)
    return ans

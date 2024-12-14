from protocols_answer.sendingOperations import*
import server
import global_server_op
import hashlib

user_pass={}

sock_address= {}
logged_username= {}

def OnConect(sock,IP):
    """activated when new socket connected to the server
    :param sock: the connected socket
    :param IP: the IP of the conected user
    :type sock: socket.socket
    :type IP: string"""
    global sock_address
    sock_address[sock]=IP

def TCP_meseg_handle(msg,sock):
    """handle an meseg that was sent to this part (without the prefix)
    :param msg: the sended meseg
    :param sock: the socket that sent the meseg
    :type msg: string
    :type sock: socket.socket"""
    splited= msg.split("|")
    try:
        print(splited[0])
        if splited[0]=="LOGIN":
            LogIn(sock,splited[1],splited[2])
        elif splited[0]=="SIGN IN":
            SignIn(sock,splited[1],splited[2])
        elif splited[0]=="LOGOUT":
            LogOut(sock)
    except:
        pass
    

def init():
    """initialize any parameter in this file"""
    global user_pass
    f= open("data/user-pass.txt","r")
    for line in f:
        line= line.split("|")
        if len(line)==2:
            user_pass[line[0]]= line[1][:-1]
    f.close()

def SignIn(sock,username,password):
    """called when the user asked to sign in.
    :param sock: the socket of the user
    :param username: the username with which the user try to sign in
    :param password: the password with which the user try to sign in
    :type sock: socket.socket
    :type username: string
    :type password: string
    """
    #add username ligithimi check
    print("sign",username,password)
    try:
        user_pass[username]
        taken(sock)
    except:
        if username_check(username,password) and password!="":
            user_pass[username]= hashing(password)
            f= open("data/user-pass.txt","a")
            f.write(username+"|"+hashing(password)+"\n")
            f.close()
            LogIn(sock,username,password)
        else:
            uncorrect(sock)
            print("anavileble username/password")

def hashing(string):
    """doing hashing to the given string
    :param string: the given string
    :type string: string"""
    m = hashlib.sha256()
    m.update(string.encode())
    return m.hexdigest()

def username_check(username,password):
    """check does username follow the folowing standards (essential to server proper work):
    1. the username isn't int
    2. the username hasn't the char | in it
    3. the username hasn't the char \n in it
    :param username: the given username
    :type username: string
    :return: as mentioned above
    :rtype: bool"""

    """try:
        int(username)
        return False
    except:
        pass
    if len(password)<8 or not contain_num(password):
        return False"""

    return (not "|" in username) and (not "\n" in username) and from_chrs(username,"QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890")

def from_chrs(str1,str2):
    """check that any char in str1 is part of str2"""
    for s in str1:
        if not s in str2:
            return False
    return True

def contain_num(string):
    for i in range(10):
        if str(i) in string:
            return True
    return False

def is_loged(username):
    """check does the given username alredy loged in
    :param username: the given username
    :type username: string"""
    try:
        logged_username[username]
        return True
    except:
        pass
    return False

def LogIn(sock,username,password):
    """activated when user try to login
    :param sock: the socket of the user
    :param username: user's username
    :param password: user's password
    :type sock: socket.socket
    :type username: string
    :type password: string"""
    global logged_sock_username
    print("p-100",username,password+".")
    password= hashing(password)
    try:
        if user_pass[username]==password:
            print(0)
            if is_loged(username):
                taken(sock)
                return
            print(0.5)
            sending_sock_key=get_sending_sock_key()
            signutures_dic= get_sending_signature()
            logged_username[username]= True
            try:
                key= sending_sock_key[sock]
                signuture= signutures_dic[sock]
            except:
                key=None
                signuture= None
            settings= Settings_string(username)
            done(sock,settings)
            print(1)
            global_server_op.GExit(sock)
            print(2)
            global_server_op.OnConect(username,sock,sock_address[sock])
            print(key)
            sending_sock_key[sock]=key
            signutures_dic[sock]= signuture
            print(3)
        else:
            print(1,password,user_pass[username],user_pass[username]==password)
            uncorrect(sock)
    except Exception as e:
        print(e)
        print(4)
        uncorrect(sock)

def Settings_string(user):
    """return user's settings
    :param user: user's username
    :type user: string
    :return: user's settings
    :rtype: string"""
    try:
        f= open("users_cloud/settings-"+user,"r")
        settings= f.read()
        f.close()
    except:
        settings="[[[97, 100, 119, 115, 105, 111, 106, 107, 108]], [[97, 100, 119, 115, 122, 120, 99, 118, 98], [1073741904, 1073741903, 1073741906, 1073741905, 105, 111, 106, 107, 108]], 0.2, 0.7, True, False]"
    return settings

def LogOut(sock):
    """called when user try to logout
    :param sock: the socket of the user that want logout
    :type sock: socket.socket"""
    global logged_sock_username
    global_server_op.GExit(sock)
    username= global_server_op.choose_unloged_username()
    global_server_op.OnConect(username,sock,sock_address[sock])

def GExit(sock):
    """activated when the socket exit the game
    :param sock: the socket that exited the game
    :type sock: socket.socket"""
    logged_username.pop(global_server_op.sock_username[sock])

#send opperations
def done(sock,settings):
    """send DONE mesge according to the protocol
    :param sock: to which socket it need send the meseg
    :param settings: the settings of the user
    :type sock: socket.socket
    :type settings: string"""
    sendMesegTCP(sock,"DONE|"+settings)

def uncorrect(sock):
    """send UNCORRECT CERTIFICATES mesge according to the protocol
    :param sock: to which socket it need send the meseg
    :type sock: socket.socket"""
    sendMesegTCP(sock,"UNCORRECT CERTIFICATES")

def taken(sock):
    """send TAKEN USERNAME mesge according to the protocol
    :param sock: to which socket it need send the meseg
    :type sock: socket.socket"""
    sendMesegTCP(sock,"TAKEN USERNAME")

from protocols_answer.sendingOperations import*
#recv
def TCP_meseg_handle(msg,username,SOCK):
    """handle an meseg that was sent to this part (without the prefix)
    :param msg: the sended meseg
    :param username: the username of the one who sent the meseg
    :param SOCK: the socket of the user
    :type msg: string
    :type username: string
    :type SOCK: socket.socket"""
    #NOTE: in diffrence of other TCP_meseg_handle functions, this one check that the username is logined
    print("hendle",username)
    try:
        int(username)
        return
    except:
        pass
    splited= msg.split("|")
    try:
        if splited[0]=="SETTINGS SAVE" and len(splited)==2:
            Settings_save(SOCK,username,splited[1])
    except:
        pass

def Settings_save(SOCK,user,data):
    """save the setings that it recive from user
    :param SOCK: the socket of the user
    :param user: the username of the user
    :param data: the recived settings strings
    :type SOCK: socket.socket
    :type user: string
    :type data: string"""
    f= open("users_cloud/settings-"+user,"w")
    f.write(data)
    f.close()


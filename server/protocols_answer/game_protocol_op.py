from protocols_answer.sendingOperations import*
import global_server_op
import random

#the keys in the dictioneryies are the usernames of the users.
users_data={}
#data is list with length 5 when
#data[0]- user socket
#data[1]- user curent window (if the program don't know in wich window is the user, then it is None)
#data[2]- to wich users this user sent ask to play
#data[3]- wich players sent to the user ask to play
#data[4]- dictioneryin whitch: key- a network that this user has, value his IP in this network

gaming_meeting={} #this dictionery will be used to track when the server need to send "game start" 
#every sell is list with length 4
#data[0]- p1 username
#data[1]- p2 username
#data[2]- does p1 agree
#data[3]- does p2 agree

randGamewitingRoom=None
common_net= None #list of all the commons network betwin the users (if there are no users it will be None). the GExit function will update it only if no user left in the system (outherwise it will not be update).

#all recv metods will be with first big letter and the send with small one

#helpfull fanctions

def try_remove(lst,x):
    """remove element from the given list (if it in the list)
    :param lst: the given list
    :param x: the element to remove
    :type lst: list
    :type x: any thing"""
    try:
        lst.remove(x)
    except:
        pass

def isInDictionery(lst,diction):
    """check that any value in given list is in the given dictionery
    :param lst: the given list
    :param diction: the given dictionery
    :type lst: list
    :type diction: dictionery"""
    try:
        for x in lst:
            diction[x]
        return True
    except:
        return False

#recv
def OnConect(username,sock,IP):
    """activated when new socket connected to the server
    :param sock: the connected socket
    :param IP: the IP of the conected user
    :param username: the busername of the player
    :type sock: socket.socket
    :type IP: string
    :type username: string"""
    global users_data
    users_data[username]=[sock,None,[],[],IP]

def IpsSave(user,networks,ips):
    """this function update user_data and common_net according to the new user networks info and return True if succeed. otherwise return False (if after the operation there would be no common network)"""
    global users_data
    global common_net
    #updating user_data
    users_data[user][4]= {}
    for i in range(len(networks)):
        users_data[user][4][networks[i]]= ips[i]
        
    #updating common_net
    print("common_net:",common_net)
    if common_net==None:
        common_net= networks
        common_net_copy= None
    else:
        common_net_copy= common_net.copy()
        new_common_net= []
        for net in networks:
            if net in common_net:
                new_common_net.append(net)
        common_net= new_common_net
    print("common_net:",common_net)

    if common_net==[]:
        common_net= common_net_copy
        return False

    return True
    

def TCP_meseg_handle(msg,username):
    """handle an meseg that was sent to this part (without the prefix)
    :param msg: the sended meseg
    :param username: the username of the one who sent the meseg
    :type msg: string
    :type username: string"""
    print("hendle",username)
    splited= msg.split("|")
    try:
        if splited[0]=="ENTER":
            Enter(splited[1],username)
        elif splited[0]=="EXIT":
            Exit(username)
        elif splited[0]=="REFUSE":
            Refuse(username,splited[1])
        elif splited[0]=="ACSEPT":
            Accept(username,splited[1])
        elif splited[0]=="FRIEND GAME":
            Friend_game(username,splited[1])
        elif splited[0]=="CANCLE GAME":
            Cancle_game(username,splited[1])
        elif splited[0]=="P2 STATUES UPDATE":
            Statues_update(username,eval(splited[1]))
        elif splited[0]=="RANDGAME":
            Rand_game(username)
    except:
        pass

def Enter(window_Name,username):
    """called when user sent meseg about entering window
    :param window_Name: to which window the user entered
    :param username: the username of the user
    :type window_Name: string
    :type username: string"""
    global users_data
    
    known_windows=["game asks","char choose","continue choose"]

    if window_Name in known_windows:
        users_data[username][1]= window_Name

def Exit(username):
    """called when the user send meseg about exiting window
    :param username: the username of the user
    :type username: string"""
    global users_data
    global randGamewitingRoom
    
    data=users_data[username]
    for user in data[2]:
        cancle_game(username,user)

    for user in data[3]:
        try:
            refuse(username,user)
        except:
            pass

    data[1]= None
    data[2]=[]
    data[3]=[]
    if randGamewitingRoom==username:
        randGamewitingRoom=None

def Refuse(from_user,to):
    """called when user refuse to play with friend
    :param from_user: the sender username
    :param to: the address username
    :type from_user: string
    :type to: string"""
    global users_data
    
    if not isInDictionery([from_user,to],users_data):
        return
    
    refuse(from_user,to)
    try_remove(users_data[from_user][3],to)
    try_remove(users_data[to][2],from_user)

def Cancle_game(from_user,to):
    """called when user cancle game with friend that he propose
    :param from_user: the sender username
    :param to: the address username
    :type from_user: string
    :type to: string"""
    global users_data
    
    if not isInDictionery([from_user,to],users_data):
        return
    
    cancle_game(from_user,to)
    try_remove(users_data[from_user][3],to)
    try_remove(users_data[to][2],from_user)

def Accept(from_user,to):
    """called when user accept to play with friend
    :param from_user: the sender username
    :param to: the address username
    :type from_user: string
    :type to: string"""
    global users_data
    global gaming_meeting
    
    if not isInDictionery([from_user,to],users_data):
        return
    if not (to in users_data[from_user][3] and from_user in users_data[to][2]):
        return
    print("p-accept")
    accept(from_user,to)
    gaming_meeting[from_user]=[from_user,to,False,False]
    gaming_meeting[to]=gaming_meeting[from_user]
    print(gaming_meeting)

def Rand_game(from_user):
    """called when user send meseg that he want game with stranger
    :param from_user: sender username
    :type from_user: string"""
    global randGamewitingRoom
    global users_data
    print(randGamewitingRoom)
    try:
        users_data[randGamewitingRoom]
        New_game(from_user,randGamewitingRoom)
        randGamewitingRoom= None
    except Exception:
        randGamewitingRoom= from_user


def Friend_game(from_user,to):
    """called when user want propose friend game
    :param from_user: sender username
    :param to: address username
    :type from_user: string
    :type to: string"""
    global users_data
    
    if not isInDictionery([from_user,to],users_data):
        anncorect_wind(from_user)
        return
    
    if users_data[to][1]!="game asks":
        print(users_data[to][1])
        anncorect_wind(from_user)
        return
    friend_game(from_user,to)
    users_data[from_user][2].append(to)
    users_data[to][3].append(from_user)
    ask_sent(from_user,to)

def Statues_update(from_user,statues):
    """called when user send meseg about statues update (see server protocol).
    :param from_user: sender username
    :param statues: to 
    :type from_user: string
    :type to: string
    :type statues: boolean"""
    global users_data
    global gaming_meeting
    print("p-updating")
    #input tasting
    if not (isInDictionery([from_user],users_data) and isInDictionery([from_user],gaming_meeting)):
        print("p-1")
        return
    to= gaming_meeting[from_user][0]
    if to==from_user:
        to= gaming_meeting[from_user][1]

    if gaming_meeting[from_user]!=gaming_meeting[to] or users_data[from_user][1]!=users_data[to][1]:
        print("p-2", users_data[from_user][1], users_data[to][1])
        return
    #the function
    statues_update(to,statues)
    if not statues:
        try:
            gaming_meeting.pop(from_user)
        except:
            pass
        try:
            gaming_meeting.pop(to)
        except:
            pass
        return

    meeting_data=gaming_meeting[from_user]
    if meeting_data[0]==from_user:
        meeting_data[2]=True
    else:
        meeting_data[3]=True

    print("p-",meeting_data, users_data[from_user][1],users_data[to][1])

    if meeting_data[2] and meeting_data[3]:
        meeting_data[2]=False
        meeting_data[3]=False
        print(users_data[from_user][1])
        if users_data[from_user][1]=="char choose":
            New_game(from_user,to)

def New_game(p1,p2):
    """create new game and send any player the corect meseges. random wich of the players (p1 or p2) will be the server for this game.
    :param p1: username of player 1
    :param p2: username of player 2
    :type p1: string
    :type p2: string"""
    global users_data
    print("new game 1")
    if not isInDictionery([p1,p2],users_data):
        print("isn't in data:",users_data)
        return
    chosenPlayer=random.randint(1,2)
    print("new game 2")
    chosenPlayer=1
    if chosenPlayer==2:
        p1,p2=p2,p1

    global_server_op.online_matches+=1
    print("new game 3")
    gaming_meeting[p1]=[p1,p2,False,False]
    gaming_meeting[p2]=gaming_meeting[p1]
    print("new game 3",get_sending_sock_key()[users_data[p1][0]])
    game_start(p1,users_data[p2][4][common_net[0]],True,get_sending_sock_key()[users_data[p2][0]])
    game_start(p2,users_data[p1][4][common_net[0]],False,get_sending_sock_key()[users_data[p1][0]])

def GExit(username):
    """called when user exit the game
    :param username: the username of the user that want to exit the game
    :type username: string"""
    global users_data
    global gaming_meeting
    global common_net
    
    try:
        Statues_update(username,False)
        gaming_meeting.pop(username)
    except:
        pass
    Exit(username)
    users_data.pop(username)
    #updating common_net
    if not bool(users_data):
        common_net= None

#send
#the following fanctions send meseges according to the protocol
def friend_game(from_user,to):
    try:
        sendMesegTCP(users_data[to][0],"FRIEND GAME|"+from_user)
    except:
        pass

def refuse(from_user,to):
    try:
        sendMesegTCP(users_data[to][0],"REFUSE|"+from_user)
    except:
        pass

def accept(from_user,to):
    try:
        sendMesegTCP(users_data[to][0],"ACSEPT|"+from_user)
    except:
        pass

def cancle_game(from_user,to):
    try:
        sendMesegTCP(users_data[to][0],"CANCLE GAME|"+from_user)
    except:
        pass

def ask_sent(from_user,to):
    try:
        sendMesegTCP(users_data[from_user][0],"ASK SENT|"+to)
    except:
        pass

def game_start(to,p2,isServer,oponent_key):
    #oponent_key is in RSA object form
    
    try:
        sendMesegTCP(users_data[to][0],"GAME START|"+p2+"|"+str(isServer)+"|"+oponent_key.export_key().decode())
    except:
        pass

def statues_update(to,statues):
    try:
        sendMesegTCP(users_data[to][0],"P2 STATUES UPDATE|"+str(statues))
    except:
        pass

def anncorect_wind(to):
    try:
        sendMesegTCP(users_data[to][0],"ANCORRECT ADDRESS WINDOW")
    except:
        pass

import protocols_answer.game_protocol_op
import protocols_answer.login_protocol_op
import protocols_answer.cloud_protocol_op
import protocols_answer.sendingOperations as sockF
import socket
import select
from collections import deque
import time
import threading
import global_server_op
import GUI
from Crypto.PublicKey import RSA

def statistic_write():
    while True:
        print("statistic_write: writing")
        f= open("data/user-pass.txt","r")
        loge_num= f.read().count("\n")
        f.close()
        to_write=("loged usernames num:"+str(loge_num)+"\nusers in the game num:"+str(len(list(global_server_op.sock_username.keys())))+
                  "\nplayed online games:"+str(global_server_op.online_matches)+"\ncommon networks:"+str(protocols_answer.game_protocol_op.common_net))
        f= open("statistic.txt","w")
        f.write(to_write)
        f.close()
        for i in range(10):
            time.sleep(1)
            if global_server_op.done:
                print("statistic_write threading out")
                return

def get_init_data(sock,data):
    """save the key of the given socket and send confirmation meseg when done (if there is no saved key for this socket by this time).
    it gives to protocols_answer.game_protocol_op.IpsSave the networks data (if there is no saved pablic key for this socket (so this funtion never called before))
    :param sock: the given socket
    :param data: the masage
    :type sock: socket.socket
    :type called: string"""
    if not sock in sockF.sending_sock_key:
        splited= data.split("|")
        splited[0]= type_eval(splited[0])
        splited[1]= type_eval(splited[1])
        key= "|".join(splited[2:])
        sockF.sending_sock_key[sock]=RSA.import_key(key)
        succes_var= protocols_answer.game_protocol_op.IpsSave(global_server_op.sock_username[sock],splited[0],splited[1])
        if not succes_var:
            sockF.sendMesegTCP(sock,"NO COMMON NETWORK")
            global_server_op.GExit(sock)
        
        sockF.sendMesegTCP(sock,"CONNECTION SECURED")

def main():
    """running the server."""
    global_server_op.init()
    threading.Thread(target= statistic_write).start()
    threading.Thread(target= GUI.main).start()
    GUI.done= False
    print("server is up and running")

    while not global_server_op.done:
        reading,writing,errors= select.select(list(global_server_op.sock_username.keys())+[global_server_op.server_socket],[],list(global_server_op.sock_username.keys()),1)
        #print(global_server_op.done)
        for sock in errors:
            global_server_op.sock_username.pop(sock)
        
        for sock in reading:
            if sock==global_server_op.server_socket:
                (new_socket, address) = global_server_op.server_socket.accept()
                username= global_server_op.choose_unloged_username()
                global_server_op.OnConect(username,new_socket,address[0])
                print("username:",username)
                continue

            if not sock in global_server_op.sock_username.keys():
                continue

            msg= sockF.unpucketMasegTCP(sock)
            if msg=="":
                global_server_op.GExit(sock)
                continue
            if msg!="":
                print(msg,global_server_op.sock_username[sock])
            categoryInd= msg.find("|")
            if categoryInd==-1:
                if msg=="GEXIT":
                    global_server_op.GExit(sock)
                elif msg=="!":
                    global_server_op.sock_connect_msg[sock]=True
                continue
            print(msg[:categoryInd])
            if msg[:categoryInd]=="GAME":
                protocols_answer.game_protocol_op.TCP_meseg_handle(msg[categoryInd+1:],global_server_op.sock_username[sock])
            elif msg[:categoryInd]=="LOGIN":
                protocols_answer.login_protocol_op.TCP_meseg_handle(msg[categoryInd+1:],sock)
            elif msg[:categoryInd]=="CLOUD":
                protocols_answer.cloud_protocol_op.TCP_meseg_handle(msg[categoryInd + 1:], global_server_op.sock_username[sock], sock)
            elif msg[:categoryInd]=="DATA":
                get_init_data(sock,msg[categoryInd + 1:])
                
    #for sock in global_server_op.sock_username.keys():
    #    sock.close()
    global_server_op.server_socket.close()
    print("server out")

#string editing functions
def type_eval(string):
    """return the value of string (if it isn't in it's supported types it will raise exception) for example: type_eval('["aaa",10,10.0,(10,1)]')=["aaa",10,10.0,(10,1)]
    supported types: list,tuple,string,int,float,boolean"""
    return type_eval_recurtion(string.replace(" ",""))

def type_eval_recurtion(string):
    """return the value of string (if it isn't in it's supported types it will raise exception) for example: type_eval('["aaa",10,10.0,(10,1)]')=["aaa",10,10.0,(10,1)]
    supported types: list,tuple,string,int,float,boolean
    NOTE: assume that there is no space in the string"""
    if len(string)==0:
        raise Exception("type_eval: string can't be ''")
    elif (string[0]=="[" and string[-1]=="]") or (string[0]=="(" and string[-1]==")"):
        #list or tuple
        ans= split_no_bracket(string[1:-1])
        for i in range(len(ans)):
            ans[i]= type_eval_recurtion(ans[i])
            
        if string[0]=="(":
            ans= tuple(ans)
    elif len(string)>1 and ((string[0]=="'" and string[-1]=="'") or (string[0]=='"' and string[-1]=='"')):
        #string
        ans= string[1:-1]
    elif string in ["True","False"]:
        return string=="True"
    elif consist_of(string[1:],"1234567890.") and (string[0] in "1234567890-"):
        #float or int
        dot_num= string.count(".")
        if dot_num==0:
            ans= int(string)
        elif dot_num==1:
            ans= float(string)
        else:
            raise Exception("type_eval: consist of nums and dots but to much dots for tuple")
    elif string.count("e")==1:
        #it can be float from the from (a)e(b) for example 1.5e-10
        parts= string.split("e")
        try:
            parts= [type_eval_recurtion(parts[0]),type_eval_recurtion(parts[1])]
            if type(parts[1])!=int:
                raise Exception()
            ans= parts[0]*(10**parts[1])
        except:
            print("string:",string)
            raise Exception("type_eval: undefint type")
    else:
        print("string:",string)
        raise Exception("type_eval: undefint type")
    return ans
        

def consist_of(string1,string2):
    """check does string1 consist of characters in string2"""
    for c in string1:
        if not c in string2:
            return False
    return True

def split_no_bracket(string):
    """split the string according to "," when ignoryng the "," that in any type of brakets (including (),[],{})"""
    ans=[]
    slice_start=0
    open_brackets= "([{"
    close_brackets= ")]}"
    brackets_level= [0,0,0,0,0]
    #brackets_level[0]- () level
    #brackets_level[1]- [] level
    #brackets_level[2]- {} level
    #brackets_level[3]- "" level
    #brackets_level[4]- '' level
    for i in range(len(string)):
        if string[i]=="," and sum(brackets_level)==0:
            #print(i)
            ans.append(string[slice_start:i])
            slice_start= i+1
        elif open_brackets.find(string[i])!=-1:
            brackets_level[open_brackets.find(string[i])]+=1
        elif close_brackets.find(string[i])!=-1:
            brackets_level[close_brackets.find(string[i])]-=1
        elif "\"'".find(string[i])!=-1:
            brackets_level["\"'".find(string[i])+3]+=1
            brackets_level["\"'".find(string[i])+3]%=2
            

        if brackets_level[0]<0 or brackets_level[1]<0 or brackets_level[2]<0:
            raise Exception("split_no_bracket: to much closing brakets in: "+string)

    if sum(brackets_level)!=0:
            raise Exception("split_no_bracket: to much opening brakets in: "+string)

    ans.append(string[slice_start:])
    return ans


if __name__=="__main__":
    main()

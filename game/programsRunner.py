import TheMainGame.the_main_game_claint
import TheMainGame.the_main_game_server
import TheMainGame.montaz_show
import menu_before_playing.mane_menu
import menu_before_playing.intro
import menu_before_playing.game_menu
import menu_before_playing.playAgain
import menu_before_playing.about_us
import menu_before_playing.friendGame.friendGame
import menu_before_playing.char_choose.choose
import menu_before_playing.char_choose.waitingWindow
import menu_before_playing.connect
import menu_before_playing.login.singIn
import menu_before_playing.login.login
import global_var
import settings.onePlayer
import settings.twoPlayers
import settings.sound

from sentOperations.sendingOperations import*
from collections import deque
import pygame
import threading
import time

global_var.init()

def main():
    """run all the programs in the right order."""
    t= threading.Thread(target=connection_support)
    t.start() #running the functionof conection&conection check answering as thread
    firstRunFile="menu_before_playing.intro" #the window to run
    #firstRunFile="menu_before_playing.about_us" #the window to run
    
    global_var.nextRunFileName=firstRunFile #saving it in global_var

    #file runing
    nextRun=global_var.nextRunFileName #the window that it need to open now.
                                       #NOTE: I need it becouse I chenge global_var.nextRunFileName before I running the window.
    while nextRun!="":
        global_var.nextRunFileName="" #reset nextRunFileName in global_var file
        global_var.curecnt_window= nextRun #save the curent window (the one that it about to run) in global_var
        print(nextRun,"-->open")
        try:
            eval(nextRun).main() #running the nextRun window
        except global_var.internalException as e:
            print(e) #in case global_var.internalException will be used to stop the running of the window
        print(nextRun,"-->close")
        nextRun=global_var.nextRunFileName #the window that it need to open now.
        global_var.wind_chenge_t= 0 #so the glithers effect will work
        global_var.prew_window_screen= global_var.screen.copy() #so the glithers effect will work

    #closing of the game
    global_var.done=True
    global_var.quit() #quit global_var (it quit pygame too)
    t.join() #ending connection_support threading

def connection_support():
    """every period of timedo the next thing:
    if there is no conection to server- trying to reconect to the server
    if there is conection to server- handeling conection check meseges"""
    REPLAY_T= 15
    while not global_var.done:
        time.sleep(1)
        global_var.t+=1
        if global_var.is_connected:
            msg= unpucketMasegTCP(global_var.server_TCP_sock,False)
            if msg!="":
                global_var.unreaded_TCP_msg.append(msg)

            if global_var.t-global_var.last_Q_t > REPLAY_T*2:
                global_var.server_TCP_sock.close()
                global_var.is_connected= False
                global_var.username = None
                global_var.reload= True
                print("disconnected")
                #may "bug" to detect the bug on the server (in which the server disconnect the claint with no reason)
                """
                global_var.curecnt_window=""
                global_var.reload= True
                break"""
        else:
            for address in global_var.server_address:
                print(address)
                if global_var.done:
                    return
                #if i==1:
                #    print("connection try",address)
                #    global_var.server_TCP_sock.connect(address) #connect 1
                try:
                    global_var.server_TCP_sock = socket.socket()
                    global_var.server_TCP_sock.settimeout(5)
                    print("connection try",address)
                    global_var.server_TCP_sock.connect(address)
                    print("connected")
                    global_var.server_TCP_sock.settimeout(30) #max time to wait untile the approval that the public key arrived to the sever
                    print("connection- wait for approval")
                    init_data_send(global_var.server_TCP_sock)
                    msg= unpucketMasegTCP(global_var.server_TCP_sock)
                    if msg=="NO COMMON NETWORK":
                        global_var.alert_data= ("you dont have commone network with any computer in the server",(450,10,600,100))
                        global_var.server_address= []
                        global_var.reload= True
                        break
                    elif msg!="CONNECTION SECURED":
                        raise Exception()
                    global_var.server_TCP_sock.settimeout(0.01)
                    global_var.unreaded_TCP_msg= deque()
                    global_var.last_Q_t= global_var.t
                    global_var.reload= True
                    global_var.is_connected=True
                    print("connected")
                    break
                except Exception as e:
                    print("connection_support (programRunner) exception",e)
                    pass

if __name__=="__main__":
    main()

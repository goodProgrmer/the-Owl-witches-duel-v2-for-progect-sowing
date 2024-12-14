import socket
import pygame
from math import*
import time
from TheMainGame.characters.absCaracter import absCaracter
from TheMainGame.characters.hunter import hunter
from TheMainGame.characters.emity import emity
from TheMainGame.characters.luz import luz
from TheMainGame.characters.willow import willow
from TheMainGame.characters.gus import gus
import TheMainGame.for_commands_sending.drawIncreption as drawIncreption
import TheMainGame.for_commands_sending.drewDecription as drewDecription
from TheMainGame.for_commands_sending.sendingOperations import*
import TheMainGame.for_commands_sending.sounds as sounds
from TheMainGame.side_functions import*
import TheMainGame.datafiles.imeges
import global_var
import threading
import random
from Crypto.PublicKey import RSA
import zlib


def bg_music_support():
        """check does it need to play new background music. if it does, it choose one and put it on music to play."""
        if not global_var.pm.Channel(0).get_busy():
                clip= random.randint(1,3)
                print("clip:",clip)
                sounds.put('TheMainGame/sounds/bg_muzic/'+str(clip)+'.mp3', 0)
                #global_var.pm.Channel(0).play(pygame.mixer.Sound('TheMainGame/sounds/bg_muzic/'+str(clip)+'.mp3'))

def get_pressing():
        """get pressing on the buttons for bose players and uctivate the right operations in the character (use UDP socket if it online game)."""
        global claint_meseg
        pressed = pygame.key.get_pressed()
        
        if pressed[pButtons[0][0]]: characters[0].moveN()
        if pressed[pButtons[0][1]]: characters[0].moveP()
        if pressed[pButtons[0][2]]: characters[0].jump()
        if pressed[pButtons[0][3]]: characters[0].down()
        if pressed[pButtons[0][4]]: characters[0].comundNumConventFunc(1)
        if pressed[pButtons[0][5]]: characters[0].comundNumConventFunc(2)
        if pressed[pButtons[0][6]]: characters[0].comundNumConventFunc(3)
        if pressed[pButtons[0][7]]: characters[0].comundNumConventFunc(4)
        if pressed[pButtons[0][8]]: characters[0].comundNumConventFunc(5)

        if plaingOnline:
                recvStr=unpucketMasegUDP(server_socketUPD)
                if recvStr!=None:
                        claint_meseg=recvStr
                for c in claint_meseg:
                        if c=="A":
                                characters[1].moveN()
                        elif c=="D":
                                characters[1].moveP()
                        elif c=="W":
                                characters[1].jump()
                        elif c=="S":
                                characters[1].down()
                        elif c in ["1","2","3","4","5"]:
                                characters[1].comundNumConventFunc(int(c))
                        else:
                                print("character operations uncoding error in char:",c,"in the str:",claint_meseg)
                
        else:
                if pressed[pButtons[1][0]]: characters[1].moveN()
                if pressed[pButtons[1][1]]: characters[1].moveP()
                if pressed[pButtons[1][2]]: characters[1].jump()
                if pressed[pButtons[1][3]]: characters[1].down()
                if not global_var.is_traning:
                        if pressed[pButtons[1][4]]: characters[1].comundNumConventFunc(1)
                        if pressed[pButtons[1][5]]: characters[1].comundNumConventFunc(2)
                        if pressed[pButtons[1][6]]: characters[1].comundNumConventFunc(3)
                        if pressed[pButtons[1][7]]: characters[1].comundNumConventFunc(4)
                        if pressed[pButtons[1][8]]: characters[1].comundNumConventFunc(5)

def all_True(lst):
        """check are all the values in given lst True.
        :param lst: give lst
        :type lst: list of bool
        :return: are all the values in given lst True.
        :rtype: bool"""
        for x in lst:
                if not x:
                        return False
        return True

def loading(loading_end):
        global server_socketTCP
        global clientTCP_sock
        global cliantAdressUPD
        global server_socketUPD
        global key
        global charOne
        global charTwo
        global pButtons
        global screen
        global clock
        global claint_meseg
        global winerInfo
        global bg
        global space
        global countT
        global break_loop
        global agreed

        if plaingOnline:
                #crieting server and connect the client
                server_socketTCP = socket.socket()
                server_socketTCP.bind(("0.0.0.0", 8809))
                server_socketTCP.listen()
                (clientTCP_sock,cliantAdressTCP)=server_socketTCP.accept()
                cliantAdressUPD=(cliantAdressTCP[0],8800)
                
                server_socketUPD = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                server_socketUPD.bind(("0.0.0.0", 8810))
                server_socketUPD.settimeout(0.01)

                #getting the claint public key
                f=open("TheMainGame\\mainGameCommunicationInfo.txt","r")
                key= eval(f.read())
                f.close()

                key= RSA.import_key(key[1])
                
                print("Server is up and running")

        
        #get players characters
        print()
        global_var.pm.Channel(0).stop()
        
        charOne= global_var.data[0]
        
        if plaingOnline:
                charTwo=unpucketMasegTCP(clientTCP_sock)
        else:
                charTwo=global_var.data[1]

        #temp reciving montaz (will be updated in later version)
        temp_recv_video(1,charOne)
        temp_recv_video(2,charTwo)

        #geting player buttons (for those that on this computer)
        pButtons= global_var.buttons2P
        if plaingOnline:
                pButtons= global_var.buttons1P
        elif global_var.is_traning:
                pButtons=[global_var.buttons1P[0],global_var.buttons2P[1]]

        if not charTwo in ["hunter","emity","luz","willow","gus"]:
                print("charTwo <"+charTwo+"> isn't correct")
                global_var.nextRunFileName= "menu_before_playing.game_menu"
                return

        #initialing pygame and the winner file

        pygame.init()
        screen = global_var.screen
        clock = pygame.time.Clock()
        #clases

        TheMainGame.datafiles.imeges.init()

        f= open("TheMainGame/datafiles/winner.txt","w")
        f.write("")
        f.close()

        if plaingOnline:
                #montaz load
                print("sending info")
                #send_video("TheMainGame/images/montaz/p1",clientTCP_sock,key)
                print("recving info")
                #recv_video("TheMainGame/images/montaz/p2",clientTCP_sock)
                print("sending character")
                sendMesegTCP(clientTCP_sock,charOne,key)
                print("recving permision to start")
                #wait for game start time
                msg= unpucketMasegTCP(clientTCP_sock)
                while msg!="ok":
                        msg= unpucketMasegTCP(clientTCP_sock)
                print("maching start time")
                clientTCP_sock.settimeout(0.003)

        #initial veriables values (to prevent error with that)
        claint_meseg=""
        winerInfo=""
        global_var.data=""
        bg= pygame.image.load("TheMainGame/images/background/bg.png")
        bg= pygame.transform.scale(bg, (1500,790)).convert_alpha()
        space= pygame.image.load("TheMainGame/images/background/space.jpg")
        space= pygame.transform.scale(space, (1300,600)).convert()

        countT= 0
        break_loop=False

        TheMainGame.datafiles.imeges.imegesDict["V"]= pygame.transform.scale(pygame.image.load("images/system image/V.png"), (100,100))
        TheMainGame.datafiles.imeges.imegesDict["q"]= pygame.transform.scale(pygame.image.load("images/system image/q_mark.png"), (100,100))

        
        if plaingOnline:
                agreed=[False,False] #show does the players pushed space
        else:
                agreed=[False]

        #tutorial loading
        if not plaingOnline:
                tutorial_paint_init(pButtons,[charOne,charTwo])
        else:
                tutorial_paint_init(pButtons+[[]],[charOne,charTwo])

        #loading ending
        loading_end[0]= True
        print("done")

def main():
        """the code of this window. it's screen is in global_var.screen. NOTE: this window is also used for game on one conputer and traning game"""
        global frame_num
        global characters
        global pButtons
        global plaingOnline
        global server_socketUPD
        global clientTCP_sock
        global claint_meseg
        global break_loop
        #will store in global_var.data the text meseg to the player after game
        plaingOnline= global_var.plaingOnline
        print(global_var.plaingOnline)

        afterPlaying="TheMainGame.montaz_show"

        
        #loading
        loading_end= [False]
        t= threading.Thread(target=lambda: loading(loading_end))
        t.start()
        if loading_display(loading_end):
                t.join()
                return
        
        #start
        for i in range(2): #if i==0- this is key trening before the game. if i==1- it is the game
                done = False
                t=0
                characters= [eval(charOne+"(screen,1)"),eval(charTwo+"(screen,2)")]
                print(characters)

                characters[0].enemy=characters[1]
                characters[1].enemy=characters[0]
                if i==0:
                        for c in characters:
                                c.movinator.imeges_loud()
                while not done:
                        for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                        done = True
                                        break_loop=True
                                        if plaingOnline:
                                                sendMesegTCP(clientTCP_sock,"EXIT 1",key)
                        
                        pressed = pygame.key.get_pressed()
                        
                        drawIncreption.init()

                        get_pressing()

                        #checking TCP socket (dose client closed the game) or pushed space
                        if plaingOnline:
                                clintTCPmeseg= unpucketMasegTCP(clientTCP_sock)
                                if clintTCPmeseg=="EXIT 2":
                                        done= True
                                        break_loop=True
                                        global_var.nextRunFileName= afterPlaying
                                        global_var.data= "the second player quit the game"
                                if clintTCPmeseg=="SPACE":
                                        agreed[1]= True
                        
                        
                        for c in characters:
                            c.tick()
                        drawIncreption.compretion()
                        
                        for c in characters:
                            c.beforeSending()
                        drawIncreption.compretion()
                        #calckTime=time.time()*1000
                        if i==0:
                                for c in characters:
                                        c.hp=100
                                drawIncreption.blitIncription(drawIncreption.textDrawIncription("Ariel",80,"press space to start",(255,255,255)),(400,200))
                                if pressed[pygame.K_SPACE]: agreed[0]=True

                        f= open("TheMainGame/datafiles/winner.txt","r")
                        winerInfo=f.read()
                        f.close()
                        if winerInfo!="" and i==1:
                                print(winerInfo)
                                done = True
                                global_var.nextRunFileName= afterPlaying
                                msg= ("WIN|"+winerInfo+", characters' HP: "+type(characters[0]).__name__+", "+str(int(characters[0].hp))+
                                             " "+type(characters[1]).__name__+" "+str(int(characters[1].hp)))
                                global_var.data= msg[4:]
                                print(global_var.data)
                                if plaingOnline:
                                        sendMesegTCP(clientTCP_sock,msg,key)

                        #bg paint
                        screen.fill((100, 100, 100))
                        pygame.draw.rect(screen,(50,50,50), pygame.Rect(100,0,1300,600))
                        global_var.screen.blit(space,(100,0))
                        """if t>v_start_t:
                                try:
                                        TheMainGame.datafiles.imeges.imegesDict["TheMainGame/images/background/stars/"+str(t%frame_num)]
                                except:
                                        img= pygame.image.load("TheMainGame/images/background/stars/"+str(t%frame_num)+".jpg")
                                        img= pygame.transform.scale(img, (1300,600))
                                        TheMainGame.datafiles.imeges.imegesDict["TheMainGame/images/background/stars/"+str(t%frame_num)]= img.convert()

                                img= TheMainGame.datafiles.imeges.imegesDict["TheMainGame/images/background/stars/"+str(t%frame_num)]
                                global_var.screen.blit(img,(100,0))"""

                        #inserting space show (sow 2 players will be must to push the space button to start the game)
                        if i==0 and plaingOnline:
                                img= "q"
                                if agreed[0]:
                                    img= "V"
                                drawIncreption.blitIncription(img,(310,10))

                                img= "q"
                                if agreed[1]:
                                    img= "V"
                                drawIncreption.blitIncription(img,(1090,10))
                        
                        if plaingOnline:
                                sendMesegUDP(server_socketUPD,zlib.compress(drawIncreption.drawStrings[1].encode()),cliantAdressUPD,key)
                        drewDecription.decription(screen,drawIncreption.drawStrings[0])
                        #print(len(zlib.compress(drawIncreption.drawStrings[0].encode())))
                        #print(drawIncreption.drawStrings[0])
                        pygame.draw.rect(screen,(100,100,100), pygame.Rect(0,600,1500,600))
                        global_var.screen.blit(bg,(0,0))
                        if i==0:
                                if not plaingOnline:
                                        tutorial_paint([True,True])
                                else:
                                        tutorial_paint([True,False])
                        
                        #checking does it need to turn of the keys trening
                        if i==0 and all_True(agreed):
                                done=True
                        #drawTime=time.time()*1000
                        bg_music_support()
                        global_var.before_menu_screen_display()
                        if plaingOnline:
                                sounds.play(clientTCP_sock,key)
                        else:
                                sounds.play()
                        pygame.display.flip()
                        dt=clock.tick(30)
                        if t==countT and i==1:
                                if plaingOnline:
                                        sendMesegTCP(clientTCP_sock,"COUNT",key)
                                if count():
                                        done=True
                        t+=1
                if break_loop:
                        break
                        

                

        if plaingOnline:
                clientTCP_sock.close()
                server_socketTCP.close()
                server_socketUPD.close()
        global_var.pm.Channel(0).stop()

if __name__=="__main__":
        main()
else:
        print(__name__)

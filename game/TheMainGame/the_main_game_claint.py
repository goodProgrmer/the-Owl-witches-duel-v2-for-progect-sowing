import socket
import pygame
from math import*
from TheMainGame.characters.absCaracter import absCaracter
from TheMainGame.characters.hunter import hunter
from TheMainGame.characters.emity import emity
from TheMainGame.characters.luz import luz
from TheMainGame.characters.willow import willow
from TheMainGame.characters.gus import gus
import TheMainGame.for_commands_sending.drawIncreption as drawIncreption
import TheMainGame.for_commands_sending.drewDecription as drewDecription
from TheMainGame.for_commands_sending.sendingOperations import*
import TheMainGame.datafiles.imeges
from TheMainGame.side_functions import*
import time
import global_var
import shutil
import os
from Crypto.PublicKey import RSA
import threading
import zlib

def loading(loading_end):
        global SERVER_IP
        global key
        global UDPsock
        global server_addressUDP
        global TCPsock
        global afterPlaying
        global character
        global screen
        global done
        global t
        global clock
        global char1
        global characters
        global space_passed
        global drawStr
        global bg
        global space
        #getting server IP and key
        f=open("TheMainGame\\mainGameCommunicationInfo.txt","r")
        (SERVER_IP,key) = eval(f.read())
        f.close()
        key= RSA.import_key(key)

        #conecting to the server

        UDPsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        server_addressUDP = (SERVER_IP, 8810)
        UDPsock.bind(("0.0.0.0", 8800))
        UDPsock.settimeout(0.005)

        TCPsock = socket.socket()
        while True:
                try:
                        TCPsock.connect((SERVER_IP,8809))
                        break
                except Exception as exc:
                        print(exc)
                        time.sleep(3)
        
        print("conected to the server")
        #rename the playrs montaz to p2 montaz
        shutil.rmtree("TheMainGame/images/montaz/p2", True)
        os.rename("TheMainGame/images/montaz/p1","TheMainGame/images/montaz/p2")
        try:
                os.remove("TheMainGame/images/montaz/p2.mp4")
        except:
                pass
        os.rename("TheMainGame/images/montaz/p1.mp4","TheMainGame/images/montaz/p2.mp4")
        
        #other stuf
        afterPlaying="TheMainGame.montaz_show"
        character= global_var.data[0]
        sendMesegTCP(TCPsock,character,key)
        
        print("character sent")

        #prepering the window
        pygame.init()
        screen= global_var.screen
        done = False
        t=0
        clock = pygame.time.Clock()
        #getting the montaz from the server and sending its own montaz
        print("shering montaz")
        #send_video("TheMainGame/images/montaz/p2",TCPsock,key)
        print("recving montaz")
        #recv_video("TheMainGame/images/montaz/p1",TCPsock)
        print("other staf")
        #louding images
        print("wite to the second player, go to the game screen")
        TheMainGame.datafiles.imeges.init()
        char1=unpucketMasegTCP(TCPsock) #resiving enemy character
        
        if not char1 in ["hunter","emity","luz","willow","gus"]:
                print("charTwo <"+char1+"> isn't correct")
                global_var.nextRunFileName= "menu_before_playing.game_menu"
                return
        characters=[eval(char1+"(screen,1)"),eval(character+"(screen,2)")]
        for c in characters:
                try:
                        c.movinator.imeges_loud()
                except Exception as e:
                        print(e)
        
        #temp recving video (will be updated in later version)
        temp_recv_video(1,char1)
        temp_recv_video(2,character)
        #initial veriables values (to prevent errors with that)
        space_passed= False
        drawStr=""
        TCPsock.settimeout(0.005)
        bg= pygame.image.load("TheMainGame/images/background/bg.png")
        bg= pygame.transform.scale(bg, (1500,790)).convert_alpha()
        space= pygame.image.load("TheMainGame/images/background/space.jpg")
        space= pygame.transform.scale(space, (1300,600)).convert()

        TheMainGame.datafiles.imeges.imegesDict["V"]= pygame.transform.scale(pygame.image.load("images/system image/V.png"), (100,100))
        TheMainGame.datafiles.imeges.imegesDict["q"]= pygame.transform.scale(pygame.image.load("images/system image/q_mark.png"), (100,100))
        tutorial_paint_init([[]]+global_var.buttons1P,[char1,character])
        
        loading_end[0]= True
        print("done")

def main():
        global done
        global drawStr
        global t
        global space_passed
        """the code of this window. it's screen is in global_var.screen."""
        #loading
        loading_end= [False]
        thread= threading.Thread(target=lambda: loading(loading_end))
        thread.start()
        if loading_display(loading_end):
                thread.join()
                return

        print("redy to start")
        sendMesegTCP(TCPsock,"ok",key) #sent permision to start

        while not done:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                sendMesegTCP(TCPsock,"EXIT 2",key)
                                done = True
                                print("done")
                
                pressed = pygame.key.get_pressed()

                #geting keybord input
                commandStr=""

                if pressed[global_var.buttons1P[0][0]]: commandStr+="A"
                if pressed[global_var.buttons1P[0][1]]: commandStr+="D"
                if pressed[global_var.buttons1P[0][2]]: commandStr+="W"
                if pressed[global_var.buttons1P[0][3]]: commandStr+="S"
                if pressed[global_var.buttons1P[0][4]]: commandStr+="1"
                if pressed[global_var.buttons1P[0][5]]: commandStr+="2"
                if pressed[global_var.buttons1P[0][6]]: commandStr+="3"
                if pressed[global_var.buttons1P[0][7]]: commandStr+="4"
                if pressed[global_var.buttons1P[0][8]]: commandStr+="5"

                if pressed[pygame.K_SPACE] and not space_passed:
                        sendMesegTCP(TCPsock,"SPACE",key)
                        space_passed=True

                #UDP comunication
                sendMesegUDP(UDPsock,commandStr,server_addressUDP,key)
                recvStr=unpucketMasegUDP(UDPsock,False)
                if recvStr!=None:
                    drawStr=zlib.decompress(recvStr).decode()
                #TCP comunication
                TCP_meseg=unpucketMasegTCP(TCPsock)
                if TCP_meseg!="":
                        print(TCP_meseg)
                commund_end= TCP_meseg.find("|")
                command= ""
                if commund_end!=-1:
                        command= TCP_meseg[:commund_end]
                if command=="WIN":
                        print(TCP_meseg)
                        global_var.data= TCP_meseg[4:]
                        done = True
                        global_var.nextRunFileName= afterPlaying
                        break
                if command=="SOUND":
                        params= TCP_meseg[commund_end+1:].split("|")
                        params[1]= int(params[1])
                        global_var.pm.Channel(params[1]).play(pygame.mixer.Sound(params[0]))
                if TCP_meseg=="EXIT 1":
                        print(TCP_meseg)
                        done = True
                        global_var.nextRunFileName= afterPlaying
                        global_var.data= "the second player quit the game"
                        break
                if TCP_meseg=="COUNT":
                        if count():
                                done=True

                #screen drawing
                screen.fill((100, 100, 100))
                pygame.draw.rect(screen,(50,50,50), pygame.Rect(100,0,1300,600))
                global_var.screen.blit(space,(100,0))

                drewDecription.decription(screen,drawStr)
                #pygame.draw.rect(screen,(100,100,100), pygame.Rect(0,600,1500,600))
                global_var.screen.blit(bg,(0,0))
                if not space_passed:
                        tutorial_paint([False,True])
                global_var.before_menu_screen_display()
                pygame.display.flip()
                t+=1
                clock.tick(30)

        print("closing")
        #close sockets and music
        UDPsock.close()
        TCPsock.close()
        global_var.pm.Channel(0).stop()

if __name__=="__main__":
        main()
else:
        print(__name__)

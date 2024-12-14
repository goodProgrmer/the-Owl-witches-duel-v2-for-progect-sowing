import global_var
from TheMainGame.for_commands_sending.sendingOperations import*
import pygame

sounds= []
pygame.init()
#for every 0<=i<len(sounds):
#sounds[i][0]- the path to the sound that the program need to put
#sounds[i][1]- the number of the chanel that program need to put this sound in it

def put(path,chanel):
    """put the ask to play sound in the list, so in the end of this frame it will be played and the commund to play it will be send to the other player if nesesery
    :param path: the path to the sound file (including the .mp3 ending)
    :param chanel: the chanel in which it need to be played
    :type path: string
    :type chanel: int"""
    sounds.append([path, chanel])

def play(sock= None,key=None):#if sock is None, then the program will not send the sounds
    """play all the sounds in the sounds list as they asked. if sock!=None, it send to the second player commund to play this sound too (acording to the protocol).
    :param sock: the socket from which it need to send the commund. if it None, it will not send it.
    :param key: the public key of the address. if sock==None, it will not use this parameter (so its meaneng isn't importent)
    :type sock: socket.socket or None
    :type key: RSA key or None"""
    global sounds
    
    for i in range(len(sounds)):
        global_var.pm.Channel(sounds[i][1]).play(pygame.mixer.Sound(sounds[i][0]))
        
        if sock!= None:
            sendMesegTCP(sock,"SOUND|"+str(sounds[i][0])+"|"+str(sounds[i][1]),key)
    sounds=[]


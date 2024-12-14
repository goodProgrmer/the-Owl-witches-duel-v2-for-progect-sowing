import pygame
import sentOperations.sendingOperations as sockF
import socket
from collections import deque
from usefull_classes.elart import elart
import random
from Crypto.PublicKey import RSA
from usefull_classes.veriable_eval import type_eval
import time
import os

def init():
    """initializing every veriable in global var"""
    global server_TCP_sock
    global nextRunFileName
    global screen
    global data
    global buttons1P
    global buttons2P
    global plaingOnline
    global is_traning
    global is_known_competitor
    global is_connected_ask
    global done
    global unreaded_TCP_msg
    global username
    global server_address
    global is_connected
    global last_Q_t
    global t
    global reload
    global bg
    global wind_chenge_t
    global glitterT
    global glitter
    global prew_window_screen
    global display_rects
    global pm
    global T_buttons1P
    global T_buttons2P
    global T_sound_data
    global bg_music
    global shootes_sound
    global shootes_sound_volume
    global bg_music_volume
    global down_info_img
    global alert_data
    global fan_made_logo
    global past_frames_t
    global frames_to_evereg
    global ctrl_v
    global connecting_text
    global SERVER_PORT

    #checking that there is video saving place
    if os.path.exists("temp"):
        raise Exception("there is alredy derectory named temp")

    frames_to_evereg= 20
    past_frames_t= [0]*frames_to_evereg
    
    data=None #information pasing bitween windows (that not one of the folowing veriables)

    #to comunication with server
    SERVER_PORT = 8820
    server_address = []
    connecting_text= ""
    server_TCP_sock = socket.socket()
    is_connected= False
    last_Q_t= -100 #the last time when ? meseg was resived (in seconds since program run start). connection to the server count like ? meseg.
    t=0 #time in seconds since program run start
    keys_init()
    reload= False
    curecnt_window= ""

    #for is_connect_Q_answer function
    done= False
    unreaded_TCP_msg= deque() #? meseges will not be writen in it
    #NOTE: the unpucketMasegTCP will first take msg from unreaded_TCP_msg.
    #NOTE: if the unpucketMasegTCP function will see ? maseg, it will send ! and recol it self

    #for program runer
    nextRunFileName=""

    #sown screen
    pygame.init()
    screen = pygame.display.set_mode((1500, 800))
    bg= pygame.image.load("images/system image/bg.PNG")
    bg= pygame.transform.scale(bg, (1500,700))
    glitter= pygame.image.load("images/system image/glitter.PNG")
    glitter= pygame.transform.scale(glitter, (150,700))
    glitterT= 25
    wind_chenge_t=0 #store the time since last window change in frame (don't raise up if it more then glitterT)
    prew_window_screen= None
    down_info_img= pygame.transform.scale(pygame.image.load("images/system image/down info image.PNG"),(1500,100))
    fan_made_logo= pygame.image.load("images/system image/fan made.PNG")

    alert_data= None

    #copy past mechanic
    ctrl_v= pygame.scrap
    ctrl_v.init()
    #sounds
    pm= pygame.mixer
    pm.init()
    chennels_num=3
    pm.set_num_channels(chennels_num)
    #channel 0 for the bg music
    #channel 1 for the character of player 1
    #channel 2 for the character of player 2

    #settings upload
    f= open("settings/settings.txt","r")
    settings_str= f.read()
    f.close()
    from_str_to_settings(settings_str)
    sound_volume_correct()
    #for settings (beffore saveing) any one of the veriables here start with T_
    T_buttons1P= None
    T_buttons2P= None
    T_sound_data= None #[bg music volume, shootes sounds volume, display bg music?, display shootes sound?]
    #for character choose (so it will know from witch button the user came to it)
    plaingOnline=True #when the game ended or you enter game menu, it will return to be True
    is_traning=False
    is_known_competitor= False

    #for login and signin
    username=None

    #for mainGame
    display_rects=False

def keys_init():
    """init the keys of the user"""
    global private_key
    global public_key
    global server_key
    global digital_signature
    #Generating private key (RsaKey object) of key length of 1024 bits
    private_key = RSA.generate(1024)
    #Generating the public key (RsaKey object) from the private key
    public_key = private_key.publickey()
    server_key= RSA.import_key(open('server_public_key.pem', 'r').read())
    digital_signature= randStr(15)
    print(digital_signature)
    print(public_key.export_key().decode())

def randStr(length):
    ans=""
    for i in range(length):
        ans+=chr(random.randint(32,123))
    return ans

def quit():
    """quit the game"""
    if is_connected:
        sockF.sendMesegTCP(server_TCP_sock,"GEXIT")
        server_TCP_sock.close()
    pm.quit()
    pygame.quit()

def settings_save():
    """saving settings"""
    #after saving, replace all temp veriables to None
    global buttons1P
    global buttons2P
    global T_buttons1P
    global T_buttons2P
    buttons1P= T_buttons1P
    buttons2P= T_buttons2P

    T_buttons1P= None
    T_buttons2P= None
    print(buttons1P)

    f= open("settings/settings.txt","w")
    f.write(setting_toString())
    f.close()
    
    if username!=None:
        sockF.sendMesegTCP(server_TCP_sock,"CLOUD|SETTINGS SAVE|"+setting_toString())

def from_str_to_settings(string):
    """get settings string and chenge any related veriable according to it
    :param string: given settings string
    :type string: str"""
    global buttons1P
    global buttons2P
    global bg_music
    global shootes_sound
    global shootes_sound_volume
    global bg_music_volume

    buttons1P,buttons2P,bg_music_volume,shootes_sound_volume, bg_music, shootes_sound= type_eval(string)
    

def setting_toString():
    """use saved in global veriables settings to create settings string"""
    return str([buttons1P,buttons2P,bg_music_volume,shootes_sound_volume, bg_music, shootes_sound])

def sound_volume_correct():
    """correct the volume of mixer according to bg_music_volume, shootes_sound_volume, bg_music, shootes_sound"""
    
    chennels_num= pm.get_num_channels()
    if not bg_music:
        pm.Channel(0).set_volume(0)
    else:
        pm.Channel(0).set_volume(bg_music_volume)
    
    for i in range(1,chennels_num):
        if not shootes_sound:
            pm.Channel(i).set_volume(0)
        else:
            pm.Channel(i).set_volume(shootes_sound_volume)

def settings_cancle():
    """cancle any chenge that was done in the settings (if it wasn't saven)"""
    global bg_music
    global shootes_sound
    global shootes_sound_volume
    global bg_music_volume
    bg_music_volume, shootes_sound_volume, bg_music, shootes_sound= T_sound_data
    sound_volume_correct()

def for_menu_screen():
    """paint the backgroand of manu screen in the start of each frame"""
    
    global screen
    screen.blit(bg, (0,0))

def before_menu_screen_display():
    """supposed to take place after the screen is drawn (but before the elarts are sown). used for things that take place in each screen"""
    global screen
    global reload
    global nextRunFileName
    global screen
    global wind_chenge_t
    global alert_data
    global past_frames_t
    global frames_to_evereg

    #print("frames per second:",frames_to_evereg/(time.time()-past_frames_t[0]))
    past_frames_t.pop(0)
    past_frames_t.append(time.time())
    #glitter draw
    if wind_chenge_t< glitterT and prew_window_screen!=None:
        glitter_x= 1500*(glitterT-wind_chenge_t)/glitterT
        cropped = pygame.Surface((glitter_x, 700))
        cropped.blit(prew_window_screen, (0, 0))
        screen.blit(cropped,(0,0))
        screen.blit(glitter,(glitter_x-glitter.get_width()/2,0))
        wind_chenge_t+=1
        

    #bottom info line drawing
    screen.blit(down_info_img,(0,700))
    if not curecnt_window in ["TheMainGame.the_main_game_server","TheMainGame.the_main_game_claint","TheMainGame.montaz_show"]:
        screen.blit(fan_made_logo,(1250,500))
    #pygame.draw.rect(screen,(25,25,25),pygame.Rect(0,700,2000,200))
    if username!=None:
        font= pygame.font.SysFont("Arial", 40)
        screen.blit(font.render("your username: "+str(username), True, (0, 0, 0)),(100,710))
    
    if is_connected:
        font= pygame.font.SysFont("Arial", 40)
        screen.blit(font.render("connected", True, (0, 0, 0)),(850,710))
    elif server_address==[]:
        font= pygame.font.SysFont("Arial", 40)
        screen.blit(font.render("no connection", True, (0, 0, 0)),(850,710))
    else:
        font= pygame.font.SysFont("Arial", 23) 
        screen.blit(font.render("Something went wrong, make sure you typed the right enterence code", True, (0, 0, 0)),(850,710))
        screen.blit(font.render("and in same network as the server", True, (0, 0, 0)),(850,740))

    #reload if necessary
    if curecnt_window in ["TheMainGame.the_main_game_server","TheMainGame.the_main_game_claint","TheMainGame.montaz_show"]:
        reload= False
    elif reload:
        reload= False
        print(curecnt_window)
        nextRunFileName= curecnt_window
        raise internalException("reload")

    if curecnt_window!="TheMainGame.the_main_game_server" and curecnt_window!="TheMainGame.the_main_game_claint":
        if not pm.Channel(0).get_busy():
            clip= random.randint(1,3)
            pm.Channel(0).play(pygame.mixer.Sound('sounds/bg_music/'+str(clip)+'.mp3'))

    if alert_data!=None:
        if elart(alert_data[0],alert_data[1]):
            nextRunFileName= ""
            raise internalException("exit during elart")
        alert_data=None

    #screen_video()
    #screenphoto()

def screen_video():
    global frame_num
    try:
        frame_num+=1
    except:
        frame_num=0

    if not os.path.exists("temp"):
        os.mkdir("temp")
    pygame.image.save(screen,"temp/"+str(frame_num)+".jpg")

def screenphoto():
    """doing screen photo and save it in temp.png if user pussed p key. NOTE: it use progect book writing and happen only if you call this function in the end of before_menu_screen_display"""
    pressed = pygame.key.get_pressed()
        
    if pressed[pygame.K_p]:
        pygame.image.save(screen,"temp.jpg")

class internalException(Exception):
    "used to stop main fanction (the window) run from global_var"
    pass

#usefull fanctions


def unconnected_exit_check(destination):
    """check is this computer disconected from the server, and """
    #assume that there is no data that need to be transmited to the destination
    #check is the disconect and if yes, throw Exception and go to distination file
    global nextRunFileName
    if not is_connected:
        nextRunFileName= destination
        raise internalException("unconnected exit")

def unable(button):
    """unable the button (chenge the image and block the onclick function)"""
    button.color= (200,200,200)
    button.onclick= lambda: print("unabled")
    button.set_img(pygame.image.load("images/system image/blocked_button.png"))
    button.set_onpose_img(None)

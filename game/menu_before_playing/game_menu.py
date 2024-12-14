import global_var
import pygame
from usefull_classes.button import button
import sentOperations.sendingOperations as sockF
from usefull_classes.elart import elart

def toOtherFile(file):
    """go to another window
    :param file: path to next window
    :type file: string"""
    global done
    global_var.nextRunFileName=file
    done=True

def oneCompG():
    """called when the user dacide to play offline game"""
    global_var.plaingOnline= False
    toOtherFile("menu_before_playing.char_choose.choose")

def traningGround():
    """called when the user dacide to play in the trening ground"""
    global_var.is_traning= True
    oneCompG()

def main():
    """the code of this window. it's screen is in global_var.screen."""
    global done
    done = False
    clock = pygame.time.Clock()

    #initing flags in global_var
    global_var.plaingOnline= True
    global_var.is_traning= False
    global_var.is_known_competitor= False


    #criating buttons
    buttons=[button(lambda: toOtherFile("menu_before_playing.char_choose.choose"),(450,200,350,100),(255,0,0),"game with stranger"),
             button(lambda: toOtherFile("menu_before_playing.friendGame.friendGame"),(450,320,350,100),(255,0,0),"game with friend"),
             button(lambda: oneCompG(),(850,200,250,100),(255,0,0),"offline game"),
             button(lambda: traningGround(),(850,320,300,100),(255,0,0),"traning ground"),
             button(lambda: toOtherFile("menu_before_playing.mane_menu"),(690,570,250,100),(255,0,0),"back")]

    #unable the anavilable buttons
    global_var.unable(buttons[3])
    buttons[3].onclick= lambda: print("need to be chenged")

    special_ip_check= True
    if (not global_var.is_connected) or (len(global_var.server_address)==1 and global_var.server_address[0][0]=="127.0.0.1" and special_ip_check):
        global_var.unable(buttons[0])
        global_var.unable(buttons[1])

    if global_var.username==None:
        global_var.unable(buttons[1])

    #running the window
    while not done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
            global_var.for_menu_screen()

            for b in buttons:
                b.tick()

            global_var.before_menu_screen_display()

            if global_var.data=="unconnected exit":
                global_var.data= None
                if elart("you disconnected from the server",(600,10,300,100)):
                    done=True
            
            pygame.display.flip()
            clock.tick(24)
            

if __name__=="__main__":
        main()
else:
        print(__name__)

import global_var
import pygame
from usefull_classes.button import button
import sentOperations.sendingOperations as sockF

def toOtherFile(file):
    """go to another window (and send meseg about exiting from this window)
    :param file: path to next window
    :type file: string"""
    global done
    global_var.nextRunFileName=file
    done=True
    sockF.sendMesegTCP(global_var.server_TCP_sock,"GAME|EXIT")

def refuse(file):
    """active when the user refuse to play again.
    :param file: path to the window to open after refusing
    :type file: string"""
    sockF.sendMesegTCP(global_var.server_TCP_sock,"GAME|P2 STATUES UPDATE|False")
    global_var.is_known_competitor= False
    toOtherFile(file)
    
def repit():
    """this function is called when the user decide to play again."""
    global agreed
    global buttons

    if agreed[1]!=-1:
        agreed[0]=1
        buttons[2].color= (200,200,200)
        sockF.sendMesegTCP(global_var.server_TCP_sock,"GAME|P2 STATUES UPDATE|True")

def main():
    """the code of this window. it's screen is in global_var.screen."""
    global done
    global choosedChar
    global chars
    global agreed
    global buttons

    sockF.sendMesegTCP(global_var.server_TCP_sock,"GAME|ENTER|continue choose")

    V_img= pygame.transform.scale(pygame.image.load("images/system image/V.png"), (100,100))
    X_img= pygame.transform.scale(pygame.image.load("images/system image/X.png"), (100,100))
    q_img= pygame.transform.scale(pygame.image.load("images/system image/q_mark.png"), (50,100))
    
    done = False
    clock = pygame.time.Clock()
    agreed= [0,0]

    buttons=[button(lambda: refuse("menu_before_playing.game_menu"),(500,350,200,100),(255,0,0),"to menu"),
             button(lambda: refuse("menu_before_playing.char_choose.choose"),(800,350,400,100),(255,0,0),"new random game"),
             button(lambda: repit(),(775,600,150,60),(255,0,0),"repeat")]

    font= pygame.font.SysFont("Algerian", 30)
    winerText= font.render(global_var.data, True, (186, 201, 0))
    if global_var.data=="the second player went of the game":
        agreed[1]=-1
        global_var.unable(buttons[2])

    while not done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
            global_var.for_menu_screen()

            for b in buttons:
                b.tick()

            serverMsg= sockF.unpucketMasegTCP(global_var.server_TCP_sock)
            if serverMsg!="":
                serverMsg=serverMsg.split("|")
                print(serverMsg)
                if serverMsg[0]=="P2 STATUES UPDATE" and serverMsg[1] in ["True","False"]:
                    if serverMsg[1]=="True":
                        agreed[1]=1
                    else:
                        agreed[1]=-1
                        global_var.unable(buttons[2])
                    print(agreed)

            img= q_img
            if agreed[0]==1:
                img= V_img
            elif agreed[0]==-1:
                img= X_img
            rect= img.get_rect()
            rect.center= (550,620)
            global_var.screen.blit(img, rect)

            img= q_img
            if agreed[1]==1:
                img= V_img
            elif agreed[1]==-1:
                img= X_img
            rect= img.get_rect()
            rect.center= (700,620)
            global_var.screen.blit(img, rect)

            if agreed==[1,1]:
                global_var.is_known_competitor= True
                toOtherFile("menu_before_playing.char_choose.choose")

            global_var.screen.blit(winerText, (450,250))
            global_var.before_menu_screen_display()
            
            pygame.display.flip()
            clock.tick(24)
            

if __name__=="__main__":
        main()
else:
        print(__name__)

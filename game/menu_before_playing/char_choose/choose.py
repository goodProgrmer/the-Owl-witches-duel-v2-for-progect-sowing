import global_var
import pygame
from usefull_classes.button import button
import sentOperations.sendingOperations as sockF
import shutil

def toOtherFile(file):
    """go to another window (and send meseg about exiting from this window if necessary)
    :param file: path to next window
    :type file: string"""
    global done
    global_var.nextRunFileName=file
    done=True
    if file!="menu_before_playing.char_choose.waitingWindow":
        print("exit")
        if global_var.is_known_competitor:
            sockF.sendMesegTCP(global_var.server_TCP_sock,"GAME|P2 STATUES UPDATE|False")
        sockF.sendMesegTCP(global_var.server_TCP_sock,"GAME|EXIT")

def chooseCharacter(cNum):
    """called when the user click on one of the characters
    :param cNum: the index of the character that the user clicked on
    :type cNum: int"""
    global lastChoosed
    global choosedChar
    global choosedCharP2
    
    if global_var.plaingOnline:
        choosedChar= cNum
    else:
        if lastChoosed==2:
            lastChoosed=1
            choosedChar= cNum
        else:
            lastChoosed= 2
            choosedCharP2= cNum

def chooseCharacterFuncGenerator(cNum):
    """return function that when called, call to chooseCharacter with the given number
    :param cNum: the given number
    :type cNum: int"""
    return lambda: chooseCharacter(cNum)

def rectP(cNum,startP,choosing_button_size):
    """return the x,y for rect that need to be drown for character with index cNum
    :param cNum: the index of the character
    :param startP: the place of image of the first character
    :param choosing_button_size: the size of character images
    :type cNum: int
    :type startP: (float,float)
    :type choosing_button_size: (float,float)"""
    return (startP[0]+cNum*(choosing_button_size[0]+20),startP[1])

def choose():
    """called when the user click on the choose button"""
    global agreed
    if global_var.plaingOnline:
        if choosedChar>=0:
            global_var.data= [chars[choosedChar]]
            if global_var.is_known_competitor:
                agreed[0]=1
                sockF.sendMesegTCP(global_var.server_TCP_sock,"GAME|P2 STATUES UPDATE|True")
                global_var.data+=agreed
            else:
                sockF.sendMesegTCP(global_var.server_TCP_sock,"GAME|RANDGAME")
            toOtherFile("menu_before_playing.char_choose.waitingWindow")
            montaz_save(1)
    else:
        if choosedChar>=0 and choosedCharP2>=0:
            global_var.data= [chars[choosedChar],chars[choosedCharP2]]
            toOtherFile("TheMainGame.the_main_game_server")
            montaz_save(1)
            montaz_save(2)

def montaz_save(pNum):
    """saving the montaz (the video and directory) for player pNum to TheMainGame\images\montaz directory
    :param pNum: the number of the player to which it need save the montaz
    :type pNum: int (1 or 2)"""
    shutil.rmtree("TheMainGame/images/montaz/p"+str(pNum), True)
    character= chars[choosedChar]
    if pNum==2:
        character= chars[choosedCharP2]
    shutil.copytree("images/montaz/"+character, "TheMainGame/images/montaz/p"+str(pNum))
    shutil.copy("images/montaz/"+character+".mp4", "TheMainGame/images/montaz/p"+str(pNum)+".mp4")

def main():
    """the code of this window. it's screen is in global_var.screen."""
    global done
    global choosedChar
    global chars

    global choosedCharP2
    global lastChoosed
    global agreed

    if global_var.plaingOnline:
        global_var.unconnected_exit_check("menu_before_playing.game_menu")

    sockF.sendMesegTCP(global_var.server_TCP_sock,"GAME|ENTER|char choose")
    
    done = False
    clock = pygame.time.Clock()

    buttons=[button(lambda: toOtherFile("menu_before_playing.game_menu"),(20,20,100,50),(255,0,0),"back"),
             button(lambda: choose(),(700,600,200,50),(255,0,0),"choose")]
    chars= ["hunter","emity","luz","willow","gus"]
    choosing_button_size=(120,160)
    xCenter= 800
    startX= xCenter- ((choosing_button_size[0]+20)*len(chars)-20)/2
    startY=250
    startP=(startX,startY)
    choosedChar=-100
    choosedCharP2=-100
    lastChoosed= 2
    agreed= [0,0]
    V_img= pygame.transform.scale(pygame.image.load("images/system image/V.png"), (100,100))
    X_img= pygame.transform.scale(pygame.image.load("images/system image/X.png"), (100,100))
    q_img= pygame.transform.scale(pygame.image.load("images/system image/q_mark.png"), (100,100))

    if global_var.plaingOnline:
        instractions= "choose 1 character"
    else:
        instractions= "choose 2 characters"
    font= pygame.font.SysFont("Algerian", 50)
    instractions= font.render(instractions,True,(186, 201, 0))

    #gus special instractions
    font2= pygame.font.SysFont("Algerian", 30)
    gus_disabled= font2.render("gus is unavailable in offline games",True,(186, 201, 0))

    for i in range(len(chars)):
        #print("menu_before_playing\\char_choose\\chars_profiles\\"+chars[i]+".png")
        charImage= pygame.image.load("menu_before_playing\\char_choose\\chars_profiles\\"+chars[i]+".png")
        f= chooseCharacterFuncGenerator(i)
        if i==4 and not global_var.plaingOnline:
            charImage= pygame.image.load("menu_before_playing/char_choose/chars_profiles/unavilable gus.png")
            f= lambda: print("blocked")
            
        buttons.append(button(f,(startX+(choosing_button_size[0]+20)*i,startY,choosing_button_size[0],choosing_button_size[1]),(200,200,200)
                              ,image=charImage, onpose_img= None))

    while not done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
            global_var.for_menu_screen()

            if global_var.is_known_competitor:
                serverMsg= sockF.unpucketMasegTCP(global_var.server_TCP_sock)
                if serverMsg!="":
                    serverMsg=serverMsg.split("|")
                    print(serverMsg)
                    if serverMsg[0]=="P2 STATUES UPDATE" and serverMsg[1] in ["True","False"]:
                        if serverMsg[1]=="True":
                            agreed[1]=1
                        else:
                            agreed[1]=-1
                            buttons[1].color= (200,200,200)
                        print(agreed)
                
                img= q_img
                if agreed[0]==1:
                    img= V_img
                elif agreed[0]==-1:
                    img= X_img
                global_var.screen.blit(img, (450,570))

                img= q_img
                if agreed[1]==1:
                    img= V_img
                elif agreed[1]==-1:
                    img= X_img
                global_var.screen.blit(img, (600,570))
            
            for b in buttons:
                b.tick()

            frameP= rectP(choosedChar,startP,choosing_button_size)
            pygame.draw.rect(global_var.screen, (0,255,0), pygame.Rect(frameP[0],frameP[1],choosing_button_size[0],choosing_button_size[1]),width=5)
            
            if not global_var.plaingOnline:
                frameP= rectP(choosedCharP2,startP,choosing_button_size)
                pygame.draw.rect(global_var.screen, (255,0,0), pygame.Rect(frameP[0],frameP[1],choosing_button_size[0],choosing_button_size[1]),width=5)

            global_var.screen.blit(instractions,(525,475))
            if not global_var.plaingOnline:
                global_var.screen.blit(gus_disabled,(520,550))

            global_var.before_menu_screen_display()
            pygame.display.flip()
            clock.tick(24)
            

if __name__=="__main__":
        main()
else:
        print(__name__)

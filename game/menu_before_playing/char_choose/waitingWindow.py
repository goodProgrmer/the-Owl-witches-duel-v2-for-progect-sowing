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
    if global_var.is_known_competitor:
            sockF.sendMesegTCP(global_var.server_TCP_sock,"GAME|P2 STATUES UPDATE|False")
    sockF.sendMesegTCP(global_var.server_TCP_sock,"GAME|EXIT")

def isIP(IP):
    """check does the IP correct
    :param IP: the IP to check
    :type IP: string"""
    IP_list= IP.split(".")
    for n in IP_list:
        try:
            num= int(n)
        except:
            return False
        if num<0 or num>255:
            return False
    return True

def main():
    """the code of this window. it's screen is in global_var.screen."""
    global done
    global choosedChar

    if global_var.plaingOnline:
        global_var.unconnected_exit_check("menu_before_playing.game_menu")
    
    done = False
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Algerian", 50)
    text = font.render("wait for other players", True, (186, 201, 0))

    buttons=[button(lambda: toOtherFile("menu_before_playing.game_menu"),(20,20,100,50),(255,0,0),"back")]
    chars= ["hunter","emity","luz","willow","gus"]
    V_img= pygame.transform.scale(pygame.image.load("images/system image/V.png"), (100,100))
    X_img= pygame.transform.scale(pygame.image.load("images/system image/X.png"), (100,100))
    q_img= pygame.transform.scale(pygame.image.load("images/system image/q_mark.png"), (100,100))
    agreed= [0,0]
    if global_var.is_known_competitor:
        agreed[0]= global_var.data[1]
        agreed[1]= global_var.data[2]

    while not done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
            global_var.for_menu_screen()

            for b in buttons:
                b.tick()

            global_var.screen.blit(text,(500,250))

            serverMsg= sockF.unpucketMasegTCP(global_var.server_TCP_sock)
            if serverMsg!="":
                serverMsg=serverMsg.split("|")
                print(serverMsg)
                #print(len(serverMsg[0])==3 , serverMsg[0]=="GAME START" , isIP(serverMsg[1]) , (serverMsg[2] in ["True","False"]))
                if len(serverMsg)==4 and serverMsg[0]=="GAME START" and isIP(serverMsg[1]) and (serverMsg[2] in ["True","False"]):
                    print("in the if")
                    if serverMsg[2]=="True":
                        print("I will be game serwer")
                        global_var.nextRunFileName="TheMainGame.the_main_game_server"
                        done=True
                    else:
                        print("I will be game clant")
                        global_var.nextRunFileName="TheMainGame.the_main_game_claint"
                        done=True
                    f=open("TheMainGame\\mainGameCommunicationInfo.txt","w")
                    f.write(str([serverMsg[1],serverMsg[3]]))
                    f.close()
                if global_var.is_known_competitor and len(serverMsg)==2 and serverMsg[0]=="P2 STATUES UPDATE" and serverMsg[1] in ["True","False"]:
                    if serverMsg[1]=="True":
                        agreed[1]=1
                    else:
                        agreed[1]=-1
                    print(agreed)

            if global_var.is_known_competitor:
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

            global_var.before_menu_screen_display()
            pygame.display.flip()
            clock.tick(24)


if __name__=="__main__":
        main()
else:
        print(__name__)

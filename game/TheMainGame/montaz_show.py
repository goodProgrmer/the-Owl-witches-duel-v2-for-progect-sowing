import global_var
import pygame
from usefull_classes.button import button
import sentOperations.sendingOperations as sockF
import shutil

def toOtherFile(file):
    """chenge the window to file (using done veriable to close this window)
    :param file: path to the window which it need to run next
    :type file: string"""
    global done
    global_var.nextRunFileName=file
    done=True

def main():
    """the code of this window. it's screen is in global_var.screen."""
    global done
    #this window will open only if one of the players win (not when one of them exit of the game)
    
    plaingOnline= global_var.plaingOnline
    global_var.plaingOnline=True

    if plaingOnline:
        aftershowing="menu_before_playing.playAgain"
    else:
        aftershowing="menu_before_playing.game_menu"
    print(aftershowing,global_var.plaingOnline,global_var.data)
    
    done = False
    clock = pygame.time.Clock()
    t=0

    #check who is the winner
    winner= 1
    if global_var.data[:12]=="player 2 win":
        winner= 2
    elif global_var.data[:12]=="player 1 win":
        winner= 1
    else:
        toOtherFile(aftershowing)
        return
    global_var.wind_chenge_t= global_var.glitterT #removing the window chenge effect
    #chechk how many frames there is in this wining montaz
    f= open("TheMainGame/images/montaz/p"+str(winner)+"/frames num.txt", "r")
    frame_num= int(f.read())
    f.close()

    global_var.pm.Channel(0).play(pygame.mixer.Sound('sounds/montuz.mp3'))

    #show the montaz
    while not done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
            global_var.for_menu_screen()
            img= pygame.image.load("TheMainGame/images/montaz/p"+str(winner)+"/"+str(t)+".jpg")
            img= pygame.transform.scale(img, (1500,700))
            global_var.screen.blit(img,(0,0))
            t+=1
            if t>=frame_num:
                toOtherFile(aftershowing)
            global_var.before_menu_screen_display()
            pygame.display.flip()
            clock.tick(24)
            

if __name__=="__main__":
        main()
else:
        print(__name__)

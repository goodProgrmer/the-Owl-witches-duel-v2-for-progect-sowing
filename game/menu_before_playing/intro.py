import global_var
import pygame
from usefull_classes.button import button
import os

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
    
    
    t=0
    f= open("images/intro/frames num.txt","r")
    frame_num= int(f.read())
    f.close()
    references= {}
    for i in range(frame_num):
        references[i]= i
    f= open("images/intro/reference file.txt","r")
    for line in f:
        splited= line.split("-")
        references[int(splited[0])]= int(splited[1])
    f.close()
    try:
        f=open("already runed.txt","x")
        f.close()
        is_first= True
    except:
        is_first=False
    b= button(lambda: toOtherFile("menu_before_playing.mane_menu"),(1250,700,225,75),(255,0,0),"skip intro")
    done= False
    clock = pygame.time.Clock()
    global_var.pm.Channel(0).play(pygame.mixer.Sound('sounds/intro.mp3'))
    #show the intro
    while not done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
            img= pygame.image.load("images/intro/"+str(references[t])+".jpg")
            img= pygame.transform.scale(img, (1500,800))
            global_var.screen.blit(img,(0,0))
            if not is_first:
                b.tick()
            t+=1
            if t>=frame_num:
                toOtherFile("menu_before_playing.mane_menu")
            pygame.display.flip()
            clock.tick(30)
    global_var.pm.Channel(0).stop()

if __name__=="__main__":
        main()
else:
        print(__name__)

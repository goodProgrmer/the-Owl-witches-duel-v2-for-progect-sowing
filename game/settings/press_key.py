import pygame
import global_var
from usefull_classes.button import button

def quitElart():
    """quit the elart"""
    global done
    done= True

def press(text,rect_tuple,font=None):
    """create alert (with no cencle option that close when the user press any key on the keybord)
    :param text: the text in the alert
    :param rect_tuple: the rect on which the text is drawn in the next format: (x,y,hight,width)
    :param font: the font of the text. by difault pygame.font.SysFont("Algerian", 15)
    :type text: string
    :type rect_tuple: (float,float,float,float)
    :type font: pygame.font
    :return: -1 if the x button of the window was clicked
             -2 if esc key was clicked
             the key pygame integer if anything else was klicked
    :rtype: int"""
    #return:
    #-1 if the x button of the window was clicked
    #-2 if esc key was clicked
    #the key pygame integer if anything else was klicked
    global done

    if font==None:
        font = pygame.font.SysFont("Algerian", 15)

    #screen preperation
    s= pygame.Surface((10000,10000))
    s.set_alpha(128)
    s.fill((0,0,0))
    global_var.screen.blit(s,(0,0))
    back_ground= global_var.screen

    #pygame variable init
    done= False
    clock = pygame.time.Clock()

    #constants
    BUUTON_H= 50

    #values to display
    text= font.render(text, True, (186, 201, 0))

    while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    return -1
                if event.type == pygame.KEYDOWN:
                    if event.key== pygame.K_ESCAPE:
                        done= True
                        return -2
                    return event.key
            
            global_var.screen.blit(back_ground,(0,0))

            pygame.draw.rect(global_var.screen, (0,0,160), pygame.Rect(rect_tuple))

            #sending prpose paint
            global_var.screen.blit(text, (rect_tuple[0]+10, rect_tuple[1]+10))
            
            pygame.display.flip()
            clock.tick(24)
        

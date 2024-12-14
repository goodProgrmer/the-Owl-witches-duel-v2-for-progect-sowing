import pygame
import global_var
from usefull_classes.button import button

def quitElart():
    """quit the elart"""
    global done
    done= True

def elart(text,rect_tuple,font=None):
    """when called, pause the previous window and pass the frames  in this fanction. create elart that will disapear when you click on the ok button
    :param text: the elart text
    :param rect_tuple: where will be the rect of the elart. it's in the next format: (x,y,width,hight)
    :param font: the font of the text. by defult it is pygame.font.SysFont("Algerian", 15)
    :type text: string
    :type rect_tuple: (float,float,float,float)
    :type font: pygame.font or None
    :return: true if the x button of the window was clicked
    :rtype: bool"""
    
    global done

    if font==None:
        font = pygame.font.SysFont("Algerian", 15)

    #screen preperation
    s= pygame.Surface((10000,10000))
    s.set_alpha(128)
    s.fill((0,0,0))
    global_var.screen.blit(s,(0,0))
    back_ground= global_var.screen.copy()

    #pygame variable init
    done= False
    clock = pygame.time.Clock()

    #constants
    BUUTON_H= 50

    #values to display
    buttons=[button(quitElart,(rect_tuple[0]+10, rect_tuple[1]+rect_tuple[3]-10-BUUTON_H, rect_tuple[2]-20, BUUTON_H),(255,0,0),"ok")]

    #creating alert screen
    pygame.draw.rect(back_ground, (0,0,160), pygame.Rect(rect_tuple))
    
    text= text.split("\n")
    text_y= rect_tuple[1]+10
    
    for i in range(len(text)):
        put_text= font.render(text[i], True, (186, 201, 0))
        back_ground.blit(put_text, (rect_tuple[0]+10, text_y))
        text_y+= put_text.get_height()+10
    

    while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    return True

            global_var.screen.blit(back_ground, (0,0))
            
            for b in buttons:
                b.tick()
            
            pygame.display.flip()
            clock.tick(24)
    return False
        

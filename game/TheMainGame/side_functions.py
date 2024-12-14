import pygame
import global_var
from usefull_classes.button import button
import TheMainGame.datafiles.imeges as img_dict

def count(font=None):
    """this stop the previoas window (without exit from it) and  start count of the start of the game.
    :return: true if the x button of the window was clicked, otherwise it returns false
    :rtype: bool"""
    global done

    if font==None:
        font = pygame.font.SysFont("Arial", 100)

    #screen preperation
    s= pygame.Surface((10000,10000))
    s.set_alpha(128)
    s.fill((0,0,0))
    global_var.screen.blit(s,(0,0))
    back_ground= global_var.screen.copy()

    #pygame variable init
    done= False
    clock = pygame.time.Clock()
    t=0

    #constents
    SECOND_T= 30 #the emount of frames that pass for 1 number

    NUMBERS= []

    for i in range(3):
        #NUMBERS.append(pygame.transform.scale(pygame.image.load("images/system image/count/X.png"), (400,100)))
        NUMBERS.append(pygame.image.load("images/system image/count/"+str(i+1)+".png"))

    while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    return True

            #print(t)
            global_var.screen.blit(back_ground,(0,0))

            #sending prpose paint
            img= NUMBERS[2-t//SECOND_T]
            rect= img.get_rect()
            rect.center= (800,400)
            global_var.screen.blit(img, rect)
            t+=1

            if 3-t//SECOND_T<=0:
                done=True
            
            pygame.display.flip()
            clock.tick(24)
    return False

def loading_display(end):
    #NOTE: end param is list with len=1 when end[0] is boolean (when end[0] is True the function stop its running)
    circle= pygame.image.load("TheMainGame/images/loading.png")
    surface= pygame.Surface((circle.get_width()*2,circle.get_width()*2)).convert_alpha()
    surface.fill((0,0,0,0))
    surface.blit(circle,(0,0))
    circle= surface
    print(type(surface),type(circle))
    angle= 0
    font = pygame.font.SysFont("Algerian", 50)
    text = font.render("loading", True, (186, 201, 0))
    clock = pygame.time.Clock()
    while not end[0]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        global_var.for_menu_screen()
        global_var.screen.blit(text,(550,300))
        to_draw= pygame.transform.rotate(circle,angle)
        rect= to_draw.get_rect()
        rect.center= (950,325)
        global_var.screen.blit(to_draw,rect)
        angle+= 3
        if angle%90==0:
            pass
            #print(angle)
        global_var.before_menu_screen_display()
        pygame.display.flip()
        clock.tick(30)
    return False

def tutorial_paint_init(keys,chars):
    #keys[i]==[] if the player dont play from this computer
    char_str= {"hunter":"""-teleport (from self)
-ground punch
-punch
-teleport (to enemy)
-ricochet shots""","emity":"""-throw golem head
-slime bubble
-punch
-create golem
-shield""","luz":"""-stunning light
-iceberg jump
-fire ball
-vine attack
-ice wall""","willow":"""-wall strike
-power plant
-plant wall
-dig
-triple vine""","gus":"""-black (enemy screen)
-clones
-punch
-fly/stop flying
-vanish (enemy screen)"""} # Restrict to 16 chars per move.
    font1= pygame.font.SysFont("Arial", 20) #for the key text
    tutorial= pygame.transform.scale(pygame.image.load("TheMainGame/images/tutorial.png"),(500,200))
    tutorial_r= pygame.transform.flip(tutorial,True,False)
    key_box= pygame.transform.scale(pygame.image.load("images/system image/key button.png"),(30,30))
    key_surface= []
    for i in range(len(keys)):
        key_surface.append([])
        for j in range(len(keys[i])):
            key= keys[i][j]
            text= font1.render(toChar(key), True, (186, 201, 0))
            textRect = text.get_rect()
            textRect.center= (key_box.get_width()/2, key_box.get_height()/2)
            key_surface[-1].append(key_box.copy())
            key_surface[-1][-1].blit(text,textRect)
            #print(type(key_box),type(key_surface[-1][-1]))

    tutorial_blit(tutorial, 150, key_surface[0],char_str[chars[0]])
    print(char_str,chars[1])
    tutorial_blit(tutorial_r, 10, key_surface[1],char_str[chars[1]])
    img_dict.imegesDict["tutorial"]= tutorial
    img_dict.imegesDict["tutorial-r"]= tutorial_r
        

def tutorial_blit(surface,x_start, key_surface,char_str):
    if key_surface==[]:
        return
    font2= pygame.font.SysFont("Algerian", 20) #for movemant label
    font3= pygame.font.SysFont("Algerian", 15) #for special op labels
    surface.blit(key_surface[0],(x_start,100))
    surface.blit(key_surface[1],(x_start+70,100))
    surface.blit(key_surface[2],(x_start+35,65))
    surface.blit(key_surface[3],(x_start+35,100))
    surface.blit(font2.render("movement:", True, (186, 201, 0)),(x_start,30))
    c_text= char_str.split("\n")
    for i in range(5):
        surface.blit(key_surface[4+i],(x_start+130,10+35*i))
        surface.blit(font3.render(c_text[i], True, (186, 201, 0)),(x_start+165,17+35*i))
    

def toChar(num):
    """trunslate pygame key index to chr (including letters and errows)
    :param num: pygame index of pussed key
    :type num: int"""
    try:
        return chr(num)
    except Exception as e:
        print(e)
        if num==pygame.K_LEFT:
            return u"\u2190"
        if num==pygame.K_RIGHT:
            return u"\u2192"
        if num==pygame.K_UP:
            return u"\u2191"
        if num==pygame.K_DOWN:
            return u"\u2193"

def tutorial_paint(draw):
    if draw[0] and draw[1]:
        global_var.screen.blit(img_dict.imegesDict["tutorial"],(240,10))
        global_var.screen.blit(img_dict.imegesDict["tutorial-r"],(760,10))
    elif draw[0]:
        global_var.screen.blit(img_dict.imegesDict["tutorial"],(int(750-img_dict.imegesDict["tutorial"].get_width()/2),10))
    elif draw[1]:
        global_var.screen.blit(img_dict.imegesDict["tutorial-r"],(int(750-img_dict.imegesDict["tutorial-r"].get_width()/2),10))
    
    

    

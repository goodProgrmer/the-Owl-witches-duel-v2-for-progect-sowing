import global_var
import pygame
from usefull_classes.button import button
from settings.press_key import press
import sentOperations.sendingOperations as sockF

def toOtherFile(file):
    """go to another window
    :param file: path to next window
    :type file: string"""
    global done
    global_var.nextRunFileName=file
    done=True

def onclick(i,j):
    """called when one of the keys buttons clicked. it chenge the flag to the indexs of the key button that clicked (buttons[j][i] is clicked).
    :param i,j: the indexs of the clicked button in buttons list (buttons[j][i] is clicked)
    :type i: int
    :type j: int"""
    global button_elart
    button_elart= (i,j)

def button_chenge(i,j):
    """get key from the user and put it as text of the button buttons[j][i]
    :param i,j: the indexs of the clicked button in buttons list (buttons[j][i] is clicked)
    :type i: int
    :type j: int"""
    global buttons
    global done
    key= press("press key to chenge (or escape to return)",(550,10,400,50))
    if key==-1:
        done= True
        return
    if key==-2:
        return
    try:
        buttons[i+ len(global_var.T_buttons2P[0])*j].text= toChar(key)
        global_var.T_buttons2P[j][i-1]= key
    except Exception as e:
        print(e,i-1)
        pass

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

def lambdaFconstractor(f,x,y):
    """return function the when called, call f(x,y)
    :param f: given f
    :param x: given x
    :param y: given y
    :type f: function
    :type x: anything
    :type y: anything"""
    return lambda: f(x,y)

def save():
    """activated when the save button pussed"""
    print(global_var.T_buttons1P)
    global_var.settings_save()
    toOtherFile("menu_before_playing.mane_menu")

def cancle():
    """activated when the cancle button pussed"""
    global_var.settings_cancle()
    toOtherFile("menu_before_playing.mane_menu")

def main():
    """the code of this window. it's screen is in global_var.screen."""
    global done
    global choosedChar
    global buttons
    global button_elart
    
    done = False
    clock = pygame.time.Clock()
    key_button=  pygame.image.load("images/system image/key button.png")
    key_button_pressed= pygame.image.load("images/system image/key button pressed.png")
    
    buttons=[button(cancle,(20,20,200,75),(255,0,0),"cancel")]
    b_place= [[(400,300),(600,300),(500,200),(500,300),
              (800,200),(900,200),(800,300),(900,300),(1000,300)],
              [(400,550),(600,550),(500,450),(500,550),
              (800,450),(900,450),(800,550),(900,550),(1000,550)]]
    button_elart= None #which of the buttons (for keys settings) was clicked in the last fram (in format of (i,j))

    for j in range(2):
        for i in range(len(global_var.T_buttons2P[0])):
            buttons.append(button(lambdaFconstractor(onclick,i+1,j),(b_place[j][i][0],b_place[j][i][1],60,60),(255,0,0),toChar(global_var.buttons2P[j][i]),
                                  image=key_button ,onpose_img=key_button_pressed ,font= pygame.font.SysFont("Arial", 30) ,text_indent=(-5,5)))

    buttons.append(button(save,(1200,400,100,75),(255,0,0),"save"))
    buttons.append(button(lambda: toOtherFile("settings.onePlayer"),(250,20,200,75),(255,0,0),"one player"))
    buttons.append(button(lambda: print("unabled"),(500,20,200,75),(255,0,0),"two players", image= pygame.image.load("images/system image/gray button.png"), onpose_img= None))
    buttons.append(button(lambda: toOtherFile("settings.sound"),(750,20,200,75),(255,0,0),"sound"))
    
    while not done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
            global_var.for_menu_screen()

            for b in buttons:
                b.tick()

            global_var.before_menu_screen_display()
            if button_elart!=None:
                button_chenge(button_elart[0],button_elart[1])
                button_elart= None
            pygame.display.flip()
            clock.tick(24)


if __name__=="__main__":
        main()
else:
        print(__name__)

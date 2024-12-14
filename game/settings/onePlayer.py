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

def onclick(i):
    """called when one of the keys buttons clicked. it chenge the flag to the index of the key buttton.
    :param i: the index of the clicked button in buttons list
    :type i: int"""
    global button_elart
    button_elart= i

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

def button_chenge(i):
    """get key from the user and put it as text of button with index i
    :param i: the given button index
    :type i: int"""
    global buttons
    global done
    key= press("press key to chenge (or escape to return)",(550,10,400,50))
    if key==-1:
        done= True
        return
    if key==-2:
        return
    try:
        buttons[i].text= toChar(key)
        global_var.T_buttons1P[0][i-1]= key
    except Exception as e:
        print(e,i-1)
        pass

def lambdaFconstractor(f,x):
    """return function the when called, call f(x)
    :param f: given f
    :param x: given x
    :type f: function
    :type x: anything"""
    return lambda: f(x)

def temp_save_P_init():
    """init all the veriable for temp saving (marked with T_ in the start)"""
    global_var.T_buttons1P= global_var.buttons1P
    global_var.T_buttons2P= global_var.buttons2P
    global_var.T_sound_data= [global_var.bg_music_volume, global_var.shootes_sound_volume, global_var.bg_music, global_var.shootes_sound]

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

    if global_var.T_buttons1P==None:
        temp_save_P_init()
    
    done = False
    clock = pygame.time.Clock()

    key_button=  pygame.image.load("images/system image/key button.png")
    key_button_pressed= pygame.image.load("images/system image/key button pressed.png")
    
    buttons=[button(cancle,(20,20,200,75),(255,0,0),"cancel")]
    b_place= [(400,400),(600,400),(500,300),(500,400),
              (800,300),(900,300),(800,400),(900,400),(1000,400)]
    button_elart= -1 #which of the buttons (for keys settings) was clicked in the last fram

    for i in range(len(global_var.T_buttons1P[0])):
        buttons.append(button(lambdaFconstractor(onclick,i+1),(b_place[i][0],b_place[i][1],60,60),(255,0,0),toChar(global_var.buttons1P[0][i]),
                              image=key_button ,onpose_img=key_button_pressed ,font= pygame.font.SysFont("Arial", 30) ,text_indent=(-5,5)))

    buttons.append(button(save,(750,500,100,50),(255,0,0),"save"))
    buttons.append(button(lambda: print("unabled"),(250,20,200,75),(255,0,0),"one player", image= pygame.image.load("images/system image/gray button.png"), onpose_img= None))
    buttons.append(button(lambda: toOtherFile("settings.twoPlayers"),(500,20,200,75),(255,0,0),"two players"))
    buttons.append(button(lambda: toOtherFile("settings.sound"),(750,20,200,75),(255,0,0),"sound"))

    while not done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
            global_var.for_menu_screen()

            for b in buttons:
                b.tick()

            global_var.before_menu_screen_display()
            if button_elart!=-1:
                button_chenge(button_elart)
                button_elart= -1
            pygame.display.flip()
            clock.tick(24)


if __name__=="__main__":
        main()
else:
        print(__name__)

import global_var
import pygame
from usefull_classes.button import button
from usefull_classes.prossent_line import prossent_line
from settings.press_key import press
import sentOperations.sendingOperations as sockF

def toOtherFile(file):
    """go to another window
    :param file: path to next window
    :type file: string"""
    global done
    global_var.nextRunFileName=file
    done=True

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

def mute(var,button_P):
    """chenge the value of boolean flage (given var) in global_var and chenge the text in button_P index acordingly (this suppost to be mute button)"""
    global buttons
    exec("global_var."+var+"= not global_var."+var)
    if buttons[button_P].text== "mute":
        buttons[button_P].text= "unmute"
    else:
        buttons[button_P].text = "mute"



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
    global prossent_lines
    
    done = False
    clock = pygame.time.Clock()

    prossent_lines= [prossent_line(650,global_var.bg_music_volume,(590,400))]
    font = pygame.font.SysFont("Algerian", 40)
    text = font.render("set background music volume", True, (186, 201, 0)) #the instractions of what you can do here

    muteText= "unmute"
    if global_var.bg_music:
        muteText= "mute"
    buttons= [button(cancle,(20,20,200,75),(255,0,0),"cancel"),button(lambda: mute("bg_music",1),(400,360,150,100),(255,0,0),muteText)]

    buttons.append(button(save,(750,550,100,75),(255,0,0),"save"))
    buttons.append(button(lambda: toOtherFile("settings.onePlayer"),(250,20,200,75),(255,0,0),"one player"))
    buttons.append(button(lambda: toOtherFile("settings.twoPlayers"),(500,20,200,75),(255,0,0),"two players"))
    buttons.append(button(lambda:  print("unabled"),(750,20,200,75),(255,0,0),"sound", image= pygame.image.load("images/system image/gray button.png"), onpose_img= None))
    
    while not done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
            global_var.for_menu_screen()

            #global_var.bg_music_volume,global_var.shootes_sound_volume= prossent_lines[0].get_prossent(), prossent_lines[1].get_prossent()
            global_var.bg_music_volume,global_var.shootes_sound_volume= prossent_lines[0].get_prossent(), global_var.shootes_sound_volume
            global_var.sound_volume_correct()
            
            for l in prossent_lines:
                l.tick()

            for b in buttons:
                b.tick()

            global_var.screen.blit(text,(520,250))

            global_var.before_menu_screen_display()
            pygame.display.flip()
            clock.tick(24)


if __name__=="__main__":
        main()
else:
        print(__name__)

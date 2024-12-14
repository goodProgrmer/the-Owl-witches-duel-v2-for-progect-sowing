import global_var
import pygame
from usefull_classes.button import button
import sentOperations.sendingOperations as sockF
from usefull_classes.roling_scroll import roling_page

def toOtherFile(file):
    """go to another window
    :param file: path to next window
    :type file: string"""
    global done
    global_var.nextRunFileName=file
    done=True

def about_us():
    global scroll
    scroll= roling_page((320,160,920,340), 20, pygame.image.load("images/about us/about us.png"))
    buttons[1]= button(key_philosopy,(340,520,400,75),(236,168,81),"key division philosophy", image=pygame.image.load("images/about us/button.png"),onpose_img=None,
                     font= pygame.font.SysFont("Arial", 40), t_color=(94,67,32))
    buttons[0]= button(lambda: print("unavilable"),(750,520,200,75),(236,168,81),"about us",
                       image=pygame.image.load("images/about us/unavileble button.png"),onpose_img=None, font= pygame.font.SysFont("Arial", 40), t_color=(50,50,50))

def key_philosopy():
    global scroll
    global buttons
    scroll= roling_page((320,160,920,340), 20, pygame.image.load("images/about us/key philoshophy.png"))
    buttons[0]= button(about_us,(750,520,200,75),(236,168,81),"about us", image=pygame.image.load("images/about us/button.png"),onpose_img=None,
                     font= pygame.font.SysFont("Arial", 40), t_color=(94,67,32))
    buttons[1]= button(lambda: print("unavilable"),(340,520,400,75),(236,168,81),"key division philosophy",
                       image=pygame.image.load("images/about us/unavileble button.png"),onpose_img=None, font= pygame.font.SysFont("Arial", 40), t_color=(50,50,50))

def main():
    """the code of this window. it's screen is in global_var.screen."""
    global done
    global scroll
    global buttons
    done = False
    clock = pygame.time.Clock()

    scroll= roling_page((320,160,920,340), 20, pygame.image.load("images/about us/key philoshophy.png"))
    scroll_bg= pygame.image.load("images/about us/scroll.PNG")
    buttons= [None,None,button(lambda: toOtherFile("menu_before_playing.mane_menu"),(10,300,200,100),(255,0,0),"back")]
    key_philosopy()

    while not done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
                    if event.type == pygame.MOUSEWHEEL:
                            scroll.wheel_roll(event.y)
            global_var.for_menu_screen()

            global_var.screen.blit(scroll_bg, (100,0))
            scroll.tick()
            pygame.draw.rect(global_var.screen, (189,135,65),pygame.Rect(325,500,950,130))

            for b in buttons:
                b.tick()

            global_var.before_menu_screen_display()
            pygame.display.flip()
            clock.tick(24)
            

if __name__=="__main__":
        main()
else:
        print(__name__)

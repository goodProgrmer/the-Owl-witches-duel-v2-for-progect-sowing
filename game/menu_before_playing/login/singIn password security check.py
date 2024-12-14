import global_var
import pygame
from usefull_classes.button import button
import sentOperations.sendingOperations as sockF
from usefull_classes.textEnterens import textEnterens
from usefull_classes.elart import elart

def toOtherFile(file):
    """go to another window
    :param file: path to next window
    :type file: string"""
    global done
    global_var.nextRunFileName=file
    done=True



def sendrequest():
    """send sign in request"""
    global username
    username= entrens[0].get_text()
    password= entrens[1].get_text()
    sockF.sendMesegTCP(global_var.server_TCP_sock,"LOGIN|SIGN IN|"+entrens[0].get_text()+"|"+entrens[1].get_text())

def main():
    """the code of this window. it's screen is in global_var.screen."""
    global done
    global entrens
    global username

    global_var.unconnected_exit_check("menu_before_playing.mane_menu")
    
    done = False
    clock = pygame.time.Clock()

    buttons=[button(lambda: toOtherFile("menu_before_playing.mane_menu"),(20,20,200,50),(255,0,0),"back"),
             button(sendrequest,(700,600,200,50),(255,0,0),"sign in"),
             button(lambda: toOtherFile("menu_before_playing.login.login"),(1280,20,200,50),(255,0,0),"log in")]
    username= None

    font= pygame.font.SysFont("Algerian", 30)
    little_font= pygame.font.SysFont("Algerian", 23)
    title_font= pygame.font.SysFont("Algerian", 50)
    
    texts= [((740,160),title_font.render("Sing up", True, (186, 201, 0))),
            ((450,300),font.render("username:", True, (186, 201, 0))),
            ((450,435),font.render("password:", True, (186, 201, 0))),
            ((450,225),little_font.render("ure password must be at least 8 characters", True, (186, 201, 0))),
            ((450,265),little_font.render("and with useg of at least one numbar and one letter", True, (186, 201, 0)))]
    entrens= [textEnterens((450, 340, 750, 75),(255,255,255),font= pygame.font.SysFont("Arial Nova", 35)),
              textEnterens((450, 475, 750, 75),(255,255,255),enter_type="password", font=pygame.font.SysFont("Arial Nova", 35))]

    while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            
            global_var.for_menu_screen()

            #ticking anything
            for o in buttons+entrens:
                o.tick()

            for t in texts:
                if t!=None:
                    global_var.screen.blit(t[1], t[0])

            #server meseges handeling
            serverMsg= sockF.unpucketMasegTCP(global_var.server_TCP_sock)
            if serverMsg!="":
                serverMsg=serverMsg.split("|")
                print(serverMsg)
                if len(serverMsg)==1 and serverMsg[0]=="TAKEN USERNAME":
                    global_var.alert_data= ("this username already taken",(600,10,300,100))
                if len(serverMsg)==1 and serverMsg[0]=="UNCORRECT CERTIFICATES":
                    global_var.alert_data= ("the username or the password against the rools",(500,10,500,100))
                if len(serverMsg)==2 and serverMsg[0]=="DONE":
                    global_var.from_str_to_settings(serverMsg[1])
                    global_var.sound_volume_correct()
                    global_var.username= username
                    toOtherFile("menu_before_playing.mane_menu")

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RETURN]:
                sendrequest()
            
            global_var.before_menu_screen_display()

            #elart showing
            pygame.display.flip()
            clock.tick(24)
            

if __name__=="__main__":
        main()
else:
        print(__name__)

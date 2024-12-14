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

def ip_update():
    text= entrens[0].get_text()
    global_var.connecting_text= text
    print("text:",text)
    if "." in text:
        global_var.server_address= [(text,global_var.SERVER_PORT)]
    else:
        global_var.server_address= ips_unzip(text)
        for i in range(len(global_var.server_address)):
            global_var.server_address[i]= (global_var.server_address[i],global_var.SERVER_PORT)
        print(global_var.server_address)
    toOtherFile("menu_before_playing.mane_menu")

def ips_unzip(string):
    letters="0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    num= 0
    digit=1
    for l in string:
        num+= letters.find(l)*digit
        digit*=len(letters)
    ans=[]
    while(num>0):
        ans.append([])
        for i in range(4):
            ans[-1].append(str(num%256))
            num= num//256

    for i in range(len(ans)):
        ans[i]= ".".join(ans[i])
    return ans

def main():
    """the code of this window. it's screen is in global_var.screen."""
    global done
    global entrens
    global username
    
    done = False
    clock = pygame.time.Clock()

    buttons=[button(lambda: toOtherFile("menu_before_playing.mane_menu"),(20,20,200,50),(255,0,0),"back"),
             button(ip_update,(700,600,200,70),(255,0,0),"connect")]
    username= None

    font= pygame.font.SysFont("Algerian", 40)
    title_font= pygame.font.SysFont("Algerian", 60)
    texts= [((480,200),title_font.render("connect to the server", True, (186, 201, 0))),
            ((450,325),font.render("enterence code:", True, (186, 201, 0)))]
    entrens= [textEnterens((450, 390, 750, 100),(255,255,255),unregular_chr=(46,), text= global_var.connecting_text)]

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

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RETURN]:
                ip_update()

            global_var.before_menu_screen_display()

            pygame.display.flip()
            clock.tick(24)
            

if __name__=="__main__":
        main()
else:
        print(__name__)

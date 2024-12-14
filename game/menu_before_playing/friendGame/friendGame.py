import global_var
import pygame
from usefull_classes.button import button
from usefull_classes.textEnterens import textEnterens
import sentOperations.sendingOperations as sockF
from usefull_classes.elart import elart

def toOtherFile(file):
    """go to another window (and send meseg about exiting from this window)
    :param file: path to next window
    :type file: string"""
    global done
    global_var.nextRunFileName=file
    done=True
    sockF.sendMesegTCP(global_var.server_TCP_sock,"GAME|EXIT")

def acceptOnClick(user):
    """called when the user accepted the propose for game
    :param user: the username of the one who proposed to play
    :type user: string"""
    print("p-accept")
    sockF.sendMesegTCP(global_var.server_TCP_sock,"GAME|ACSEPT|"+user)
    global_var.is_known_competitor= True
    toOtherFile("menu_before_playing.char_choose.choose")

def refuseOnClick(user):
    """called when the user refuse to propose for game
    :param user: the username of the one who proposed to play
    :type user: string"""
    print("p-refuse")
    global toMe_user_propse
    sockF.sendMesegTCP(global_var.server_TCP_sock,"GAME|REFUSE|"+user)
    try:
        toMe_user_propse[user].isActive= False
        toMe_user_propse.pop(user)
    except:
        pass

def cancleOnClick(user):
    """called when the user cancle his own propose for game
    :param user: the username of the address of the proposal
    :type user: string"""
    global fromMe_user_propse
    print("p-cancle",fromMe_user_propse)
    sockF.sendMesegTCP(global_var.server_TCP_sock,"GAME|CANCLE GAME|"+user)
    try:
        print("p-1")
        fromMe_user_propse[user].isActive= False
        fromMe_user_propse.pop(user)
        print("p-2")
    except:
        pass

def lambdaFconstractor(f,x):
    """return function the when called, call f(x)
    :param f: given f
    :param x: given x
    :type f: function
    :type x: anything"""
    return lambda: f(x)

class gameProposal:
    """propose to play lable
    :param x: its x
    :param y: its y
    :param color: its color (in case you uses rect)
    :param buttons_text: the text of buttons on this lable (in each index for the next button)
    :param buttons_color: the color of buttons on this lable (in each index for the next button)
    :param buttons_function: the function of buttons on this lable (in each index for the next button)
    :param asker_username: the username of the one who asked the proposal or the address of it (the one that isn't the user)
    :param images: the images of buttons on this lable (in each double index,the image of its button and in each odd index, the onpose_img image of its button)
    :type x: float
    :type y: float
    :type color: (int,int,int)- RGB
    :type buttons_text: list of strings
    :type button_color: list of RGB-(int,int,int) colors
    :type buttons_function: functions
    :type asker_username: string
    :type images: list of pygame.surface"""
    def __init__(self, x, y, color, buttons_text, buttons_color, buttons_function, asker_username, images=None): #image in double indexes- button image, in odd indexes- button onpose_img
        self.x= x
        self.y= y
        self.color=color
        self.buttons_text= buttons_text
        self.buttons_color= buttons_color
        self.asker_username= asker_username

        #constants
        self.SIZE=(300,100)
        self.BUTTON_HIGH=50
        SPACES_BETWIN=10
        self.FONT = pygame.font.SysFont("Monotype Hadassah", 30)
        self.IMAGE= pygame.image.load("images/system image/game propose.png")
        self.IMAGE= pygame.transform.scale(self.IMAGE, self.SIZE)

        #fields for object work
        self.isActive=True
        self.buttons= []
        #placing the buttons
        button_size=((self.SIZE[0]-(len(buttons_text)+1)*SPACES_BETWIN)/len(buttons_text),self.BUTTON_HIGH)

        if images==None:
            images= ["None"]*(len(buttons_text)*2)
        for i in range(len(buttons_text)):
            self.buttons.append(button(buttons_function[i],(self.x+SPACES_BETWIN+button_size[0]*i ,self.y+(self.SIZE[1]-self.BUTTON_HIGH-10),button_size[0],button_size[1])
                   ,buttons_color[i] ,buttons_text[i], image= images[i*2], onpose_img= images[i*2+1]))

    def buttonYupdate(self):
        """update the y of the buttons of the buttons according to the y of this object"""
        for b in self.buttons:
            b.rect_tuple= (b.rect_tuple[0],self.y+(self.SIZE[1]-self.BUTTON_HIGH-10),b.rect_tuple[2],b.rect_tuple[3])
        

    def tick(self):
        """pass one frame for this object and drow it"""
        #pygame.draw.rect(global_var.screen, self.color, pygame.Rect(self.x,self.y, self.SIZE[0],self.SIZE[1]))
        global_var.screen.blit(self.IMAGE,(self.x,self.y))
        self.textPaint()
        self.buttonYupdate()

        for b in self.buttons:
            b.tick()

    def textPaint(self):
        """paint text (self.asker_username)"""
        text = self.FONT.render(self.asker_username, True, (186, 201, 0))
        textRect = text.get_rect()
        textRect.centerx= self.x+self.SIZE[0]/2
        textRect.y= self.y+5

        global_var.screen.blit(text,textRect)

    def __str__(self):
        return self.asker_username+"-"+ self.isActive

def proposalsYcorrect(lst,startY):
    """uppdate the list to delete all the elements that not active and aapdate there y so the will be the right emount of empty space between to lables
    :param lst: the list it need to update
    :param startY: the Y that supposed to be of the first lable at the end of this function running
    :type lst: list of gameProposal
    :type startY: float"""
    nextY= startY
    ls_copy= lst+[]
    lst_to_empty(lst)
    for a in ls_copy:
        a.y= nextY
        nextY+= a.SIZE[1]+10
        if a.isActive:
            lst.append(a)

def lst_to_empty(lst):
    """get list and delete from it any item except from index 0
    :param lst: the list to delete from it
    :type lst: list"""
    while len(lst)!=0:
        lst.pop(-1)

def send_ask():
    """send propose to play to someone"""
    global show_elart_self
    user= tEnter.get_text()
    
    if user== global_var.username:
        global_var.alert_data= ("can not challenge yourself",(600,10,320,100))
    else:
        sockF.sendMesegTCP(global_var.server_TCP_sock,"GAME|FRIEND GAME|"+user)
    tEnter.set_text("")

def main():
    """the code of this window. it's screen is in global_var.screen."""
    global done
    global choosedChar
    global chars
    global agreed
    global buttons
    global tEnter
    global fromMe_user_propse
    global toMe_user_propse
    global show_elart_self

    global_var.unconnected_exit_check("menu_before_playing.game_menu")

    sockF.sendMesegTCP(global_var.server_TCP_sock,"GAME|ENTER|game asks")
    
    done = False
    clock = pygame.time.Clock()
    
    font= pygame.font.SysFont("Algerian", 30)
    title_font= pygame.font.SysFont("Algerian", 50)
    PROPSES_FIRST_Y=100
    TOME_PRO_X=50
    FROMME_PRO_X=800
    ASK_SENT_ST_Y=400
    
    buttons=[button(lambda: toOtherFile("menu_before_playing.game_menu"),(1380,20,100,50),(255,0,0),"back")]
    gameProposalsToMe=[] #list of game proposal that arived to me
    toMe_user_propse= {} #dictionery in which the game proposal that arived to me are the key, and the username of the one who send it is the value
    gameProposalsFromMe=[] #list of game proposal that I sent
    fromMe_user_propse={} #dictionery in which the game proposal that I sent are the key, and the address is the value

    #asking objects
    Ptext= font.render("proposing to play", True, (186, 201, 0))
    PTEXT_P= (10,10+ASK_SENT_ST_Y)
    user_getting_text= font.render("username:", True, (186, 201, 0))
    USERTEXT_P= (10, PTEXT_P[1]+Ptext.get_rect().height+10)
    tEnter= textEnterens((10+user_getting_text.get_rect().width, USERTEXT_P[1],1000,50),(255,255,255))
    buttons.append(tEnter)
    B_SIZE= (150,75)
    buttons.append(button(send_ask, (800-B_SIZE[0], 660-B_SIZE[1], B_SIZE[0], B_SIZE[1]), (0,0,255), "send"))

    while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            
            global_var.for_menu_screen()
        
            #paint
            for g in gameProposalsToMe+gameProposalsFromMe:
                g.tick()

            s= pygame.Surface((1500,300))
            s.set_alpha(128)
            s.fill((0,0,255))
            global_var.screen.blit(s,(0,ASK_SENT_ST_Y))

            for b in buttons:
                b.tick()

            #server meseg handeling
            serverMsg= sockF.unpucketMasegTCP(global_var.server_TCP_sock)
            if serverMsg!="":
                serverMsg=serverMsg.split("|")
                print(serverMsg)
                if len(serverMsg)==2 and serverMsg[0]=="REFUSE":
                    user= serverMsg[1]
                    try:
                        fromMe_user_propse[user].isActive= False
                        fromMe_user_propse.pop(user)
                    except:
                        pass
                elif len(serverMsg)==2 and serverMsg[0]=="ACSEPT":
                    user= serverMsg[1]
                    isCorrect=True
                    try:
                        fromMe_user_propse[user]
                    except:
                        isCorrect=False
                    if isCorrect:
                        global_var.is_known_competitor= True
                        toOtherFile("menu_before_playing.char_choose.choose")
                elif len(serverMsg)==2 and serverMsg[0]=="CANCLE GAME":
                    user= serverMsg[1]
                    print("cencle",toMe_user_propse)
                    try:
                        toMe_user_propse[user].isActive= False
                        toMe_user_propse.pop(user)
                        print("done")
                    except:
                        pass
                elif len(serverMsg)==2 and serverMsg[0]=="ASK SENT":
                    user= serverMsg[1]
                    try:
                        fromMe_user_propse[user]
                    except:
                        gameProposalsFromMe.append(gameProposal(FROMME_PRO_X,-1000,(200,200,200),["cancel"],[(0,0,255)],
                                                  [lambdaFconstractor(cancleOnClick,user)],user))
                        fromMe_user_propse[user]= gameProposalsFromMe[-1]
                elif len(serverMsg)==1 and serverMsg[0]=="ANCORRECT ADDRESS WINDOW":
                    global_var.alert_data= ("friend isn't on this screen",(600,10,300,100))
                    print("your friend doesn't wating for you")
                elif len(serverMsg)==2 and serverMsg[0]=="FRIEND GAME":
                    user= serverMsg[1]
                    try:
                        toMe_user_propse[user]
                    except:
                        gameProposalsToMe.append(gameProposal(TOME_PRO_X,-1000,(200,200,200),["accept","refuse"],[(0,255,0),(255,0,0)], 
                                                  [lambdaFconstractor(acceptOnClick,user),lambdaFconstractor(refuseOnClick,user)],user,
                                                 [pygame.image.load("images/system image/accept.png"), pygame.image.load("images/system image/accept pushed.png"),
                                                  pygame.image.load("images/system image/refuse.png"), pygame.image.load("images/system image/refuse pushed.png")]))
                        toMe_user_propse[user]= gameProposalsToMe[-1]

            #peropose text creating
            text = font.render("proposed to me games", True, (140, 150, 0))
            global_var.screen.blit(text,(TOME_PRO_X,10))
            text = font.render("proposed by me games", True, (140, 150, 0))
            global_var.screen.blit(text,(FROMME_PRO_X,10))
            
            #Y correcting
            proposalsYcorrect(gameProposalsToMe, PROPSES_FIRST_Y)
            proposalsYcorrect(gameProposalsFromMe, PROPSES_FIRST_Y)

            #propose titeles blit
            global_var.screen.blit(Ptext, PTEXT_P)
            global_var.screen.blit(user_getting_text, USERTEXT_P)

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RETURN]:
                send_ask()


            global_var.before_menu_screen_display()
            pygame.display.flip()
            clock.tick(24)
            

if __name__=="__main__":
        main()
else:
        print(__name__)

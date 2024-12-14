import pygame
import global_var

class button:
    """button class
    :param onclick: the function that heppens when you click the button
    :param rect_tuple: the rect in which the button will be. it is in the following format (x,y,width,hight)
    :param color: the color of the button (in case you don't use image)
    :param text: the text on the button
    :param font: the font of the text in the button. if it None, it will turn into pygame.font.SysFont("Edwardian Script ITC", 60)
    :param image: the image of the button. if it None, solid filled rect will be used as button. if it "None", it will turn into the image in "images/system image/button.png".
    :param onpose_img: the image of the button when the mouse put on it. if it None, solid filled rect will be used as button. if it "None", it will turn into the image in "images/system image/clicked button.png".
    :param text_indent: text indentation related to the center
    :param onpose_text_indent: text indentation related to the center when the mouse on the button
    :type onclick: function
    :type rect_tuple: (float,float,float,float)
    :type color: (int,int,int)-RGB
    :type text: string
    :type font: pygame.font
    :type image: pygame.surface
    :type onpose_img: pygame.surface"""
    def __init__(self,onclick,rect_tuple,color,text="",font=None,image="None", onpose_img= "None",text_indent=(0,0),onpose_text_indent=(0,0),t_color= (186, 201, 0)):
        #rect_tuple corectens to in (in case it had arguments that are floot)
        rect_tuple= (int(rect_tuple[0]), int(rect_tuple[1]), int(rect_tuple[2]), int(rect_tuple[3]))
        #onpose_img- the image when your mouse on the button
        self.onclick=onclick
        self.rect_tuple=rect_tuple
        self.color=color
        self.text=text
        self.font=font
        self.text_indent=text_indent
        self.onpose_text_indent=onpose_text_indent
        if font==None:
            self.font = pygame.font.SysFont("Edwardian Script ITC", 60)

        self.image=image
        if image=="None":
            self.image= pygame.image.load("images/system image/button.png")
        
        if image!=None:
            self.image= pygame.transform.scale(self.image, (rect_tuple[2],rect_tuple[3]))
            
        self.onpose_img= onpose_img
        if onpose_img=="None":
            self.onpose_img= pygame.image.load("images/system image/clicked button.png")
        
        if onpose_img!=None:
            self.onpose_img= pygame.transform.scale(self.onpose_img, (rect_tuple[2],rect_tuple[3]))

        self.clicked=False
        self.t_color = t_color
    def tick(self):
        """pass 1 frame for this button and paint it"""
        self.paint()
        mp=pygame.mouse.get_pos()
        if self.rect_tuple[0]<mp[0]<self.rect_tuple[0]+self.rect_tuple[2]:
            if self.rect_tuple[1]<mp[1]<self.rect_tuple[1]+self.rect_tuple[3]:
                if pygame.mouse.get_pressed()[0]:
                    self.clicked=True
                elif self.clicked:
                    self.clicked=False
                    self.onclick()
                    
    def set_onpose_img(self, img):
        """chenge the onpose_img including the exceptions (if onpose_img is None)
        :param img: the given image
        :type img: pygame.surface"""
        self.onpose_img= img
        if img!=None:
            self.onpose_img= pygame.transform.scale(img, (self.rect_tuple[2],self.rect_tuple[3]))

    def set_img(self, img):
        """chenge the image including the exceptions (if image is None)
        :param img: the given image
        :type img: pygame.surface"""
        self.image=img
        if img!=None:
            self.image= pygame.transform.scale(img, (self.rect_tuple[2],self.rect_tuple[3]))
    
    def paint(self):
        """paint the button"""
        mp=pygame.mouse.get_pos()
        #rect
        if self.image==None:
            pygame.draw.rect(global_var.screen, self.color, pygame.Rect(self.rect_tuple))
        
        #image
        if self.image!=None:
            img= self.image
            if self.rect_tuple[0]<mp[0]<self.rect_tuple[0]+self.rect_tuple[2] and self.rect_tuple[1]<mp[1]<self.rect_tuple[1]+self.rect_tuple[3] and self.onpose_img!=None:
                img= self.onpose_img
            global_var.screen.blit(img,(self.rect_tuple[0],self.rect_tuple[1]))
        #text
        text = self.font.render(self.text, True, self.t_color)
        textRect = text.get_rect()
        textRect.center=(self.rect_tuple[0]+self.rect_tuple[2]/2,self.rect_tuple[1]+self.rect_tuple[3]/2)
        if self.rect_tuple[0]<mp[0]<self.rect_tuple[0]+self.rect_tuple[2] and self.rect_tuple[1]<mp[1]<self.rect_tuple[1]+self.rect_tuple[3] and self.onpose_img!=None:
            point=(textRect.x+self.onpose_text_indent[0], textRect.y+self.onpose_text_indent[1])
        else:
            point=(textRect.x+self.text_indent[0], textRect.y+self.text_indent[1])
        global_var.screen.blit(text,point)


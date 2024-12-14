import global_var
import pygame

class roling_page:
    #NOTE: button so this window will reference to wheel rotate only when it was clicked may be needed in the futer 
    def __init__(self,visible_rect,roling_w,img):
        #img is surface
        self.page_roller= page_rolling(visible_rect[3],roling_w,0,(visible_rect[0]+visible_rect[2],visible_rect[1]))
        self.visible_rect= visible_rect
        self.img= img.convert_alpha()
        if self.img.get_width()>visible_rect[2]:
            print("unfull image")

    def wheel_roll(self,y):
        #called during pygame.MOUSEWHEEL event
        self.page_roller.wheel_roll(-y)
        
    def tick(self):
        self.page_roller.tick()

        #painting
        rect_surface = self.img.subsurface(0,((self.img.get_height()-self.visible_rect[3])*max(min(self.page_roller.get_prossent(),0.99999999),0.000000001)),
                                         min(self.visible_rect[2],self.img.get_width()),min(self.visible_rect[3],self.img.get_height()))
        global_var.screen.blit(rect_surface,(self.visible_rect[0],self.visible_rect[1]))
        

class page_rolling:
    """line in which you can mark prosent (by moving rect along the line)
    :param length: the length of the line
    :param start_prossent: the diffult prosent (before the user moves the rect) that this sows. assume that 0<=start_prossent<=1
    :param place: the point of the left center of the line
    :param line_img: the image of the line. if it None, solid filled rect will be used as line. if it "None", it will turn into the image in "images/system image/button.png".
    :param corsor_img: the image of the line. if it None, solid filled rect will be used as corsor. if it "None", it will turn into the image in "images/system image/button.png".
    :type length: float
    :type start_prossent: float
    :type place: (float,float)"""
    def __init__(self,length,w,start_prossent,place,corsor_img="None",line_img="None"):
        self.L= length
        self.place= place

        self.W= w
        self.CORSOR_L_PROCENT= 0.1
        self.rect= (place[0],place[1],self.W, self.L)
        self.corsor_size= (self.W,self.L*self.CORSOR_L_PROCENT)
        self.corrsor= (place[0], place[1]+(self.L-self.corsor_size[1])*start_prossent, self.corsor_size[0],self.corsor_size[1])
        self.is_pressed= False

        self.corrsor_img= corsor_img
        if corsor_img=="None":
            self.corsor_img= rect_to_line((w, self.corsor_size[1]),(50,50,50))
        if corsor_img!=None:
            self.corsor_img= pygame.transform.scale(self.corsor_img, self.corsor_size)

        self.line_img= line_img
        if line_img=="None":
            self.line_img= rect_to_line((w, length),(128,128,128,128))
        if line_img!=None:
            self.line_img= pygame.transform.scale(self.line_img, (w, self.L))

    
    def press_check(self):
        """check does the cursor presed"""
        mp=pygame.mouse.get_pos()
        if self.corrsor[0]<mp[0]<self.corrsor[0]+self.corrsor[2]:
            if self.corrsor[1]<mp[1]<self.corrsor[1]+self.corrsor[3]:
                self.is_pressed= pygame.mouse.get_pressed()[0]
                
        if not pygame.mouse.get_pressed()[0]:
            self.is_pressed= False
        

    def tick(self):
        """pass one frame to this object and paint it"""
        if self.is_pressed:
            mp=pygame.mouse.get_pos()
            #print(max(mp[1]-self.corsor_size[1]/2,self.place[1]),self.place[1]+self.L-self.corsor_size[1])
            self.corrsor=(self.corrsor[0],min(max(mp[1]-self.corsor_size[1]/2,self.place[1]),self.place[1]+self.L-self.corsor_size[1]),self.corrsor[2],self.corrsor[3])
        self.press_check()

        self.paint()

    def wheel_roll(self,y):
        self.corrsor=(self.corrsor[0],min(max(self.corrsor[1]+ y*2,self.place[1]),self.place[1]+self.L-self.corsor_size[1]),self.corrsor[2],self.corrsor[3])

    def paint(self):
        """paint the object"""
        if self.line_img==None:
            pygame.draw.rect(global_var.screen, (100,100,100), pygame.Rect(self.rect))
        else:
            global_var.screen.blit(self.line_img,(self.rect[0],self.rect[1]))

        if self.corrsor_img==None:
            pygame.draw.rect(global_var.screen, (200,200,200), pygame.Rect(self.corrsor))
        else:
            global_var.screen.blit(self.corsor_img,(self.corrsor[0],self.corrsor[1]))

    def get_prossent(self):
        """get in which prosent is the corrsor"""
        return (self.corrsor[1]-self.place[1])/(self.L-self.corrsor[3])

def rect_to_line(size,color):
    surface= pygame.image.load("images/about us/blank_surface.PNG")
    surface= pygame.transform.scale(surface, size)
    draw_circle_end_line(surface, color, (size[0]/2,size[0]/2),(size[0]/2,size[1]-size[0]/2),size[0])
    if len(color)==4:
        surface.set_alpha(color[3])
    return surface

def draw_circle_end_line(surface,color,start,end,w):
    pygame.draw.line(surface,color,start,end,w)
    pygame.draw.circle(surface,color,start,w/2)
    pygame.draw.circle(surface,color,end,w/2)

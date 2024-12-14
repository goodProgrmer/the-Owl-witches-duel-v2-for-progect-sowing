import global_var
import pygame

class prossent_line:
    """line in which you can mark prosent (by moving rect along the line)
    :param length: the length of the line
    :param start_prossent: the diffult prosent (before the user moves the rect) that this sows. assume that 0<=start_prossent<=1
    :param place: the point of the left center of the line
    :param line_img: the image of the line. if it None, solid filled rect will be used as line. if it "None", it will turn into the image in "images/system image/button.png".
    :param corsor_img: the image of the line. if it None, solid filled rect will be used as corsor. if it "None", it will turn into the image in "images/system image/button.png".
    :type length: float
    :type start_prossent: float
    :type place: (float,float)"""
    def __init__(self,length,start_prossent,place, orientation="horizontal",corsor_img="None",line_img="None"):
        self.L= length
        self.place= place

        self.H=20
        self.rect= (place[0],place[1]-self.H/2,self.L, self.H)
        self.corsor_size= (40,50)
        self.corrsor= (place[0]+self.L*start_prossent-self.corsor_size[0]/2, place[1], self.corsor_size[0],self.corsor_size[1])
        self.is_pressed= False

        self.corrsor_img= corsor_img
        if corsor_img=="None":
            self.corsor_img= pygame.image.load("images/system image/corsor.png")
        if corsor_img!=None:
            self.corsor_img= pygame.transform.scale(self.corsor_img, self.corsor_size)

        self.line_img= line_img
        if line_img=="None":
            self.line_img= pygame.image.load("images/system image/prosent line.png")
        if line_img!=None:
            self.line_img= pygame.transform.scale(self.line_img, (self.L, self.H))
    
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
            self.corrsor=(min(max(mp[0],self.place[0]),self.place[0]+self.L)-self.corsor_size[0]/2,self.corrsor[1],self.corrsor[2],self.corrsor[3])
        self.press_check()

        self.paint()

    def paint(self):
        """paint the object"""
        if self.line_img==None:
            pygame.draw.rect(global_var.screen, (100,100,100), pygame.Rect(self.rect))
        else:
            global_var.screen.blit(self.line_img,(self.rect[0],self.rect[1]))
        
        if self.corsor_img==None:
            pygame.draw.rect(global_var.screen, (200,200,200), pygame.Rect(self.corrsor))
        else:
            global_var.screen.blit(self.corsor_img,(self.corrsor[0],self.corrsor[1]))

    def get_prossent(self):
        """get in which prosent is the corrsor"""
        return (self.corrsor[0]+self.corrsor[2]/2-self.place[0])/self.L
        

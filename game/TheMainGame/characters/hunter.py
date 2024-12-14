from TheMainGame.characters.absCaracter import*
from math import*
import random
import TheMainGame.for_commands_sending.sounds as sounds

class hunter(absCaracter):
    """game charcter: hunter
    :param screen: pointer to the screen
    :param pNum: the number of the character (1 or 2)
    :type screen: pygame.surface
    :type pNum: int"""
    def __init__(self,screen,pNum):
        super().__init__(screen,pNum,hanterMovinator(self),[1,4,2,3,5])

        #parameters for quick change
        self.telportDistens=300
        self.times= [-200,0,-200,0,-200]
        
        #[0]- time of last op1 activate
        #[1]- time from last op2 activate (0 if you can activ it now)
        #[2]- time of last op3 activate
        #[3]- time from last op3 activate (0 if you can activ it now)

        self.isFromTick=False
        self.powerP=100
        self.powerPgenerateV=0.2

    def tick(self):
        self.isFromTick=True
        
        super().tick()
        #adds
        if self.times[1]!=0:
            self.op2()

        if self.times[3]!=0:
            self.op4()

        if self.powerP+self.powerPgenerateV<=100:
            self.powerP+=self.powerPgenerateV
        
        #print(self.lookDirection)
        
        self.isFromTick=False

    def paramPaint(self):
        super().paramPaint()
        #powerP paint
        powerPPos=(120,50) #powerP display posizion for player 1
        powerPWid=100 #powerP display width
        if self.pNum==1:
            blitIncription(prosentRestIncription(self.powerP,powerPWid,20,(100,100,100)),powerPPos)
        else:
            blitIncription(prosentRestIncription(self.powerP,powerPWid,20,(100,100,100)),(self.screen.get_width()-powerPPos[0]-powerPWid,powerPPos[1]))
    def op1(self):
        """teleport forword"""
        
        if self.timeFromStart-self.times[0]>30:
            lastComands=["jump","moveP","moveN","down"]
            teleport=[(0,-self.telportDistens),(self.telportDistens,0),(-self.telportDistens,0),(0,self.telportDistens)]
            for i in range(len(lastComands)):
                if lastComands[i]==self.lastComand:
                    self.movinator.teleport_init()
                    self.x+=teleport[i][0]
                    self.y+=teleport[i][1]
                    self.times[0]=self.timeFromStart
    def op2(self):
        """kik operation"""
        kw=20 #kik width
        kh=20 #kik high
        kt=6 #kik time
        
        
        blastSize=10
        if self.times[1]==0:
            self.times[1]=1
            if self.lookDirection!="":
                self.movinator.kik_init()
            return
        if self.isFromTick:
            if self.times[1]==kt:
                self.times[1]=-10
                return
            if self.times[1]>0:
                if self.lookDirection=="moveN":
                    kx=self.x-(1-abs(1-self.times[1]/(kt/2)))*kw
                    ky=self.y+self.size[1]/2-kh/2
                    blastDir=(-10,0) #blast direction
                    kd=2 #kik damage
                elif self.lookDirection=="moveP":
                    kx=self.x+self.size[0]-kw+(1-abs(1-self.times[1]/(kt/2)))*kw
                    ky=self.y+self.size[1]/2-kh/2
                    blastDir=(10,0)
                    kd=2 #kik damage
                elif self.lookDirection=="jump":
                    kw,kh=kh,kw
                    ky=self.y-(1-abs(1-self.times[1]/(kt/2)))*kh
                    kx=self.x+self.size[0]/2-kw/2
                    blastDir=(0,-10)
                    kd=2 #kik damage
                elif self.lookDirection=="down":
                    kw,kh=kh,kw
                    ky=self.y+self.size[1]-kh+(1-abs(1-self.times[1]/(kt/2)))*kh
                    kx=self.x+self.size[0]/2-kw/2
                    blastDir=(0,10)
                    kd=4 #kik damage
                else:
                    self.times[1]=0
                    return
                if self.display_rects:
                    rectDrewIncription((0,255,0),(kx,ky,kw,kh),3)
                self.restHitEnemies(blastDir,kd,(kx,ky,kw,kh))
            self.times[1]+=1
            #if min(self.enemy.x+self.enemy.size[0])
            
    def op3(self):
        """teleport in front of the enemy"""
        
        distFromEnemy=250
        speedForword=20
        if self.timeFromStart-self.times[2]>30:
            lastComands=["jump","moveP","moveN","down"]
            teleport=[(0,distFromEnemy,0,-speedForword),(-distFromEnemy,0,speedForword,0),(distFromEnemy,0,-speedForword,0),(0,-distFromEnemy,0,-speedForword)] #(xdist,ydist,vx,vy)
            enemyX=random.choice(self.enemy.semyObjects).get_aiming_x()
            enemyY=random.choice(self.enemy.semyObjects).get_aiming_y()
            for i in range(len(lastComands)):
                if lastComands[i]==self.lastComand and (i!=0 or self.enemy.y+self.enemy.size[1]<self.floorLevel-100):
                    self.movinator.teleport_init()
                    self.x=teleport[i][0]+enemyX
                    self.y=teleport[i][1]+enemyY
                    self.vx=teleport[i][2]
                    self.vy=teleport[i][3]
                    self.times[2]=self.timeFromStart

    def op4(self):
        """floor hand kik"""
        kw=70 #kik width
        kh=200 #kik high
        kt=30 #kik time
        warningT=10
        blastSize=10
        powerPprice=50
        if self.times[3]==0 and self.powerP>=powerPprice:
            self.times[3]=1
            self.groundKikX=random.choice(self.enemy.semyObjects).get_aiming_x()
            self.powerP-=powerPprice
            self.movinator.groundKik_init()
            return
        if self.isFromTick:
            if self.times[3]==kt+warningT:
                self.times[3]=-10
                return
            if self.times[3]>0:
                kx=self.groundKikX-kw/2+self.enemy.size[0]/2
                ky=self.floorLevel-(1-(1+(warningT/kt))*abs(1-self.times[3]/((kt+warningT)/2)))*kh
                blastDir=(0,-10)
                kd=2
                if self.display_rects:
                    rectDrewIncription((0,255,0),(kx,ky,kw,kh))
                imgSize= TheMainGame.datafiles.imeges.imegesDict["hanter/ground_hand"].get_size()
                blitIncription("hanter/ground_hand",(kx+kw/2-imgSize[0]/2,ky))
                imgSize= TheMainGame.datafiles.imeges.imegesDict["hanter/hill"].get_size()
                blitIncription("hanter/hill",(kx+kw/2-imgSize[0]/2, self.floorLevel-imgSize[1]))
                self.restHitEnemies(blastDir,kd,(kx,ky,kw,kh))
            self.times[3]+=1
    def op5(self):
        """ricochet shots shoot operation"""
        powerPprice=50
        
        if self.timeFromStart-self.times[4]>10 and self.powerP>=powerPprice and (self.lookDirection in ["moveN","moveP","down"]):
            self.movinator.lightning_init()
            self.powerP-=powerPprice
            self.times[4]=self.timeFromStart
            if self.lookDirection=="moveN":
                self.recothetShot(180,135,10)
            elif self.lookDirection=="moveP":
                self.recothetShot(0,45,10)
            elif self.lookDirection=="down":
                self.recothetShot(135,45,10)
            else:
                self.times[1]=0
                return
            #self.arrows.append(recotionErrow(self.x+self.size[0]/2,self.y+self.size[1]/2,[self.enemy],100,0*pi/180,100,20,self.floorLevel,100,1400,100,1,self.screen))


    def recothetShot(self,startAngle,endAngle,shotNum):
        """"shooting ricochet shots"""
        #assume that shotNum>=2
        for i in range(shotNum):
            self.tickAbleAppend(recotionErrow(self.x+self.size[0]/2,self.y+self.size[1]/2,self.enemy,(startAngle+((endAngle-startAngle)/(shotNum-1))*i)*pi/180,
                                             100,20,self.floorLevel,100,1400,40,5,100))

class hanterMovinator(absMovinator):
    """hanter's movinator
    :param character: its character
    :type character: absCaracter"""
    def __init__(self,charcter):
        rectsize=(100,100)
        color=(255,0,0)
        self.opT=0
        super().__init__(color,rectsize,"hanter",charcter)
        self.opData= None # any data (asid from self.opT) that will pass from op init to the op, will be stored hir

    def teleport_init(self):
        """start the animation of teleport"""
        self.op= self.teleport
        self.opT= self.t
        self.opData= (self.c.x, self.c.y) #will store from wich point, was the teleport done
        sounds.put("TheMainGame/sounds/hunter/teleport.mp3", self.c.pNum)

    def teleport(self):
        """playing the animation of teleportinging"""
        image= self.getFrame("hanter/teleport",self.t-self.opT,10000)
        try:
            TheMainGame.datafiles.imeges.img_indentation[image]
            self.image=image
            blitIncription(image,self.opData)
        except:
            self.op= None

    def kik_init(self):
        """start the animation of kik"""
        self.op= self.kik
        self.opT= self.t
        #self.opData will not store nothing
    
    def kik(self):
        """playing the animation of kiking"""
        directory="hanter/kikN"
        if self.c.lookDirection=="moveP":
            directory="hanter/kikP"
        elif self.c.lookDirection=="jump":
            directory="hanter/kikU"
        elif self.c.lookDirection=="down":
            directory="hanter/kikD"
        image= self.getFrame(directory,self.t-self.opT,10000)
        try:
            TheMainGame.datafiles.imeges.img_indentation[image]
            self.image=image
        except:
            self.op= None

    def lightning_init(self):
        """start the animation of shooting ricochet errows"""
        self.op= self.lightning
        self.opT= self.t
        #self.opData will store the directory of lightning in the right direction
        self.opData="hanter/lightningN"
        if self.c.xDirection=="moveP":
            self.opData="hanter/lightningP"
    
    def lightning(self):
        """playing the animation of shooring recochet errows"""
        image= self.getFrame(self.opData, self.t-self.opT,10000)
        try:
            TheMainGame.datafiles.imeges.img_indentation[image]
            self.image=image
        except:
            self.op= None

    def groundKik_init(self):
        """start the animation of kik from ground"""
        self.ops= self.groundKik
        self.opT= self.t
        #self.opData will not store nothing
    
    def groundKik(self):
        """playing the animation of kik from ground"""
        image= self.getFrame("hanter/ground kik",self.t-self.opT,10000)
        try:
            TheMainGame.datafiles.imeges.img_indentation[image]
            self.image=image
        except:
            self.op= None
    

class recotionErrow(absErrow):
    """recochet errow"""
    def TochingWalls(self):
        if self.y+self.L*sin(self.a)>self.fl:
            self.y=self.fl
            self.x=self.x+self.L*cos(self.a)
            self.a*=-1
            
        if self.x+self.L*cos(self.a)<self.lW:
            self.y=self.y+self.L*sin(self.a)
            self.x=self.lW
            self.a=pi-self.a

        if self.x+self.L*cos(self.a)>self.rW:
            self.y=self.y+self.L*sin(self.a)
            self.x=self.rW
            self.a=pi-self.a
        
            
        

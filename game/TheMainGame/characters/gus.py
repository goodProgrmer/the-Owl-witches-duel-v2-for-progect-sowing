from TheMainGame.characters.absCaracter import*
from math import*
import random

class gus(absCaracter):
    """gus game character
    :param screen: pointer to the screen
    :param pNum: the number of the character (1 or 2)
    :type screen: pygame.surface
    :type pNum: int"""
    def __init__(self,screen,pNum):
        super().__init__(screen,pNum,gusMovinator(self),[2,4,1,5,3])

        #parameters for quick change
        self.telportDistens=200
        self.times= [-20,-20,-20,-20,-20]
        
        #[0]- the last time when op1 was active
        #[1]- the last time when op2 was active (it can be more than the curent time to indicate that it is active now and the enemy need to see gus antil this time)
        #[2]- the last time when op3 was active 
        #[3]- the last time when op4 was active 

        self.isFromTick=False
        self.lookDirection="moveN"
        self.powerP=100
        self.powerPgenerateV=0.2
        self.flyingP=100
        self.flyingPgenerateV=0.2
        self.is_flying=False

    def tick(self):
        self.isFromTick=True

        #kikDirection update
        if self.lastComand in ["jump","moveP","moveN","down"]:
                self.lookDirection=self.lastComand
        
        super().tick()

        if self.powerP+self.powerPgenerateV<=100:
            self.powerP+=self.powerPgenerateV

        if self.flyingP+self.flyingPgenerateV<=100:
            self.flyingP+=self.flyingPgenerateV

        if self.times[0]!=0:
            self.op1()

        if self.is_flying:
            self.op5()
        
        self.isFromTick=False
    def paint(self):
        playersWisebility=[True,True] #playersWisebility[0]- is player 1 can see the params. playersWisebility[1]- is player 2 can see the params
        if 0<=self.timeFromStart-self.times[1]<2:
            playersWisebility=[False,False]
            playersWisebility[self.pNum-1]=True
        super().paint(playersWisebility[0],playersWisebility[1])
        
    def paramPaint(self):
        playersWisebility=[True,True] #playersWisebility[0]- is player 1 can see the params. playersWisebility[1]- is player 2 can see the params
        if self.timeFromStart-self.times[1]<2:
            playersWisebility=[False,False]
            playersWisebility[self.pNum-1]=True
            rectColor=(0,0,0)
            if self.timeFromStart-self.times[2]<2:
                rectColor=(255,255,255)
            if self.pNum==1:
                rectDrewIncription(rectColor,(120,110,50,20),0,playersWisebility[0], playersWisebility[1])
            else:
                rectDrewIncription(rectColor,(self.screen.get_width()-120-50,110,50,20),0, playersWisebility[0], playersWisebility[1])
        super().paramPaint(playersWisebility[0],playersWisebility[1])
        #powerP paint
        powerPPos=(120,50) #powerP display posizion for player 1
        powerPWid=100 #powerP display width
        if self.pNum==1:
            blitIncription(prosentRestIncription(self.powerP,powerPWid,20,(0,0,255)),powerPPos,playersWisebility[0],playersWisebility[1])
        else:
            blitIncription(prosentRestIncription(self.powerP,powerPWid,20,(0,0,255)),(self.screen.get_width()-powerPPos[0]-powerPWid,powerPPos[1]),playersWisebility[0],playersWisebility[1])

        font = pygame.font.SysFont("Algerian", 13)
        text= font.render("consentration", True, (0, 128, 0))
        textRect = text.get_rect()
        if self.pNum==1:
            textRect.center= (powerPPos[0]+powerPWid/2, powerPPos[1]+9)
        else:
            textRect.center= (self.screen.get_width()-powerPPos[0]-powerPWid/2, powerPPos[1]+9)

        blitIncription(textDrawIncription("Algerian", 13,"consentration",(186, 201, 0)),textRect.topleft,playersWisebility[0],playersWisebility[1])

        flyingPPos=(120,80) #powerP display posizion for player 1
        flyingPWid=100 #powerP display width
        if self.pNum==1:
            blitIncription(prosentRestIncription(self.flyingP,flyingPWid,20,(255,0,0)),flyingPPos,playersWisebility[0],playersWisebility[1])
        else:
            blitIncription(prosentRestIncription(self.flyingP,flyingPWid,20,(255,0,0)),(self.screen.get_width()-flyingPPos[0]-powerPWid,flyingPPos[1]),playersWisebility[0],playersWisebility[1])

    def op1(self):
        """kik operation"""
        kw=40 #kik width
        kh=20 #kik high
        kt=15 #kik time
        
        
        blastSize=10
        if self.times[0]==0:
            self.times[0]=1
            self.movinator.kik_init(kt)
            return
        if self.isFromTick:
            if self.times[0]==kt:
                self.times[0]=-10
                return
            if self.times[0]>0:
                if self.lookDirection=="moveN":
                    kx=self.x-(1-abs(1-self.times[0]/(kt/2)))*kw
                    ky=self.y+self.size[1]/2-kh/2
                    blastDir=(-10,0) #blast direction
                    kd=2 #kik damage
                elif self.lookDirection=="moveP":
                    kx=self.x+self.size[0]-kw+(1-abs(1-self.times[0]/(kt/2)))*kw
                    ky=self.y+self.size[1]/2-kh/2
                    blastDir=(10,0)
                    kd=2 #kik damage
                else:
                    self.times[0]=0
                    return
                
                if self.display_rects:
                    rectDrewIncription((0,255,0),(kx,ky,kw,kh),3)
                self.restHitEnemies(blastDir,kd,(kx,ky,kw,kh))
            self.times[0]+=1
            
    def op2(self):
        """turn enemy screen to black"""
        if self.powerP>0:
            self.times[1]=max(self.timeFromStart,self.times[1])
            if random.random()>0.99:
                self.times[1]+=15
            self.powerP-=self.powerPgenerateV+0.2
            setIncriptionStr(self.pNum%2,"RDUZ|(0,0,0)|0|("+str(self.screen.get_width())+","+str(self.screen.get_height())+")|(0,0)\n"+getIncriptionStr(self.pNum%2))            
    def op3(self):
        """make every paramter from enemy screen and gus to disappire (on enemy screen)"""
        if self.powerP>1:
            self.times[2]=self.timeFromStart #will be consider in beforeSending function
            self.powerP-=self.powerPgenerateV+0.2
            self.op2()

    def op4(self):
        """create a lot of duplices of itself"""
        pPowerCost=50

        spread= 200
        if self.timeFromStart-self.times[3]>20 and self.powerP>=pPowerCost:
            self.movinator.appear_init()
            self.times[3]=self.timeFromStart
            self.powerP-=pPowerCost
            for i in range(20):
                self.tickAbleAppend(gusBott(self.screen,self,self.x+random.randrange(-spread,spread),self.y+random.randrange(-spread,spread),self.vx,self.vy))
                self.semyObjects.append(self.tickAbleCreatedObjects[-1])
    def op5(self):
        """fly/unfly operation"""
        flyingP_per_frame=1
        if self.isFromTick and self.flyingP>=flyingP_per_frame:
            self.flyingP-=flyingP_per_frame
            #y axis friction append
            if self.vy>0:
                self.ay=-self.friction
            elif self.vy<0:
                self.ay=self.friction
        elif self.timeFromStart-self.times[4]>20 or self.flyingP<flyingP_per_frame:
            if self.is_flying:
                self.movinator.dis_fly_init()
                self.ay=self.G
                self.is_flying=False
            else:
                self.movinator.fly_init()
                self.ay=0
                self.is_flying=True
            self.times[4]=self.timeFromStart

    def jump(self):
        if self.is_flying:
            if self.stantimer!=0:
                return
            if -self.move_v<=self.vy<0.1:
                self.vy=-self.move_v*2
            self.lastComand="jump"
        else:
            super().jump()
            
    def down(self):
        if self.is_flying:
            if self.stantimer!=0:
                return
            if self.move_v>=self.vy>-0.1:
                self.vy=self.move_v*2
            self.lastComand="down"
        else:
            super().down()
            
    def moveP(self):
        if self.is_flying:
            if self.stantimer!=0:
                return
            self.ax=3+self.friction
            self.lastComand="moveP"
        else:
            super().moveP()

    def moveN(self):
        if self.is_flying:
            if self.stantimer!=0:
                return
            self.ax=-3-self.friction
            self.lastComand="moveN"
        else:
            super().moveN()

    def get_aiming_x(self):
        if self.is_show_rand_place():
            return random.randint(0,self.screen.get_width()-self.size[1])
        return super().get_aiming_x()

    def get_aiming_y(self):
        if self.is_show_rand_place():
            return random.randint(0,self.screen.get_height()-self.size[0])
        return super().get_aiming_y()

    def is_show_rand_place(self):
        """return does the enemy character supposed to know it's place
        :return: does the enemy character supposed to know it's place
        :rtype: boolean"""
        return 0<=self.timeFromStart-self.times[1]<2 or self.timeFromStart-self.times[2]<2

    def beforeSending(self):
        if self.timeFromStart-self.times[2]<2:
            setIncriptionStr(self.pNum%2,"")
            self.enemy.paint()

class gusMovinator(absMovinator):
    """gus's movinator
    :param character: its character
    :type character: absCaracter"""
    def __init__(self,charcter):
        rectsize=(100,100)
        color=(0, 0, 255)
        super().__init__(color,rectsize,"gus",charcter)

    def kik_init(self,t):
        """start the animation of kik
        :param t: the time that kiking animation supposed to take
        :type t: int"""
        if self.op in [None, self.kik]:
            self.op= self.kik
            self.opT= self.t
            #self.opData will store the length (in frames) of the kik
            self.data= t
    
    def kik(self):
        """playing the animation of kiking"""
        if self.t-self.opT<self.data:
            self.image="gus/charImg/kikN"
            if self.c.xDirection=="moveP":
                self.image="gus/charImg/kikP"
        else:
            self.op= None

    def appear_init(self):
        """start the animation of appiring"""
        self.op= self.appear
        self.opT= self.t
        #self.opData will store the start point of the character
        self.opData= (self.c.x,self.c.y)
    
    def appear(self):
        """playing the animation of appearing"""
        directory="gus/appear"
        image= self.getFrame(directory,(self.t-self.opT)//2,10000)
        self.c.vx=0
        self.c.vy=0
        self.c.x, self.c.y= self.opData
        try:
            TheMainGame.datafiles.imeges.img_indentation[image]
            self.image=image
        except:
            self.op= None

    def disappear_init(self):
        """start the animation of disappearing"""
        #only for gus bots
        self.op= self.disappear
        self.opT= self.t
        #self.opData will store the start point of the character
        self.opData= (self.c.x,self.c.y)
        self.c.activator.supporters.remove(self.c) #he isn't supporter,so he cant be hitted
        self.c.hp=0
    
    def disappear(self):
        """playing the animation of disappearing"""
        directory="gus/disappear"
        image= self.getFrame(directory,(self.t-self.opT)//2,10000)
        self.c.vx=0
        self.c.vy=0
        self.c.x, self.c.y= self.opData
        try:
            TheMainGame.datafiles.imeges.img_indentation[image]
            self.image=image
        except:
            self.op= None
            self.c.isActive=False

    def fly_init(self):
        """start the animation of flying"""
        self.op= self.fly
        self.opT= self.t
        #self.opData will store nothing
    
    def fly(self):
        """playing the animation of flying"""
        directory="gus/flyN"
        if self.c.xDirection=="moveP":
            directory="gus/flyP"
        image= self.getFrame(directory,(self.t-self.opT)//1,10000)
        try:
            TheMainGame.datafiles.imeges.img_indentation[image]
            self.image=image
        except:
            self.op= self.flying

    def dis_fly_init(self):
        """start the animation of disflying"""
        self.op= self.dis_fly
        self.opT= self.t
        #self.opData will store nothing
    
    def dis_fly(self):
        """playing the animation of disflying"""
        directory="gus/dis_flyN"
        if self.c.xDirection=="moveP":
            directory="gus/dis_flyP"
        image= self.getFrame(directory,(self.t-self.opT)//1,10000)
        try:
            TheMainGame.datafiles.imeges.img_indentation[image]
            self.image=image
        except:
            self.op= None

    def flying(self):
        """uctive while gus flying (after the animation)"""
        self.image="gus/charImg/flyN"
        if self.c.xDirection=="moveP":
            self.image="gus/charImg/flyP"
            

class gusBott(absCaracter):
    """gus bot character (the one that made to mislead the enemy). this character moves in random way
    :param screen: the game screen
    :param activator: the object that created it
    :param x: character x
    :param y: character y
    :param vx: character v in x axis
    :param vy: character v in y axis
    :type screen: pygame.surface
    :type activator: absCharacter
    :type x: flout
    :type y: flout
    :type vx: flout
    :type vy: flout"""
    def __init__(self,screen,activator,x,y,vx,vy):
        super().__init__(screen,1,gusMovinator(self))
        self.activator=activator
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy

        #for bot playing
        self.moveDirection=self.moveDerectionChoise()
        #uppiring
        self.movinator.appear_init()

    def paramPaint(self):
        pass
    def winningCheck(self):
        pass

    def hit(self,blast,damage,stan=0):
        self.stantimer=10
        self.hp-=damage*1000000

    def tick(self):
        self.gusBottPlay()
        if self.hp<0:
            self.movinator.disappear_init()

        super().tick()

    #for bot playing
    def gusBottPlay(self):
        """gusBot bot play (in random way)"""
        #disiding do it need to cheng move direction
        if random.random()>0.98:
            #disiding to which direction to move
            self.moveDirection=self.moveDerectionChoise()

        #move in the chosen direction
        if self.moveDirection!=None:
            self.moveDirection()

        #diside is it need to jump and do it
        
        if random.random()>0.96:
            self.jump()

    def moveDerectionChoise(self):
        """choose move direction in x axis in random way.
        :return: function to move in the direction it desided
        :rtype: function pointer"""
        choisesLst=[self.moveN,None,self.moveP]
        return random.choice(choisesLst)

    def get_aiming_x(self):
        if self.activator.is_show_rand_place():
            return random.randint(0,self.screen.get_width()-self.size[1])
        return super().get_aiming_x()
    
    def get_aiming_y(self):
        if self.activator.is_show_rand_place():
            return random.randint(0,self.screen.get_height()-self.size[0])
        return super().get_aiming_x()


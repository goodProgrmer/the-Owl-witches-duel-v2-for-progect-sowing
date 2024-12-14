from TheMainGame.characters.absCaracter import*
from math import*
from random import*

class emity(absCaracter):
    """game charcter: emity
    :param screen: pointer to the screen
    :param pNum: the number of the character (1 or 2)
    :type screen: pygame.surface
    :type pNum: int"""
    
    def __init__(self,screen,pNum):
        super().__init__(screen,pNum,emityMovinator(self),[5,4,1,3,2])
        #self.displayAnimation= False
    
        
        self.times= [0,-1000,-1000,-10,-10]
        
        #[0]- time from last op1 activate (0 if you can activ it now)
        #[1]- time of last op3 activate
        #[2]- time of last op4 activate
        #[3]- time of last op2 activate
        #[4]- time of last op5 activate

        self.isFromTick=False
        self.powerP=100
        self.isSildBroken=False
        self.shitDerection="off"

        #parameters for quick change
        self.powerPgenerateV=0.1
        self.glemGeneratingTime=200
        self.shoteGeneratingTime=400

    def tick(self):
        """this function pass 1 frame to this character and the objects created by it, and paint those objects
        NOTE: this function supposed to be called after the special operations actived
        """
        self.isFromTick=True
        
        super().tick()

        if self.powerP+self.powerPgenerateV<=100:
            self.powerP+=self.powerPgenerateV

        if self.times[0]!=0:
            self.op1()
        
        self.isFromTick=False

    def paramPaint(self):
        """paint characters parameters (such as hp)"""
        super().paramPaint()
        #powerP paint
        powerPPos=(120,50) #powerP display posizion for player 1
        powerPWid=100 #powerP display width
        if self.pNum==1:
            blitIncription(prosentRestIncription(self.powerP,powerPWid,20,(100,100,100)),powerPPos)
        else:
            blitIncription(prosentRestIncription(self.powerP,powerPWid,20,(100,100,100)),(self.screen.get_width()-powerPPos[0]-powerPWid,powerPPos[1]))

        #glome makeAble paint
        glomeMakeAbleCenter=(135,105)
        r=25
        self.clockPaint(glomeMakeAbleCenter,r,min((self.timeFromStart-self.times[1])/self.glemGeneratingTime,1))

        shoteMakeAbleCenter=(195,105)
        r=25
        self.clockPaint(shoteMakeAbleCenter,r,min((self.timeFromStart-self.times[2])/self.shoteGeneratingTime,1))
    def op1(self):
        """kik operation"""
        kw=20 #kik width
        kh=40 #kik high
        kt=15 #kik time
        
        blastSize=10
        if self.times[0]==0:
            self.times[0]=1
            if self.xDirection!="":
                self.movinator.kik_init()
            return
        if self.isFromTick:
            if self.times[0]==kt:
                self.times[0]=-10
                return
            if self.times[0]>0:
                if self.xDirection=="moveN":
                    kx=self.x+10
                    ky=self.y+self.size[1]/2-kh/2
                    blastDir=(-10,0) #blast direction
                    kd=4 #kik damage
                elif self.xDirection=="moveP":
                    kx=self.x+self.size[0]-kw-10
                    ky=self.y+self.size[1]/2-kh/2
                    blastDir=(10,0)
                    kd=4 #kik damage
                else:
                    self.times[0]=0
                    return
                if self.display_rects:
                    rectDrewIncription((150, 0, 120),(kx,ky,kw,kh),3)
                self.restHitEnemies(blastDir,kd,(kx,ky,kw,kh),3)
            self.times[0]+=1
            #if min(self.enemy.x+self.enemy.size[0])

    def op2(self):
        """shild operation"""
        if self.powerP>0:
            #change parameters:
            #self.moveA=15
            #self.jumpSpeed= -35
            self.times[3]=self.timeFromStart
            self.shitDerection= self.lookDirection
            #draw
            if self.display_rects:
                if self.shitDerection=="moveN":
                    rectDrewIncription((0, 255, 0),(self.x,self.y,20,self.size[1]))
                elif self.shitDerection=="moveP":
                    rectDrewIncription((0, 255, 0),(self.x+self.size[0]-10,self.y,20,self.size[1]))
                elif self.shitDerection=="jump":
                    rectDrewIncription((0, 255, 0),(self.x,self.y,self.size[0],20))

    def resetParam(self):
        """reset specific parameters"""
        super().resetParam()

        if self.timeFromStart-self.times[3]<2:
            self.move_v=6
            self.jump_speed= -14
        else:
            self.shitDerection="off"
            
    
    def op3(self):
        """golem creation operation"""
        if self.timeFromStart-self.times[1]>=self.glemGeneratingTime:
            self.times[1]=self.timeFromStart
            newGolem=golem(self.screen,self.pNum,self.floorLevel,100,1400,self.x,self.floorLevel)
            newGolem.enemy=self.enemy
            self.tickAbleAppend(newGolem)
            self.movinator.circle_init()

    def op4(self):
        """slyme shoot operation"""
        #x,y,maneAnemy,floorlevel,leftWall,rightWall,vx,length,uctivator
        if self.timeFromStart-self.times[2]>=self.shoteGeneratingTime:
            self.times[2]=self.timeFromStart
            #print(self.lookDirection)
            if self.xDirection=="moveP":
                self.tickAbleAppend(emtShot(self.x+self.size[0],self.y+self.size[1]/2-5,self.enemy,self.floorLevel,100,1400,20,50,self))
            elif self.xDirection=="moveN":
                self.tickAbleAppend(emtShot(self.x-50,self.y+self.size[1]/2-5,self.enemy,self.floorLevel,100,1400,-20,50,self))
    def op5(self):
        """golem throw head"""
        if self.timeFromStart-self.times[4]>=20:
            self.times[4]=self.timeFromStart
            for obj in self.supporters:
                if isinstance(obj,golem):
                    obj.headThrow_init()
                    return

    def hit(self,blast,damage,stanT=5):
        a=atan2(blast[1],blast[0])
        if -pi/4<a<pi/4 and self.shitDerection=="moveN":
            self.shitHit(blast,damage)
        elif pi/4<a<=3*pi/4 and self.shitDerection=="jump":
            self.shitHit(blast,damage)
        elif (a<-3*pi/4 or a>3*pi/4) and self.shitDerection=="moveP":
            self.shitHit(blast,damage)
        else:
            super().hit(blast,damage,stanT)

    def shitHit(self,blast,damage):
        """hit emity's shild"""
        if self.powerP>=damage:
            self.powerP-=damage
        else:
            blast= (blast[0]*(self.powerP/damage), blast[1]*(self.powerP/damage))
            damage-=self.powerP
            self.powerP=-20
            self.shitDerection="off"
            super().hit(blast,damage)

class emityMovinator(absMovinator):
    """emity's movinator
    :param character: its character
    :type character: absCaracter"""
    def __init__(self,character):
        rectsize=(100,100)
        color=(147, 70, 151)
        super().__init__(color,rectsize,"emity",character)
    
    def kik_init(self):
        """start the animation of kik"""
        self.op= self.kik
        self.opT= self.t
        #self.opData will not store nothing
    
    def kik(self):
        """playing the animation of kiking"""
        directory="emity/kikN"
        if self.c.xDirection=="moveP":
            directory="emity/kikP"
        image= self.getFrame(directory,self.t-self.opT,10000)
        try:
            TheMainGame.datafiles.imeges.img_indentation[image]
            self.image=image
        except:
            self.op= None

    def circle_init(self):
        """start the animation of drewing circle"""
        self.op= self.circle
        self.opT= self.t
        #self.opData will not store nothing
    
    def circle(self):
        """playing the animation of painting circle"""
        directory="emity/making circle"
        image= self.getFrame(directory,(self.t-self.opT)//2,10000)
        try:
            TheMainGame.datafiles.imeges.img_indentation[image]
            self.image=image
        except:
            self.op= None

    def tick(self):
        super().tick()
        if self.op==None:
            if self.c.shitDerection=="moveN":
                self.image= "emity/charImg/shildN"
            elif self.c.shitDerection=="moveP":
                self.image= "emity/charImg/shildP"
            elif self.c.shitDerection=="jump":
                self.image= "emity/charImg/shild up"
            self.rectsize= TheMainGame.datafiles.imeges.imegesDict[self.image].get_size()
            if self.img_indentation!=None:
                self.c_x_y_update()
            self.img_indentation= TheMainGame.datafiles.imeges.img_indentation[self.image]
            self.oldImg=self.image

class golem(absCaracter):
    """golem game character
    :param screen: pointer to the screen
    :param pNum: the number of the character (1 or 2)
    :param floorlevel: y of the floor
    :param leftWall: x of the left wall
    :param rightWall: x of the right wall
    :param x: its x
    :param y: its y
    :type screen: pygame.surface
    :type pNum: int
    :type floorlevel: int
    :type leftWall: int
    :type rightWall: int
    :type x: its x
    :type y: its y"""
    def __init__(self,screen,pNum,floorlevel,leftWall,rightWall,x,y):
        super().__init__(screen,pNum,golemMovinator(self),[1,2,3,4,5])
        self.fL=floorlevel
        self.lW=leftWall
        self.rW=rightWall

        self.MOVE_V=6

        self.x=x
        self.y=y
        self.times=[0] #times[0]- time from last kik activate (0 if you can activ it now)
        self.is_dying=False
        self.death_x=0
    def tick(self):
        """this function pass 1 frame to this golem and paint it"""
        self.botPlay()

        self.isFromTick=True
        super().tick()
        if self.times[0]!=0:
            self.kik()
        self.isFromTick=False

    def paramPaint(self):
        #hp paint
        hpPos=(self.x+self.size[0]/2-50,self.y-30) #hp display posizion for player 1
        hpWid=100 #hp display width
        blitIncription(prosentRestIncription(self.hp,hpWid,20,(200,200,200)),hpPos)
        

    def hit(self,blast,damage,stanT=5):
        super().hit(blast,damage*8,stanT)

    def winningCheck(self):
        if self.hp<0:
            if not self.is_dying:
                #print("call")
                self.movinator.death_with_head_init()
            self.vx=0
            self.vy=0
            self.is_dying= True

    def botPlay(self):
        """golem bot play"""
        target=self.enemy.supporters[0]
        for c in self.enemy.supporters:
            if abs(c.x+c.size[0]/2-self.x)<abs(target.x+target.size[0]/2-self.x):
                target=c
        if target.get_aiming_x()+target.size[0]/2<self.x:
            self.moveN()
            if self.x-(target.x+target.size[0])<40:
                self.kik()
        else:
            self.moveP()
            if target.x-(self.x+self.size[0])<40:
                self.kik()

    def kik(self):
        """kik in moving direction"""
        
        if self.stantimer<=0:
            kw=60 #kik width
            kh=40 #kik high
            kt=15 #kik time
            blastSize=20
            if self.times[0]==0:
                self.times[0]=1
                self.movinator.kik_init(kt)
                return
            elif self.isFromTick:
                if self.times[0]==kt:
                    self.times[0]=-10
                    return
                if self.times[0]>0:
                    if self.lookDirection=="moveN":
                        kx=self.x
                        ky=self.y+self.size[1]/2-kh/2-20
                        blastDir=(-10,0) #blast direction
                        kd=0.5 #kik damage
                    elif self.lookDirection=="moveP":
                        kx=self.x+self.size[0]-kw
                        ky=self.y+self.size[1]/2-kh/2-20
                        blastDir=(10,0)
                        kd=0.5 #kik damage
                    else:
                        self.times[0]=0
                        return
                    if self.display_rects:
                        rectDrewIncription((150, 0, 120),(kx,ky,kw,kh),3)
                    
                    self.restHitEnemies(blastDir,kd,(kx,ky,kw,kh))
                self.times[0]+=1

    def headThrow_init(self):
        """start throwing head animation"""
        self.movinator.throw_head_init()
    
    def headThrow(self):
        """throwing it's head (after the animation)"""
        #choosing turget point
        self.movinator.death_without_head_init()
        self.hp=-1
        self.is_dying=True
        target=self.enemy.supporters[0]
        for c in self.enemy.supporters:
            if abs(c.x+c.size[0]/2-self.x)<abs(target.x+target.size[0]/2-self.x) and isinstance(c,absCaracter):
                target=c
        target=(target.get_aiming_x()+target.size[0]/2,target.get_aiming_y()+target.size[1]/2)

        ay=1.6
        v=40
        headSize= TheMainGame.datafiles.imeges.imegesDict["emity/golem/head"].get_size()

        #calculating the shooting angle
        dx= target[0]-(self.x+headSize[0]/2)
        dy= target[1]-(self.y+headSize[1]/2)

        if dx==0:
            angle=pi/2
        else:
            try:
                a=ay*dx**2/(2*v**2) #root formula parameter
                b=dx #root formula parameter
                c=ay*dx**2/(2*v**2)-dy #root formula parameter
                tanA1=(-b+sqrt(b**2-4*a*c))/(2*a) #root formula answer
                tanA2=(-b-sqrt(b**2-4*a*c))/(2*a) #root formula answer
                posibleAngles=[atan(tanA1),atan(tanA1)+pi,atan(tanA2),atan(tanA2)+pi]

                i=0
                #print(4,posibleAngles)
                while i<len(posibleAngles):
                    t=dx/(v*cos(posibleAngles[i]))
                    if t>=0:
                        i+=1
                    else:
                        posibleAngles.pop(i)

                #print(5,posibleAngles)
                angle=choice(posibleAngles)
                #print(6)
            except:
                angle=-pi/4

        self.enemy.enemy.tickAbleAppend(golemHead(self.x,self.y,self.enemy,angle,10000,v,self.fL,self.lW,self.rW,10,20,headSize))

        
class golemMovinator(absMovinator):
    """golem movinator
    :param charcter: its character
    :type charcter: absCaracter"""
    def __init__(self,charcter):
        rectsize=(100,150)
        color=(200, 0, 200)
        super().__init__(color,rectsize,"emity/golem",charcter)

    def kik_init(self,t):
        """start the animation of kik"""
        if self.op in [None, self.kik]:
            self.op= self.kik
            self.opT= self.t
            #self.opData will store the length (in frames) of the kik
            self.data= t
    
    def kik(self):
        """playing the animation of kiking"""
        if self.t-self.opT<self.data:
            self.image="emity/golem/kikN"
            if self.c.xDirection=="moveP":
                self.image="emity/golem/kikP"
        else:
            self.op= None

    def throw_head_init(self):
        """start the animation of throwing head"""
        if self.op in [None, self.kik]:
            self.op= self.throw_head
            self.opT= self.t
            #self.opData will store nothing

    def throw_head(self):
        """playing the animation of throwing head"""
        directory="emity/golem/throw headN"
        if self.c.xDirection=="moveP":
            directory="emity/golem/throw headP"
        image= self.getFrame(directory,self.t-self.opT,10000)
        try:
            TheMainGame.datafiles.imeges.img_indentation[image]
            self.image=image
        except:
            self.op= None
            self.c.headThrow()

    def death_without_head_init(self):
        """start the animation of death without head"""
        if self.op in [None, self.kik]:
            self.op= self.death_without_head
            self.opT= self.t
            #self.opData will store nothing

    def death_without_head(self):
        """playing the animation of death without head"""
        directory="emity/golem/death_without_head"
        image= self.getFrame(directory,(self.t-self.opT),10000)
        try:
            TheMainGame.datafiles.imeges.img_indentation[image]
            self.image=image
        except:
            self.op= None
            self.c.isActive=False

    def death_with_head_init(self):
        """start the animation of deth with head"""
        if self.op in [None, self.kik]:
            #print("di")
            self.op= self.death_with_head
            self.opT= self.t
            #self.opData will store nothing

    def death_with_head(self):
        """playing the animation of death with head"""
        #print("d",self.t-self.opT)
        directory="emity/golem/death_with_head"
        image= self.getFrame(directory,(self.t-self.opT)//2,10000000)
        try:
            TheMainGame.datafiles.imeges.img_indentation[image]
            self.image=image
        except:
            self.op= None
            self.c.isActive=False
            #print(self.c.isActive)

class golemHead(absErrow):
    """thrown head of the golem
    :param x: the x of the errow
    :param y: the y of the errow
    :param maneAnemy: the mane enemy of the produser of the errow
    :param a: the angle relative to x axis
    :param destroyTime: after that emount of frames, this object destroyed
    :param v: speed
    :param floorlevel: the y of the floor
    :param leftWall: left wall x
    :param rightWall: right wall x
    :param blastSize: the size of the blast
    :param damege: the demeg size
    :type x: int
    :type y: int
    :type maneAnemy: absCharacter
    :type a: float
    :type destroyTime: int
    :type v: int
    :type floorlevel: int
    :type leftWall: int
    :type rightWall: int
    :type blastSize: int
    :type damege: int
    """
    def __init__(self,x,y,maneAnemy,a,destroyTime,v,floorlevel,leftWall,rightWall,blastSize,damege,size):
        super().__init__(x,y,maneAnemy,a,destroyTime,v,floorlevel,leftWall,rightWall,blastSize,damege,0)
        self.size=size
        self.ay=1.6

    def tick(self):
        vx= self.v*cos(self.a)
        vy= self.v*sin(self.a)
        vy+=self.ay
        self.v=sqrt(vx**2+vy**2)
        self.a=atan2(vy,vx)
        super().tick()

    def isHit(self):
        rectTuple=(self.x,self.y,self.size[0],self.size[1])
        for en in self.maneAnemy.supporters:
            if max(rectTuple[0],en.x)<min(rectTuple[0]+rectTuple[2], en.x+en.size[0]) and max(rectTuple[1],en.y)<min(rectTuple[1]+rectTuple[3], en.y+en.size[1]):
                return en
        return None

    def restHitEnemies(self,blast,damage,rectTuple): #rect tuple as it insert in pygame.Rect
        #hit all the characters in the rect
        for en in self.enemy.supporters:
            if max(rectTuple[0],en.x)<min(rectTuple[0]+rectTuple[2], en.x+en.size[0]) and max(rectTuple[1],en.y)<min(rectTuple[1]+rectTuple[3], en.y+en.size[1]):
                en.hit(blast,damage)

    def paint(self):
        blitIncription("emity/golem/head",(self.x,self.y))
        if global_var.display_rects:
            rectDrewIncription((200, 0, 200),(self.x,self.y,self.size[0],self.size[1]),3)
            

class emtShot(absErrow):
    """shot for the that on hit torn to slyme boble
    :param x: the x of the errow
    :param y: the y of the errow
    :param maneAnemy: the mane enemy of the produser of the errow
    :param floorlevel: the y of the floor
    :param leftWall: left wall x
    :param rightWall: right wall x
    :param vx: shot speed on x axis
    :param length: the length of the errow
    :param uctivator: pointer to the character that activated this shot
    :type x: int
    :type y: int
    :type maneAnemy: absCharacter
    :type a: float
    :type destroyTime: int
    :type v: int
    :type floorlevel: int
    :type leftWall: int
    :type rightWall: int
    :type blastSize: int
    :type damege: int
    :type length: int
    :type vx: flout
    :type uctivator: absCaracter
    """
    def __init__(self,x,y,maneAnemy,floorlevel,leftWall,rightWall,vx,length,uctivator):
        super().__init__(x,y,maneAnemy,0,100,vx,floorlevel,leftWall,rightWall,0,0,length)
        self.uctivator=uctivator

    def paint(self):
        imgSize= TheMainGame.datafiles.imeges.imegesDict["emity/slyme boble hitN/1"].get_size()
        if self.v<0:
            blitIncription("emity/slyme boble hitN/1",(self.x+self.L/2-imgSize[0]/2, self.y-imgSize[1]/2))
        else:
            blitIncription("emity/slyme boble hitP/1",(self.x+self.L/2-imgSize[0]/2, self.y-imgSize[1]/2))
        if global_var.display_rects:
            super().paint()
    def onHit(self,en):
        if isinstance(en,absCaracter):
            self.uctivator.tickAbleAppend(SlymeBoble(en,self.uctivator,self.v))
        self.isActive=False


class SlymeBoble:
    """shot for the that on hit torn to slyme boble
    :param enemy: the mane enemy character
    :param supportedChar: the main in character wich it support
    :param direction:shoot of this boble direction. <0-left, >0-right
    """
    def __init__(self,enemy,supportedChar,direction):#parent,screen,x,y,w,h
        w=40
        self.stanedYFloor= enemy.y+enemy.size[1]
        self.standx= enemy.x
        self.paramP=(enemy.x+enemy.size[0]/2-50,enemy.y-w-30)
        self.slimeRect=hitablePartBlock(self,enemy.x-w,enemy.y-w,enemy.size[0]+2*w,enemy.size[1]+2*w,supportedChar)
        self.hp=100
        self.self_dpf= 1
        self.maneEnemy=supportedChar.enemy
        self.isActive=True

        #for animation
        self.t=0
        self.direction=direction #<0 - left. >0 - right

        self.stanedEnemys=[]

    def tick(self):
        """this function pass 1 frame to this golem and paint it"""
        self.paint()
        self.hiting()
        self.paramPaint()

        self.hp-= self.self_dpf

        if self.hp<=0:
            self.activeOff()

        self.t+=1

    def hiting(self):
        """check is it nesesery to hit other objects and hit, check who it need to add to self.stanedEnemys and hit unholdable objects (like plants)"""
        hitedEnemys=self.slimeRect.isHit(self.maneEnemy.supporters)
        for en in hitedEnemys:
            if isinstance(en,absCaracter):
                if not en in self.stanedEnemys:
                    self.stanedEnemys.append(en)
            else:
                en.hit((0,0),1)

        #hold self.stanedEnemys in there place
        
        for en in self.stanedEnemys:
            en.vx=0
            en.vy=0
            en.x=self.standx
            en.y=self.stanedYFloor-en.size[1]
            en.stantimer= -10
        
    def paint(self):
        """paint this slyme boble"""
        directory="emity/slyme boble hitN/"
        if self.direction>0:
            directory="emity/slyme boble hitP/"
        file= open("TheMainGame/images/"+directory+"frames num.txt")
        fram_num= int(file.read())
        file.close()
        imgSize= TheMainGame.datafiles.imeges.imegesDict["emity/slyme boble hitN/"+str(min(self.t,fram_num-1))].get_size()
        blitIncription(directory+str(min(self.t//2,fram_num-1)),(self.slimeRect.x+self.slimeRect.size[0]/2-imgSize[0]/2,
                                                                            self.slimeRect.y+self.slimeRect.size[1]/2-imgSize[1]/2))
        if global_var.display_rects:
            self.slimeRect.paint()

    def selfHit(self,blast,damege):
        """hit itself
        :param blast: 2D vector to append to this character speed
        :param damage: the demege to this character
        :param stanT: how many time from now the stan should be
        :type blast: (int,int) or [int,int]
        :type damage: int
        :type stanT: int"""
        self.hp-=4.5*damege

    def paramPaint(self):
        """painting this object parameters"""
        hpRectCode=prosentRestIncription(self.hp,100,20,(100,100,100))
        blitIncription(hpRectCode,self.paramP)

    def activeOff(self):
        """destroy the object"""
        self.slimeRect.isActive=False
        self.isActive=False
    

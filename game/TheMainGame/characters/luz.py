from TheMainGame.characters.absCaracter import*
from math import*

class luz(absCaracter):
    """luz game character
    :param screen: pointer to the screen
    :param pNum: the number of the character (1 or 2)
    :type screen: pygame.surface
    :type pNum: int"""
    def __init__(self,screen,pNum):
        super().__init__(screen,pNum,luzMovinator(self),[1,5,3,4,2])

        self.times= [-20,0,-20,0,-200]
        
        #[0]- time of last op1 activate
        #[1]- time of last op2 activate
        #[2]- time of last op3 activate
        #[3]- time of last op4 activate
        #[4]- time of last op5 activate

        self.LODING_ABILITIES_TIMES=[100,100,100,200] #[0]-light,[1]-ice,[2]-fire,[3]-plant
        self.MAX_ABILITY_STORAGE=3

        self.lodedAbilitesClocks=self.LODING_ABILITIES_TIMES.copy() #[0]-light,[1]-ice,[2]-fire,[3]-plant

        self.lookDirection="moveP"
        self.op5T=29
        self.op5Dir=""
    def tick(self):
        self.isFromTick=True

        #kikDirection update
        if self.lastComand in ["jump","moveP","moveN","down"]:
                self.lookDirection=self.lastComand
        super().tick()

        for i in range(4):
            self.lodedAbilitesClocks[i]=min(self.MAX_ABILITY_STORAGE*self.LODING_ABILITIES_TIMES[i],self.lodedAbilitesClocks[i]+1)

        #print(self.timeFromStart-self.times[4],self.op5T)
        if self.timeFromStart-self.times[4]<=self.op5T:
            self.op5()

        self.isFromTick=False

    def paramPaint(self):
        super().paramPaint()

        font = pygame.font.SysFont("comicsansms", 40)
        
        r=50
        abilitesCirclesSenters=[(170,100),(170+2*r+10,100),(170,100+2*r+10),(170+2*r+10,100+2*r+10)] #in the same order like self.lodedAbilitesClocks
        gliphsPicters=["luz/gliphs/light","luz/gliphs/ice","luz/gliphs/fire","luz/gliphs/plant"]
        
        for i in range(4):
            #if i==3:
            #    print(self.lodedAbilitesClocks[i]/self.LODING_ABILITIES_TIMES[i])
            self.imegedClockPaint(abilitesCirclesSenters[i],r,self.lodedAbilitesClocks[i]/self.LODING_ABILITIES_TIMES[i],gliphsPicters[i])
            
            text = font.render(str(self.lodedAbilitesClocks[i]//self.LODING_ABILITIES_TIMES[i]), True, (0, 128, 0))
            textRect = text.get_rect()
            
            if self.pNum==1:
                textRect.center = abilitesCirclesSenters[i]
            else:
                textRect.center = (self.screen.get_width()-abilitesCirclesSenters[i][0],abilitesCirclesSenters[i][1])
            
            blitIncription(textDrawIncription("comicsansms", 40,str(self.lodedAbilitesClocks[i]//self.LODING_ABILITIES_TIMES[i]),(125, 125, 125)),textRect.topleft)
            
        
    def op1(self):
        """lightShot"""
        if self.timeFromStart-self.times[0]>20 and self.lodedAbilitesClocks[0]>=self.LODING_ABILITIES_TIMES[0] and (self.lookDirection in ["moveP","moveN"]):
            self.lodedAbilitesClocks[0]-=self.LODING_ABILITIES_TIMES[0]
            self.times[0]=self.timeFromStart
            if self.lookDirection=="moveP":
                self.lightShot((self.x+self.size[0],self.y+self.size[1]/2),90)
            else:
                self.lightShot((self.x,self.y+self.size[1]/2),90)
            self.movinator.lightning_init()

    def op2(self):
        """iceWall"""
        if self.timeFromStart-self.times[1]>20 and self.lodedAbilitesClocks[1]>=self.LODING_ABILITIES_TIMES[1] and (self.lookDirection in ["moveP","moveN"]):
            self.lodedAbilitesClocks[1]-=self.LODING_ABILITIES_TIMES[1]
            self.times[1]=self.timeFromStart
            if self.lookDirection=="moveP":
                newIceWall=iceWall(self.x+self.size[0]+10,self.floorLevel+20,self)
            else:
                newIceWall=iceWall(self.x-10-116,self.floorLevel+20,self)
            self.tickAbleAppend(newIceWall)
            self.movinator.iceWall_init()
    
    def op3(self):
        """fire boll"""
        if self.timeFromStart-self.times[2]>20 and self.lodedAbilitesClocks[2]>=self.LODING_ABILITIES_TIMES[2]:
            self.lodedAbilitesClocks[2]-=self.LODING_ABILITIES_TIMES[2]
            self.times[2]=self.timeFromStart
            fx=0 #fireBall x
            fy=0 #fireBall y
            fa=0 #fireBall a
            if self.lookDirection=="moveP":
                fx=self.x+self.size[0]
                fy=self.y+self.size[1]/2
                fa=0
            elif self.lookDirection=="moveN":
                fx=self.x
                fy=self.y+self.size[1]/2
                fa=pi
            elif self.lookDirection=="jump":
                fx=self.x+self.size[0]/2
                fy=self.y
                fa=3*pi/2
            elif self.lookDirection=="down":
                fx=self.x+self.size[0]/2
                fy=self.y+self.size[1]
                fa=pi/2
            self.tickAbleAppend(fireBall(fx,fy,self.enemy,fa,200,20,self.floorLevel,100,1400,100,20,25))
            self.movinator.fireball_init()

    def op4(self):
        """plant"""
        if self.timeFromStart-self.times[3]>20 and self.lodedAbilitesClocks[3]>=self.LODING_ABILITIES_TIMES[3] and (self.lookDirection in ["moveP","moveN"]):
            self.lodedAbilitesClocks[3]-=self.LODING_ABILITIES_TIMES[3]
            self.times[3]=self.timeFromStart
            if self.lookDirection=="moveP":
                self.tickAbleAppend(burrow(self.x,self.floorLevel,10,self.enemy,self.tickAbleCreatedObjects,50,self.screen))
            else:
                self.tickAbleAppend(burrow(self.x,self.floorLevel,-10,self.enemy,self.tickAbleCreatedObjects,50,self.screen))
            self.movinator.plant_init()
            
            
    def op5(self):
        """ice jump"""
        if self.timeFromStart-self.times[4]>self.op5T and self.lodedAbilitesClocks[1]>=self.LODING_ABILITIES_TIMES[1] and self.onGround() and (self.lastComand in ["","moveP","moveN"]):
            self.lodedAbilitesClocks[1]-=self.LODING_ABILITIES_TIMES[1]
            self.times[4]=self.timeFromStart
            self.op5Dir=self.lastComand
            self.movinator.ice_jump_init()
        elif self.isFromTick:
            start_T= 19
            img_pos=None
            img_a=None
            if self.timeFromStart-self.times[4]>start_T:
                ice=pygame.Surface((75, 400)).convert_alpha() #used to check where to place the ice image
                ice.fill((0,0,255))
                ice_size_m= (0.646,2)
                if self.op5Dir=="":
                    self.vy=self.jump_speed*2
                    #blitIncription(rotatedfilledSurfaseCreateIncription((75, 400),(0,0,255),0),(self.x+self.size[0]/2-37.5,self.y+self.size[1]))
                    img_pos= (self.x+self.size[0]/2,self.y+self.size[1])
                    img_a= 90
                    blitIncription(rotatedResizedImageIncription("luz/melting_ice/0",ice_size_m,0),(self.x+self.size[0]/2-37.5,self.y+self.size[1]))
                elif self.op5Dir=="moveP":
                    self.vy=self.jump_speed*sqrt(2)
                    self.vx=-self.jump_speed*sqrt(2)
                    ice=pygame.transform.rotate(ice,-45)
                    iceRect=ice.get_rect()
                    iceRect.topright=(self.x+self.size[0]/2,self.y+self.size[1]/2)
                    img_pos= iceRect.bottomleft
                    img_pos= (img_pos[0]+26.517,img_pos[1]-26.517)
                    img_a= -45
                    #blitIncription(rotatedfilledSurfaseCreateIncription((75, 400),(0,0,255),-45),iceRect.topleft)
                    blitIncription(rotatedResizedImageIncription("luz/melting_ice/0",ice_size_m,-45),iceRect.topleft)
                elif self.op5Dir=="moveN":
                    self.vy=self.jump_speed*sqrt(2)
                    self.vx=self.jump_speed*sqrt(2)
                    img_pos= (self.x+self.size[0]/2,self.y+self.size[1]/2)
                    img_a= 45
                    #blitIncription(rotatedfilledSurfaseCreateIncription((75, 400),(0,0,255),45),(self.x+self.size[0]/2,self.y+self.size[1]/2))
                    blitIncription(rotatedResizedImageIncription("luz/melting_ice/0",ice_size_m,45),(self.x+self.size[0]/2,self.y+self.size[1]/2))
            if self.timeFromStart-self.times[4]==self.op5T:
                #self.tickAbleAppend(melting_ice(img_pos,img_a,ice_size_m))
                pass
            

    def lightShot(self,center,shotNum):
        """shoot shotNum light shots from center in deferent derection (0<=alpha<2*pi).
        :param center: the point from which the fanction shoot the light shots
        :param shotNum: the number of lisht shots. shotNum>=2
        :type center: (float,float)
        :type shotNum: int. shotNum>=2"""
        stan_counter= light_stan_counter()
        for i in range(shotNum):
            self.tickAbleCreatedObjects.append(luzLightRay(center[0],center[1],self.enemy,(((2*pi)/(shotNum-1))*i),
                                             5,20,self.floorLevel,100,1400,0.2,stan_counter))

    def imegedClockPaint(self,center,r,prosents,imageName):
        """paint clocked image in center. if self.pNum==2, it peint it from the other derction of x axis (in x= self.screen.get_width()-center[0])
        :param center: the center of the clock
        :param r: the rudios of the clock
        :param prosents: the prosent from the full clock that need to be filled. prosents sowed as a float for example: 0.01 is 1%.if the prosents >1 it relate only to the flout part.
        :param imageName: the key for the image in TheMainGame.datafiles.imeges.imegesDict
        :type center: (float,float)
        :type r: float
        :type prosents: float
        :type imageName: string"""
        #prosents sowed as a float for example: 0.01 is 1%
        #if the prosents >1 it relate only to the flout part
        imgRect=pygame.Rect(0,0,2*r,2*r)
        if self.pNum==1:
            imgRect.center=center
        else:
            imgRect.center=(self.screen.get_width()-center[0],center[1])

        blitIncription(imegedClockImgIncription(r,prosents,imageName),imgRect.topleft)

class luzMovinator(absMovinator):
    def __init__(self,character):
        rectsize=(50,150)
        color=(30, 40, 120)
        super().__init__(color,rectsize,"luz",character)
        self.opData= None # any data (asid from self.opT) that will pass from op init to the op, will be stored hir

    def init_with_direction(self,op,directory):
        self.op= op
        self.opT= self.t
        #self.opData will store the directory of lightning in the right direction
        self.opData= directory

    def lightning_init(self):
        """start the animation of lignt shot"""
        self.init_with_direction(lambda: self.special_video(2),"luz/lightning"+self.c.xDirection[-1])

    def special_video(self,fram_division):
        image= self.getFrame(self.opData,int((self.t-self.opT)/fram_division),10000)
        try:
            TheMainGame.datafiles.imeges.img_indentation[image]
            self.image=image
        except:
            self.op= None

    def iceWall_init(self):
        """start the animation of creating ice wall"""
        self.init_with_direction(lambda: self.special_video(2),"luz/iceWall"+self.c.xDirection[-1])

    def fireball_init(self):
        """start the animation of shooting fireball"""
        directory= "luz/fireball"+{"moveN":"N","moveP":"P","jump":"U","down":"D"}[self.c.lookDirection]
        self.init_with_direction(lambda: self.special_video(1),directory)

    def plant_init(self):
        """start the animation of plant barrow creating"""
        self.init_with_direction(lambda: self.special_video(2),"luz/plant"+self.c.xDirection[-1])

    def ice_jump_init(self):
        """start the animation of shooting ricochet errows"""
        self.init_with_direction(lambda: self.special_video(1),"luz/ice jump")
    
    

    

class fireBall(absErrow):
    """fire ball that luz shot
    :param x: x of the center of the ball
    :param y: y of the center of the ball
    :param maneAnemy: the mane character enemy
    :param a: the angle in which it shooted
    :param destroyTime: the time before it destroyed (in frames)
    :param v: speed
    :param floorlevel: y of floor
    :param leftWall: x of left wall
    :param rightWall: x of right wall
    :param blastSize: the size of the blast
    :param damege: demege to the enemy on hit
    :param r: radius
    :type x: float
    :type y: float
    :type maneAnemy: absCaracter
    :type a: float
    :type destroyTime: int
    :type v: float
    :type floorlevel: float
    :type leftWall: float
    :type rightWall: float
    :type blastSize: float
    :type damege: float
    :type r: float"""
    def __init__(self,x,y,maneAnemy,a,destroyTime,v,floorlevel,leftWall,rightWall,blastSize,damege,r): #a-alpha
        super().__init__(x,y,maneAnemy,a,destroyTime,v,floorlevel,leftWall,rightWall,blastSize,damege,1)
        self.r=r
        self.x-=r
        self.y-=r
        self.size=[2*r,2*r]

        if 5*pi/4<a<=7*pi/4:
            self.img= "luz/fireballU"
        elif pi/4<a<=3*pi/4:
            self.img= "luz/fireballD"
        elif 3*pi/4<a<=5*pi:
            self.img= "luz/fireballL"
        else:
            self.img= "luz/fireballR"

    def isHit(self):
        for en in self.maneAnemy.supporters:
            if max(self.x-self.r,en.x)<min(self.x+self.r, en.x+en.size[0]) and max(self.y-self.r,en.y)<min(self.y+self.r, en.y+en.size[1]):
                return en
        return None
    
    def onHit(self,en):
        try:
            start_hp= en.hp
        except:
            start_hp=0
        en.hit((self.blastSize*cos(self.a),self.blastSize*sin(self.a)),self.damege)
        try:
            if en.hp>=0:
                print("get hir")
                self.isActive=False
            elif start_hp>=0:
                multiple= (start_hp-en.hp)/self.damege
                print("damage before:",self.damege,multiple)
                oldDemeg= self.damege
                self.damege-= start_hp/multiple
                print("damage after:",self.damege,multiple)
                #rudios chenging
                r= self.r
                self.x+= r
                self.y+= r
                self.r*= self.damege/oldDemeg
                r= self.r
                self.x-=r
                self.y-=r
                self.size=[2*r,2*r]
        except Exception as e:
            print(e)
            self.isActive=False
        
    def paint(self):
        #circleDrewIncription((255,0,0),self.r,(self.x+self.r,self.y+self.r))
        blitIncription(self.img,(self.x-40,self.y-40))
        if global_var.display_rects:
            self.hitingPpaint()
    def hitingPpaint(self):
        """paint the hiting rect"""
        rectDrewIncription((255,0,0),(self.x,self.y,self.size[0],self.size[1]),1)

    def hit(self,blast,demege,stan=5):
        pass

    def get_aiming_x(self):
        return self.x

    def get_aiming_y(self):
        return self.y

class light_stan_counter:
    def __init__(self):
        self.stans= {}
        
    def tick(self):
        for char in self.stans:
            try:
                char.stantimer= max(self.stans[char],char.stantimer)
            except:
                pass

class luzLightRay(absErrow):
    """one light ray that luz shot
    :param x: x of the center of the ball
    :param y: y of the center of the ball
    :param maneAnemy: the mane character enemy
    :param a: the angle in which it shooted
    :param destroyTime: the time before it destroyed (in frames)
    :param v: speed
    :param floorlevel: y of floor
    :param leftWall: x of left wall
    :param rightWall: x of right wall
    :param blastSize: the size of the blast
    :param damege: demege to the enemy on hit
    :param stanDamage: the stan that it append to enemy on hit
    :type x: float
    :type y: float
    :type maneAnemy: absCaracter
    :type a: float
    :type destroyTime: int
    :type v: float
    :type floorlevel: float
    :type leftWall: float
    :type rightWall: float
    :type blastSize: float
    :type damege: float
    :type stanDamage: float"""
    def __init__(self,x,y,maneAnemy,a,destroyTime,v,floorlevel,leftWall,rightWall,stanDamage,stan_counter_pointer): #a-alpha, stp-start point
        super().__init__(x,y,maneAnemy,a,destroyTime,v,floorlevel,leftWall,rightWall,0,0.01,0)
        self.stp= (x,y)
        self.stanDamage=stanDamage
        self.stan_counter_pointer= stan_counter_pointer

    def onHit(self,en):
        try:
            if en in self.stan_counter_pointer.stans:
                self.stan_counter_pointer.stans[en]+=self.stanDamage
            else:
                self.stan_counter_pointer.stans[en]=self.stanDamage
            self.stan_counter_pointer.tick()
        except:
            pass
    
    def TochingWalls(self):
        pass
    def isHit(self):
        self.L=sqrt((self.x-self.stp[0])**2+(self.y-self.stp[1])**2)
        self.a+=pi
        en=super().isHit()
        self.a-=pi
        return en
    def paint(self):
        lineDrewIncription((255,255,0),(self.x,self.y),self.stp)

class iceWall:
    """wall from ice
    :param x: x of the center of the wall
    :param floorLevel: y of the floor
    :param activator: the character that activated the ice
    :type x: float
    :type floorLevel: float
    :type activator: absCaracter"""
    
    def __init__(self,x,floorLevel,activator):
        self.frame=0
        self.size= TheMainGame.datafiles.imeges.imegesDict["luz/melting_ice/"+str(int(self.frame))].get_size()
        self.activator= activator
        
        self.hp=100
        self.isActive=True
        self.x=x
        self.y=floorLevel-self.size[1]
        self.displayAnimation=True
        self.display_rects=False
        
    def tick(self):
        """this function pass 1 frame to this wall and paint it"""
        self.paramPaint()
        self.paint()

        if self.hp<=0:
            self.activator.tickAbleAppend(melting_ice((self.x+self.size[0]/2,self.y+self.size[1]),0,(1,1)))
            self.isActive=False

    def paint(self):
        """paint the hiting place"""
        if self.displayAnimation:
            blitIncription("luz/melting_ice/"+str(int(self.frame)),(self.x,self.y))
            
        if self.display_rects:
            rectDrewIncription((0,0,255),(self.x,self.y,self.size[0],self.size[1]),10)

    def paramPaint(self):
        """"display wall parameters on screen (like hp)"""
        blitIncription(prosentRestIncription(self.hp,100,20,(100,100,100)),(self.x+self.size[0]/2-50,self.y-30))
    

    def hit(self,blast,damage,stan=0):
        """hit the wall
        :param blast: 2D vector to append to this character speed
        :param damage: the demege to this character
        :param stanT: how many time from now the stan should be
        :type blast: (int,int) or [int,int]
        :type damage: int
        :type stanT: int"""
        self.hp-=damage*1.5

    def get_aiming_x(self):
        """get aiming x for the enemy"""
        return self.x

    def get_aiming_y(self):
        """get aiming y for the enemy"""
        return self.y

class melting_ice:
    """use to show melting ice in some direction
    :param pos: the position of the middle of the bottom of the ice ice
    :param a: the angle of the ice according to y axis
    :param size_m: size multiple of the ice"""
    def __init__(self,pos,a,size_m):
        self.pos= pos
        self.a=a
        self.size_m= size_m
        self.frames_division= 2

        #parameters for internul using
        self.t=0
        self.isActive= True

    def tick(self):
        self.t+=1
        if not "luz/melting_ice/"+str(int(self.t/self.frames_division)) in TheMainGame.datafiles.imeges.img_indentation:
            self.isActive=False
            return

        #variables for quick access
        size= TheMainGame.datafiles.imeges.imegesDict["luz/melting_ice/"+str(int(self.t/self.frames_division))].get_size()

        self.y= self.pos[1]-sin(self.a*pi/180)*size[0]/2 -size[1]*cos(self.a*pi/180)
        self.x= self.pos[0]-cos(self.a*pi/180)*size[0]/2 -size[1]*sin(self.a*pi/180)

        #print(self.x,self.y,self.pos,size,-sin(self.a*pi/180)*size[0]/2, -size[1]*cos(self.a*pi/180))
        #paint
        self.paint()

    def paint(self):
        blitIncription(rotatedResizedImageIncription("luz/melting_ice/"+str(int(self.t/self.frames_division)),self.size_m,self.a),(self.x,self.y))

class lozPlant(plant):
    """plants that luz use
    :param x: its x
    :param y: its y
    :param rootSize: this plant will be constracted from rect with size of rootSizeXrootSize
    :param rectsForTick: appended rect in each fram
    :param torningMultiple: before uppending new rect,the plant is turning. the turning angle is torningMultiple*(the angle bitwin the plant and the enemy)
    :param maxT: after that amount of frames, the plant disapire
    :param parent: its creator
    :param dxForRect: the length that it move forword before the next rect
    :param selfDemegMultipel: the multiple that the hit operation doing for the demege
    :param timeToSidesGrow: time (in frames) until it stop growing vertical
    :param turgetInd: the index of the turget in parent.enemy.supporters
    :type x: int
    :type y: int
    :type rootSize: int
    :type rectsForTick: int
    :type torningMultiple: flout
    :type maxT: int
    :type parent: absCharacter
    :type dxForRect: flout
    :type selfDemegMultipel: flout
    :type timeToSidesGrow: int
    :type turgetInd: int
    """
    def __init__(self,x,y,rootSize,rectsForTick,torningMultiple,maxT,parent,dxForRect,selfDemegMultipel,timeToSidesGrow,turgetInd):#turgetInd-the index of the turget in parent.enemy.supporters 
        super().__init__(x,y,rootSize,rectsForTick,torningMultiple,maxT,parent,dxForRect,selfDemegMultipel,0.5,10,turgetInd)
        self.timeToSidesGrow=timeToSidesGrow
        self.torningMultiple=0
        self.originalTorningMultiple=torningMultiple
    def tick(self):
        if self.time>=self.timeToSidesGrow:
            self.torningMultiple=self.originalTorningMultiple
        super().tick()

class burrow:
    """the burrow that go from luz and plant the plants
    :param x: its current x
    :param y: its current y
    :param vx: speed in x axis
    :param maneAnemy: the mane character enemy
    :param tickAbleCreatedObjects: link to tickAbleCreatedObjects list in its creator object
    :param dx: distance betwin enemy x and the created plant
    :param screen: game screen
    :type x: float
    :type y: float
    :type vx: float
    :type maneAnemy: absCaracter
    :type tickAbleCreatedObjects: list of tickable objects
    :type dx: float
    :type screen: pygame.surface"""
    def __init__(self,x,y,vx,maneAnemy,tickAbleCreatedObjects,dx,screen):
        self.stP=(x,y) #start point
        self.x=x
        self.y=y
        
        self.vx=vx
        self.maneAnemy=maneAnemy
        self.tickAbleCreatedObjects=tickAbleCreatedObjects
        self.dx=dx

        self.plentNum=0 #already created plants number
        self.time=0
        self.isActive=True
        self.screen=screen

    def tick(self):
        """this function pass 1 frame to this wall and paint it"""
        #check does it need to move forword
        if self.plentNum<2:
            self.x+=self.vx


        #check does it need to plant plant
        if self.plentNum==0 and self.vx>0:
            for i in range(len(self.maneAnemy.supporters)):
                en=self.maneAnemy.supporters[i]
                if en.x-self.dx-15<=self.x<=en.get_aiming_x()-self.dx+15 and self.y-(en.get_aiming_y()+en.size[1])<=75:
                    self.newPlant(i)
                    break
        elif self.plentNum==1 and self.vx>0:
            for i in range(len(self.maneAnemy.supporters)):
                en=self.maneAnemy.supporters[i]
                if en.get_aiming_x()+en.size[0]+self.dx-15<=self.x<=en.get_aiming_x()+en.size[0]+self.dx+15 and self.y-(en.get_aiming_y()+en.size[1])<=75:
                    self.newPlant(i)
                    break
        elif self.plentNum==0 and self.vx<0:
            for i in range(len(self.maneAnemy.supporters)):
                en=self.maneAnemy.supporters[i]
                if en.get_aiming_x()+en.size[0]+self.dx+15>=self.x>=en.get_aiming_x()+en.size[0]+self.dx-15 and self.y-(en.get_aiming_y()+en.size[1])<=75:
                    self.newPlant(i)
                    break
        elif self.plentNum==1 and self.vx<0:
            for i in range(len(self.maneAnemy.supporters)):
                en=self.maneAnemy.supporters[i]
                if en.get_aiming_x()-self.dx+15>=self.x>=en.get_aiming_x()-self.dx-15 and self.y-(en.get_aiming_y()+en.size[1])<=75:
                    self.newPlant(i)
                    break

        #check does it out of the screen
        if self.x<=0 or self.x>=self.screen.get_width():
            self.isActive=False

        #check does it need to disappire (becouse of time ufter last plant)
        if self.plentNum==2:
            self.time+=1
            if self.time>=100:
                self.isActive=False

        self.paint()#paint

    def newPlant(self,i): 
        """plant new plant
        :param i: the place of the enemy to which the plant will drow in self.enemys
        :type i: int"""
        self.tickAbleCreatedObjects.append(lozPlant(self.x,self.y,20,1,0.1,100,self.maneAnemy.enemy,10,2,20,i))
        self.plentNum+=1

    def paint(self):
        """paint the borrow"""
        lineDrewIncription((136, 84, 0),self.stP,(self.x,self.y),10)

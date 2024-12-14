from TheMainGame.characters.absCaracter import*
from math import*
import time
import random
import global_var

class willow(absCaracter):
    """game charcter: willow
    :param screen: pointer to the screen
    :param pNum: the number of the character (1 or 2)
    :type screen: pygame.surface
    :type pNum: int"""
    def __init__(self,screen,pNum):
        super().__init__(screen,pNum,willowMovinator(self),[4,5,2,3,1])

        self.times= [-20,-20,0,-20,-20]
        #[0]- time of last op1 activate
        #[1]- time of last op2 activate
        #[2]- time from last op3 activate (if self.op3Direction=="down") or time until op3 will stop be activate (if self.op3Direction=="up")
        #[4]- time of last op5 activate

        self.lookDirection="moveP"
        
        self.powerP=[0] #it is a list so it will be pushed to other objects lick linck and not as int
        self.powerPGenerationSpead=0.5
        self.op5AchangeSpeed=0.1
        self.op3Direction="" #up if willow floting up or down if willow going down under the ground
        #self.display_rects= True
    def tick(self):
        self.isFromTick=True

        #kikDirection update
        if self.lastComand in ["jump","moveP","moveN","down"]:
                self.lookDirection=self.lastComand
        
        super().tick()

        self.powerP[0]+=self.powerPGenerationSpead

        if self.times[2]!=0:
            self.powerP[0]=max(0,self.powerP[0]-1)
            if self.powerP[0]==0:
                self.op3Direction="up"

        self.isFromTick=False

    def paramPaint(self):
        super().paramPaint()

        powerPPos=(120,50) #powerP display posizion for player 1
        powerPSize=(100,20) #powerP display (width,hight)
        self.paramPaintBlit(pygame.Surface(powerPSize),prosentRestIncription(self.powerP[0]%100,powerPSize[0],powerPSize[1],(100,100,100)),powerPPos)
        hundredPowerImg= TheMainGame.datafiles.imeges.imegesDict["willow/+"]
        #print(hundredPowerImg.get_width())

        for i in range(int(self.powerP[0]//100)):
            self.paramPaintBlit(hundredPowerImg,"willow/+",(powerPPos[0]+(hundredPowerImg.get_width()+10)*i,powerPPos[1]+powerPSize[1]+10))

    def paramPaintBlit(self,surface,surfaceCode,p):
        """blit the surface (that represent parameter) in the correct place uacounting the number of the player (is its param on right or left side)
        :param surface: the surface that it need to blit
        :param surfaceCode: the incoded code for the surface
        :param p: point to blit it for player 1"""
        if self.pNum==1:
            blitIncription(surfaceCode,p)
        else:
            blitIncription(surfaceCode,(self.screen.get_width()-p[0]-surface.get_width(),p[1]))
        
    def op1(self):
        """3 bot plants that growing to diferent directions growing. they will grow to closest to them enemy"""
        powerCoust=60
        
        if self.timeFromStart-self.times[0]>20 and self.onGround() and self.powerP[0]>=powerCoust:
            self.movinator.multiple_plants_init()
            self.powerP[0]-=powerCoust
            self.times[0]=self.timeFromStart
            plantStartP=(self.x+self.size[0]/2,self.floorLevel)
            for i in range(3):
                self.tickAbleCreatedObjects.append(botPlant(plantStartP[0],plantStartP[1],20,1,0.1,50,self,10,2,20,-pi/6-i*(pi/3)))

    def op2(self):
        """wall plant"""
        powerCoust=10
        
        if self.timeFromStart-self.times[1]>20 and self.onGround() and (self.lookDirection in ["moveP","moveN"]) and self.powerP[0]>=powerCoust:
            self.powerP[0]-=powerCoust
            self.movinator.wall_plant_init()
            self.times[1]=self.timeFromStart
            
            if self.lookDirection=="moveN":
                self.tickAbleCreatedObjects.append(wallplant(self.x-30,self.floorLevel,20,self,10,5,25,0.2))
            else:
                self.tickAbleCreatedObjects.append(wallplant(self.x+self.size[0]+30,self.floorLevel,20,self,10,5,25,0.2))
        pass
    
    def op3(self):
        """going under/above the ground"""
        if self.op3Direction=="" and self.times[2]==0:
            self.movinator.plant_down_init()
            self.op3Direction="down"
            self.times[2]=1
            self.tickAbleAppend(thorny_grass(self, self.floorLevel))
        elif self.op3Direction=="":
            self.movinator.plant_up_init()
            self.op3Direction="up"
        

    def has_avilable_plantwalls(self):
        """check does willow has plantwalls avilable for wall strike"""
        for obj in self.tickAbleCreatedObjects:
            if isinstance(obj,wallplant) and not obj.isAttacking:
                return True
        return False

    def op4(self):
        """all wall plants start grow in cercle in the derection of the enemy"""
        powerCoust=40
        plants_enemys_lst=[]
        if self.timeFromStart-self.times[3]>=20 and self.powerP[0]>=powerCoust and self.has_avilable_plantwalls():
            self.powerP[0]-=powerCoust
            self.times[3]=self.timeFromStart
            #plants_enemys_lst list filling
            for obj in self.tickAbleCreatedObjects:
                if isinstance(obj,wallplant) and not obj.isAttacking:
                    plants_enemys_lst.append(obj)
            for obj in self.enemy.supporters:
                if isinstance(obj,absCaracter):
                    plants_enemys_lst.append(obj)
            #sorting
            plants_enemys_lst.sort(key=lambda obj: obj.get_aiming_x())
            #making plants attak
            plants= [] #the plants that we alredy passed throw in the list and still dont attacking
            last_character_x= -1 #last character that we alredy passed throw in the list x coordinate
            for i in range(len(plants_enemys_lst)):
                if isinstance(plants_enemys_lst[i],wallplant):
                    if last_character_x==-1:
                        plants_enemys_lst[i].attack(1)
                    else:
                        plants.append(plants_enemys_lst[i])
                elif isinstance(plants_enemys_lst[i],absCaracter):
                    if last_character_x!=-1:
                        for p in plants:
                            if p.get_aiming_x()- last_character_x< plants_enemys_lst[i].get_aiming_x()- p.get_aiming_x():
                                p.attack(-1)
                            else:
                                p.attack(1)
                        plants=[]
                    last_character_x= plants_enemys_lst[i].get_aiming_x()

            for p in plants:
                p.attack(-1)
            
    def op5(self):
        """plant seed that will grow to flower that gives willow more energy"""
        powerCoust=60
        
        if self.timeFromStart-self.times[4]>20 and self.onGround() and self.powerP[0]>=powerCoust:
            self.powerP[0]-=powerCoust
            self.movinator.plant_seed_init()
            self.times[4]=self.timeFromStart
            self.tickAbleAppend(power_plant(self.x+self.size[0]/2,self.floorLevel,self,100,1400))
            print("done")
    
    def movingFizickRools(self):
        if self.times[2]==0:
            super().movingFizickRools()
        else:
            #if op3 is active (anderGround)
            #flotingTime=10
            flotingTime=25
            if self.op3Direction=="down":
                self.times[2]+=1
            elif self.op3Direction=="up":
                self.times[2]-=1
            self.vy=0
            self.y=self.floorLevel-self.size[1]+self.times[2]*(self.size[1]+20)/flotingTime

            #x axes fithick rules
            #map limit check
            self.x+=self.vx*4 #give to willow *4 speed (becouse she ander the ground)
            self.vx+=self.ax
            if self.x<100:
                self.x=100
                self.vx=0
            if self.x+self.size[0]>1400:
                self.x=1400-self.movinator.rectsize[0]
                self.vx=0

            #friction adding
            if self.vx>0:
                self.ax=-self.friction
            elif self.vx<0:
                self.ax=self.friction

            if self.times[2]==flotingTime or self.times[2]==0:
                self.op3Direction=""

                if self.times[2]==0:
                    for obj in self.tickAbleCreatedObjects:
                        if isinstance(obj,thorny_grass):
                            obj.remove()
                
    def stanIt(self,commundNum):
        if self.times[2]!=0:
            return commundNum!=3
        return super().stanIt(commundNum)

class willowMovinator(absMovinator):
    """hanter's movinator
    :param character: its character
    :type character: absCaracter"""
    def __init__(self,charcter):
        rectsize=(50,150)
        color=(30, 120, 30)
        super().__init__(color,rectsize,"willow",charcter)
    
    def multiple_plants_init(self):
        """start the animation of growing multiple plants"""
        self.op= self.multiple_plants
        self.opT= self.t
        #self.opData will store the start point of the character
        self.opData= (self.c.x,self.c.y)
    
    def multiple_plants(self):
        """playing the animation of growing multiple plants"""
        image= self.getFrame("willow/3-plantes",(self.t-self.opT)//3,10000)
        self.c.vx=0
        self.c.vy=0
        self.c.x,self.c.y= self.opData
        try:
            TheMainGame.datafiles.imeges.img_indentation[image]
            self.image=image
        except:
            self.op= None

    def plant_down_init(self):
        """start the animation of going underground"""
        self.op= self.plant_down
        self.opT= self.t
        #self.opData will not store anything
    
    def plant_down(self):
        """playing the animation of going underground"""
        image= self.getFrame("willow/plant down",(self.t-self.opT)*2,10000)
        try:
            TheMainGame.datafiles.imeges.img_indentation[image]
            self.image=image
        except:
            self.op= None

    def plant_up_init(self):
        """start the animation of going above the ground"""
        self.op= self.plant_up
        self.opT= self.t
        #self.opData will not store anything
    
    def plant_up(self):
        """playing the animation of going above the ground"""
        delay= 15
        if self.t-self.opT>delay:
            image= self.getFrame("willow/plant downR",(self.t-self.opT-delay)*2,10000)
            try:
                TheMainGame.datafiles.imeges.img_indentation[image]
                self.image=image
            except:
                self.op= None
        else:
            self.image= "willow/charImg/plant"

    def image_update(self):
        super().image_update()

        if self.c.times[2]!=0 and self.op==None:
            self.image= "willow/charImg/plant"

    def wall_plant_init(self):
        """start the animation of growing wall plant"""
        self.op= self.wall_plant
        self.opT= self.t
        #self.opData will store the directory of wall plant in the right direction
        self.opData= "willow/wall plantN"
        if self.c.xDirection=="moveP":
            self.opData= "willow/wall plantP"
    
    def wall_plant(self):
        """playing the animation of growing wall plant"""
        image= self.getFrame(self.opData,self.t-self.opT,10000)
        try:
            TheMainGame.datafiles.imeges.img_indentation[image]
            self.image=image
        except Exception as e:
            print(e)
            self.op= None

    def plant_seed_init(self):
        """start the animation of planting seed"""
        self.op= self.plant_seed
        self.opT= self.t
        #self.opData will store the start x -self.img_indentation[0]
        self.opData= self.c.x-self.img_indentation[0]
    
    def plant_seed(self):
        """playing the animation of planting seed"""
        image= self.getFrame("willow/plant seed",(self.t-self.opT)//2,10000)
        self.c.vx=0
        self.c.vy=0
        self.c.x= self.opData
        try:
            TheMainGame.datafiles.imeges.img_indentation[image]
            self.image=image
            self.opData+=TheMainGame.datafiles.imeges.img_indentation[self.image][0]-self.img_indentation[0]
        except:
            self.op= None

class power_plant:
    """plant that throw power circles (that give willow energy on hit) in the air. in the start it's a seed.
    :param x: x of center of the plant
    :param floorLevel: y of the floor
    :param uctivator: the absCaracter that created this object
    :param leftWall: x of left wall
    :param rightWall: x of the right wall
    :type x: float
    :type floorLevel: float
    :type uctivator: absCaracter
    :type leftWall: x of left wall
    :type rightWall: x of the right wall"""
    def __init__(self,x,floorLevel,uctivator,leftWall,rightWall):
        self.x= x
        self.fL= floorLevel
        self.uctivator= uctivator
        self.lW=leftWall
        self.rW=rightWall

        self.TIME_TO_GROW=40
        self.CYCLE_T=12
        self.SIZE=[20,50]

        self.size=self.SIZE
        self.isActive=True
        self.isGrowen=False
        self.time_from_start=0
        self.power_circle_to_shoot=15

    def paint(self):
        """paint this plant (or seed) on screen"""
        if global_var.display_rects:
            if self.isGrowen:
                rectDrewIncription((0,255,0),(self.x,self.fL-10,self.size[0],self.size[1]),10)
            else:
                rectDrewIncription((0,100,0),(self.x,self.fL,self.size[0]-10,self.size[1]),10)
        
        if self.isGrowen:
            imgSize= TheMainGame.datafiles.imeges.imegesDict["willow/Sunflower"].get_size()
            blitIncription("willow/Sunflower",(self.x+self.size[0]/2-imgSize[0]/2,
                                                                        self.fL-imgSize[1]))
        else:
            imgSize= TheMainGame.datafiles.imeges.imegesDict["willow/seed"].get_size()
            blitIncription("willow/seed",(self.x+self.size[0]/2-imgSize[0]/2,
                                                                        self.fL-imgSize[1]))

    def tick(self):
        """this function pass 1 frame to this plant and paint it"""
        self.time_from_start+=1
        self.paint()

        if self.TIME_TO_GROW<=self.time_from_start:
            self.isGrowen=True

        if self.isGrowen==True and self.time_from_start%self.CYCLE_T==0:
            self.shoot_power_circle()

        if self.power_circle_to_shoot<=0:
            self.isActive=False

    def shoot_power_circle(self):
        """shoot one power circle"""
        SHOOT_R=10
        self.uctivator.tickAbleAppend(power_circle(self.x-SHOOT_R, self.fL-2*SHOOT_R, self.uctivator, random.random()*(pi/2)-3*pi/4,300,40,self.fL,self.lW,self.rW
                                                   ,SHOOT_R))
        self.power_circle_to_shoot-=1


class power_circle(absErrow):
    """power circles that give willow energy on hit
    :param x: x of circle center
    :param y: y of circle center
    :param supported: the mane character supported by this object
    :param a: the angle relative to x axis
    :param destroyTime: after that emount of frames, this object destroyed
    :param v: speed
    :param floorlevel: the y of the floor
    :param leftWall: left wall x
    :param rightWall: right wall x
    :param r: the radius of the power circle
    :type x: int
    :type y: int
    :type maneAnemy: absCharacter
    :type a: float
    :type destroyTime: int
    :type v: int
    :type floorlevel: int
    :type leftWall: int
    :type rightWall: int
    :type r: float"""
    def __init__(self,x,y,supported,a,destroyTime,v,floorlevel,leftWall,rightWall,r):
        super().__init__(x,y,supported.enemy,a,destroyTime,v,floorlevel,leftWall,rightWall,0,0,0)
        self.r=r
        self.ay=1.6
        self.supported= supported
        
        self.ADD_P=6

    def tick(self):
        vx= self.v*cos(self.a)
        vy= self.v*sin(self.a)
        vy+=self.ay
        self.v=sqrt(vx**2+vy**2)
        self.a=atan2(vy,vx)
        super().tick()

    def isHit(self):
        rectTuple=(self.x,self.y,self.r,self.r)
        sup= self.supported
        if max(rectTuple[0],sup.x)<min(rectTuple[0]+rectTuple[2], sup.x+sup.size[0]) and max(rectTuple[1],sup.y)<min(rectTuple[1]+rectTuple[3], sup.y+sup.size[1]):
            return sup
        return None

    def TochingWalls(self):
        pass

    def onHit(self,hitted):
        hitted.powerP[0]+=self.ADD_P
        self.isActive=False

    def paint(self):
        circleDrewIncription((50, 200, 50),self.r,(self.x+self.r,self.y+self.r))
        
        
    

class botPlant(plant):
    """bot plant that grow to the derection of the closest enemy (after it grow gust forword in the start)
    :param x: its x
    :param y: its y
    :param rootSize: this plant will be constracted from rect with size of rootSizeXrootSize
    :param rectsForTick: appended rect in each fram
    :param torningMultiple: before uppending new rect,the plant is turning. the turning angle is torningMultiple*(the angle bitwin the plant and the enemy)
    :param maxT: after that amount of frames, the plant disapire
    :param parent: its creator
    :param dxForRect: the length that it move forword before the next rect
    :param selfDemegMultipel: the multiple that the hit operation doing for the demege
    :param timeToSidesGrow: after this emount of frames, the plant stops to grow in straight line
    :param startA: the angle in which this plant grow from the start
    :type x: int
    :type y: int
    :type rootSize: int
    :type rectsForTick: int
    :type torningMultiple: float
    :type maxT: int
    :type parent: absCharacter
    :type dxForRect: float
    :type selfDemegMultipel: float
    :type startA:  float"""
    def __init__(self,x,y,rootSize,rectsForTick,torningMultiple,maxT,parent,dxForRect,selfDemegMultipel,timeToSidesGrow,startA):
        super().__init__(x,y,rootSize,rectsForTick,torningMultiple,maxT,parent,dxForRect,selfDemegMultipel,0.5,10,0)
        self.a=startA
        self.timeToSidesGrow=timeToSidesGrow
        self.torningMultiple=0
        self.originalTorningMultiple=torningMultiple
    def tick(self):
        if self.time>=self.timeToSidesGrow:
            self.torningMultiple=self.originalTorningMultiple

        #finding the closest enemy
        closestEnemyIndex=0
        for i in range(1,len(self.parent.enemy.supporters)):
            if self.dist(self.parent.enemy.supporters[i])<self.dist(self.parent.enemy.supporters[closestEnemyIndex]):
                closestEnemyIndex=i
        self.turgetInd=closestEnemyIndex

        super().tick()

    def dist(self,en):
        """check the disatance betwin plants head and en
        :param en: enemy
        :type en: object with get_aiming_y,get_aiming_x methodes
        :return: disatance betwin plants head and en
        :rtype: float"""
        return sqrt((self.x-(en.get_aiming_x()+en.size[0]/2))**2+(self.y-(en.get_aiming_y()+en.size[1]/2))**2)

class wallplant(plant):
    """"wall plant
    :param x: its x
    :param y: its y
    :param rootSize: this plant will be constracted from rect with size of rootSizeXrootSize
    :param parent: its creator
    :param dxForRect: the length that it move forword before the next rect
    :param selfDemegMultipel: the multiple that the hit operation doing for the demege
    :param hpRedusingSpeed: how many hp reducing in eath frame
    :type x: int
    :type y: int
    :type rootSize: int
    :type parent: absCharacter
    :type dxForRect: flout
    :type selfDemegMultipel: flout
    :type hpRedusingSpeed: flout"""
    def __init__(self,x,y,rootSize,perant,dxForRect,selfDemegMultipel,gerowTime,hpRedusingSpeed):
        self.SPEED=1
        super().__init__(x,y,rootSize,self.SPEED,0,100000,perant,dxForRect,selfDemegMultipel,0,10,0)
        self.gerowTime=gerowTime
        self.hpRedusingSpeed=hpRedusingSpeed
        self.isAttacking=False
    def tick(self):
        self.hp-=self.hpRedusingSpeed
        if self.time>=self.gerowTime:
            self.speed=0
        super().tick()
    def attack(self,side):
        """this plant start grow in cercle in the derection side
        :param side: the side to which this plant supposed to grow. side=-1 -left.side=1 -right.
        :type side: int (-1 or 1)"""
        ATAK_ANGLE=0.06
        DEMEG=2.15
        ATAK_T=20
        SPEED=10
        self.torningMultiple=ATAK_ANGLE*side
        self.hitingDamage=DEMEG
        self.speed=self.SPEED
        self.maxT=ATAK_T
        self.time=0
        self.speed=SPEED
        self.isAttacking=True

        self.gerowTime= (2*pi/ATAK_ANGLE)/SPEED
        
    def growing(self):
        if not self.isAttacking:
            super().growing()
        else:
            for i in range(self.speed):
                self.plantBlocks.append(hitablePartBlock(self,self.x,self.y,self.rootSize,self.rootSize,self.parent,self.a))

                #upands the new rect to all the enemys
                    
                self.x+=self.dxForRect*cos(self.a)
                self.y+=self.dxForRect*sin(self.a)
                self.a+=self.torningMultiple
                
                if self.y<self.miny:
                    self.miny=self.y
                self.xSum+=self.x

    def get_aiming_x(self):
        return self.x

    def get_aiming_y(self):
        return self.y

class thorny_grass:
    """thorny grass that doing damege to enemys that stand on it
    :param activator: the character that activated it
    :param floorLevel: y of the floor"""
    def __init__(self,activator,floorLevel):
        #this object will act like wawe
        self.ACTIVATOR=activator
        self.L= self.ACTIVATOR.size[0]*1.5 #the length of the tritory that the grees need to cover
        self.MAXH=20
        self.L_PERE_GRESE_PART=20
        self.DEMEG_PER_HIT=0.1
        self.FL= floorLevel
        self.F= lambda x: self.FL-sin((pi/self.L)*x)*self.MAXH #the high of the grase as function of distance from its bigining

        self.isActive=True
        self.rects=[]

        for i in range(int(self.L/self.L_PERE_GRESE_PART+2)):
            self.rects.append(hitablePartBlock(self,-100,0,self.L_PERE_GRESE_PART,self.MAXH,self.ACTIVATOR))

    def tick(self):
        """this function pass 1 frame to this grass and paint it"""
        self.update_rect_p()
        self.paint()
        self.hitEnemys()

    def paint(self):
        """paint the grass"""
        for block in self.rects:
            if global_var.display_rects:
                block.paint()
            blitIncription("willow/thorn",(block.x, block.y))

    def update_rect_p(self):
        """update it's hiting rects position ucording to activatore position"""
        startX= self.ACTIVATOR.x+self.ACTIVATOR.size[0]/2-self.L/2
        startX= (startX//self.L_PERE_GRESE_PART)*self.L_PERE_GRESE_PART

        for i in range(len(self.rects)):
            self.rects[i].x= startX+ i*self.L_PERE_GRESE_PART
            self.rects[i].y= self.F(i*self.L_PERE_GRESE_PART)

    def selfHit(self,blast,damage):
        """called when hitted
        :param blast: 2D vector to append to this character speed
        :param damage: the demege to this character
        :param stanT: how many time from now the stan should be
        :type blast: (int,int) or [int,int]
        :type damage: int
        :type stanT: int"""
        pass

    def hitEnemys(self):
        """hit all the enemys that stand on it"""
        for block in self.rects:
            hited_en=block.isHit(self.ACTIVATOR.enemy.supporters)
            for en in hited_en:
                en.hit((0,0),self.DEMEG_PER_HIT,0)

    def remove(self):
        """distroying itself"""
        self.isActive=False
        for block in self.rects:
            block.isActive=False

from math import*
import pygame
from TheMainGame.for_commands_sending.drawIncreption import*
import TheMainGame.datafiles.imeges
import global_var
import os

class absCaracter:
    """game character without special abilities.
   :param screen: game screen
   :param pNum: the number of the character (1 or 2)
   :param movinator: object that responsible for displaying the animation
   :param comundNumConvent: list to chenge the order of the operation (so instid of op3 will be actived po{comundNumConvent[2]})
   :type screen: surface
   :type pNum: int
   :type movinator: absMovinator
   :type comundNumConvent: int list
   """
    def __init__(self,screen,pNum,movinator,comundNumConvent=[1,2,3,4,5]):
        """there are some helpfull fields and functions that this class ofire to the successors classes (that aren't related to moving the character):
        self.stantimer- show hove many time will the object be in stan
        self.timeFromStart-int that show the time from the sturte of the game (the number of screens that was drawn from the start of the game)
        self.floorLevel- the y of the floor
        self.lastComand- the last comand from ["jump","moveP","moveN","down"] that was down
        self.hp-health points
        self.tickAbleCreatedObjects- all the objects that support this character and it need to do tick() to the (the class doing tick otomatickly)
        self.supporters- all the hitable objects that support the character and the character
        self.enemy- the mane enemy of the character
        self.tickAbleAppend(obj)- append obj to self.tickAbleAppend and toself.supporters if it need to
        self.restHitEnemies(blast,damage,rectTuple)- hit the enemys that in the rectTuple (tupel as it given for the __init__ of the object Rect) with given blast and demeg
        self.onGround()- check is the churucter on ground
        self.comundNumConventF(commundNum)- turn on speshial function with number comundNumConvent[commundNum-1] (will be very helpful to do setings in the future)
        self.stanIt(commundNum)-doing everything that need to be done before every speshial power. return true if the operation dont need to be done.
        """#TODO: check is this commect correct

        self.G=1.6 #gravity
        #given parameters
        self.pNum=pNum
        self.screen=screen
        self.movinator=movinator
        self.size=self.movinator.rectsize
        self.comundNumConvent=comundNumConvent

        #physics parameters
        if pNum==1:
            self.x=120
        else:
            self.x= self.screen.get_width()-self.size[0]-120
        self.y=20
        self.vx=0
        self.vy=0
        self.ay=self.G
        self.ax=0

        self.friction=1.6
        self.floorLevel=600

        #constents for quick change
        self.MOVE_V=12
        self.JUMP_SPEED= -20

        #moving fields
        self.move_v= self.MOVE_V
        self.jump_speed= self.JUMP_SPEED
        

        #other stuff
        self.stantimer=0 #count in frames. the character in stan while self.stantimer>0.
        self.absCartimes= [0]
        #self.absCartimes[0]-last jump time (in frames)
        
        
        self.timeFromStart=0 #in frames
        
        #look directions (needed for special operation)
        self.lastComand=""
        self.lookDirection="moveN"
        self.xDirection="moveN"
        if pNum==1:
            self.lookDirection="moveP"
            self.xDirection="moveP"

        #winning check
        self.isActive=True
        self.hp=100

        #to display or consider
        self.supporters=[self] #all the hitable objects that support the character and the character
        self.semyObjects=[self] #object that similar to the churacter and need to mislead the enemy
        self.tickAbleCreatedObjects=[]
        self.enemy=None

        #for doble jump
        self.airJumpAble=True

        #flags for programer
        self.displayAnimation= True
        self.display_rects= global_var.display_rects
    def tick(self):
        """this function pass 1 frame to this character and the objects created by it, and paint those objects
        NOTE: this function supposed to be called after the special operations actived
        """
        
        self.winningCheck() #check is the second player win
        
        self.movingFizickRools()

        #updating derctions
        if self.lastComand in ["jump","moveP","moveN","down"]:
            self.lookDirection=self.lastComand
        if self.lookDirection in ["moveP","moveN"]:
            self.xDirection=self.lookDirection
        
        #poping not active tickable objects all there lists
        i=0
        while i<len(self.supporters):
            if not self.supporters[i].isActive:
                self.supporters.pop(i)
            else:
                i+=1

        i=0
        while i<len(self.semyObjects):
            if not self.semyObjects[i].isActive:
                self.semyObjects.pop(i)
            else:
                i+=1

        i=0
        while i<len(self.tickAbleCreatedObjects):
            if self.tickAbleCreatedObjects[i].isActive:
                self.tickAbleCreatedObjects[i].tick()
                i+=1
            else:
                self.tickAbleCreatedObjects.pop(i)
        #time updateing
        self.timeFromStart+=1
        #painting
        if self.displayAnimation:
            self.movinator.tick()
            self.size=self.movinator.rectsize
        self.paint()
        self.paramPaint()
        self.resetParam()

        self.stantimer=max(self.stantimer-1,0)
    def winningCheck(self):
        """check does the this character lose. if it is so, the program write the second character as the winner in the winner file
        """
        if self.hp<0:
            f= open("TheMainGame/datafiles/winner.txt","w")
            f.write("player "+str(self.pNum%2+1)+" win")
            f.close()

    def get_aiming_x(self):
        """get aiming x for the enemy
        """
        return self.x

    def get_aiming_y(self):
        """get aiming y for the enemy
        """
        return self.y

    def movingFizickRools(self):
        """update the physics parameters acording to physics rules
        """
        if self.onGround():
            self.airJumpAble=True
        #phithic clculations

        self.x+=self.vx
        self.y+=self.vy
        self.vy+=self.ay
        self.vx+=self.ax

        #if vx is negligible (less then friction), it turn it to 0
        if -self.friction<self.vx<self.friction:
            self.vx=0

        #map limit check

        if self.x<100:
            self.x=100
            self.vx=0
        if self.x+self.size[0]>1400:
            self.x=1400-self.movinator.rectsize[0]
            self.vx=0

        if self.y+self.size[1]>self.floorLevel:
            self.y=600-self.movinator.rectsize[1]
            self.vy=0

        #friction adding
        if self.vx>0:
            self.ax=-self.friction
        elif self.vx<0:
            self.ax=self.friction
        else:
            self.ax=0

    def resetParam(self):
        """reset specific parameters
        """
        self.lastComand=""

        #moving speed parameters reloude
        self.move_v=self.MOVE_V
        self.jump_speed= self.JUMP_SPEED

    def paint(self,isForP1=True,isForP2=True):
        """paint the character
        :param isForP1: does character 1 supposed to see this paint
        :param isForP2: does character 2 supposed to see this paint
        :type isForP1: boolean
        :type isForP2: boolean
        """
        if self.displayAnimation:
            blitIncription(self.movinator.image,(self.x,self.y),isForP1,isForP2)
            
        if self.display_rects:
            rectDrewIncription(self.movinator.color,(self.x,self.y,self.size[0],self.size[1]),10,isForP1,isForP2)
    
    def paramPaint(self,isForP1=True,isForP2=True):
        """paint characters parameters (such as hp)
        :param isForP1: does character 1 supposed to see this paint
        :param isForP2: does character 2 supposed to see this paint
        :type isForP1: boolean
        :type isForP2: boolean
        """
        #hp paint
        hpPos=(120,20) #hp display posizion for player 1
        hpWid=100 #hp display width
        if self.pNum==1:
            blitIncription(prosentRestIncription(self.hp,hpWid,20,(200,200,200)),hpPos,isForP1,isForP2)
        else:
            blitIncription(prosentRestIncription(self.hp,hpWid,20,(200,200,200)),(self.screen.get_width()-hpPos[0]-hpWid,hpPos[1]),isForP1,isForP2)

        textCode=textDrawIncription("comicsansms",30,"You",(0,150,0))
        font = pygame.font.SysFont("comicsansms",30)
        text=font.render("You", True, (0,150,0))
        textRect=text.get_rect()
        textRect.centerx=self.x+self.size[0]/2
        textRect.bottom=self.y-70

        triangleP=((self.x+self.size[0]/2,self.y-10),(textRect.left-10,self.y-60),(textRect.right+10,self.y-60))
        if self.pNum==1:
            polygonIncription((0,0,255),triangleP,0,isForP1,False)
            blitIncription(textCode,textRect.topleft,isForP1,False)
        else:
            polygonIncription((0,0,255),triangleP,0,False,isForP2)
            blitIncription(textCode,textRect.topleft,False,isForP2)

    def moveN(self):
        """make this character walk right
        """
        if self.stantimer!=0:
            return
        
        if self.displayAnimation:
            self.movinator.moveN()
        if -self.move_v<=self.vx<0.1:
            self.vx=-self.move_v
        self.lastComand="moveN"

    def moveP(self):
        """make this character walk left
        """
        if self.stantimer!=0:
            return

        if self.displayAnimation:
            self.movinator.moveP()
        if self.move_v>=self.vx>-0.1:
            self.vx=self.move_v
        self.lastComand="moveP"

    def jump(self):
        """make this character jump
        """
        if self.stantimer!=0:
            return
        self.lastComand="jump"
        if self.timeFromStart-self.absCartimes[0]>10:
            if self.onGround():
                self.absCartimes[0]=self.timeFromStart
                self.vy=self.jump_speed
            elif self.airJumpAble:
                self.absCartimes[0]=self.timeFromStart
                self.vy=self.jump_speed
                self.airJumpAble=False

    def down(self):
        """called when the button down is active
        """
        if self.stantimer!=0:
            return
        self.lastComand="down"


    def hit(self,blast,damage,stanT=5):
        """hit this character
        :param blast: 2D vector to append to this character speed
        :param damage: the demege to this character
        :param stanT: how many time from now the stan should be
        :type blast: (int,int) or [int,int]
        :type damage: int
        :type stanT: int
        """
        self.stantimer=stanT
        self.hp-=damage
        self.vx+=blast[0]
        self.vy+=blast[1]

    def comundNumConventFunc(self,commundNum):
        """chenge the order of the operation acording to self.comundNumConvent
        :param commundNum: the number of the special operation
        :type commundNum: list of ints
        """
        if self.stanIt(self.comundNumConvent[commundNum-1]):
            return
        #ussume that 1<=commundNum<=5
        comunds=[self.op1,self.op2,self.op3,self.op4,self.op5]
        comunds[self.comundNumConvent[commundNum-1]-1]()

    def stanIt(self,commundNum):
        """check does this operation need to be staned
        :param commundNum: the number of the special operation
        :type commundNum: list of ints
        :return: does this operation need to be staned
        :rtype: boolean
        """
        if self.stantimer>0:
            return True
        return False
    def op1(self):
        pass

    def op2(self):
        pass

    def op3(self):
        pass

    def op4(self):
        pass

    def op5(self):
        pass

    def beforeSending(self):
        """this method take place bose mane characters ticked"""
        pass

    #help fuctions
    def tickAbleAppend(self,obj):
        """append obj to tickAble list and to supporters list (if obj can be hitted)
        :param obj: tickAble object
        :type obj: object
        """
        self.tickAbleCreatedObjects.append(obj)
        if hasattr(obj,"hit"):
            self.supporters.append(obj)
    
    def restHitEnemies(self,blast,damage,rectTuple,stan=5): #rect tuple as it insert in pygame.Rect
        """hit all the enemys in the rect
        :param blast: 2D vector to append to this character speed
        :param damage: the demege to this character
        :param stanT: how many time from now the stan should be
        :param rectTuple: rect tuple as used in pygame.Rect init
        :type blast: (int,int) or [int,int]
        :type damage: int
        :type stanT: int
        :param rectTuple: (int,int,int,int)
        """
        #hit all the characters in the rect
        for en in self.enemy.supporters:
            if max(rectTuple[0],en.x)<min(rectTuple[0]+rectTuple[2], en.x+en.size[0]) and max(rectTuple[1],en.y)<min(rectTuple[1]+rectTuple[3], en.y+en.size[1]):
                en.hit(blast,damage,stan)

    def onGround(self):
        """check does this character is on the ground
        :return: does this character is on the ground
        :rtype: boolean
        """
        return self.y+self.movinator.rectsize[1]>=600

    def clockPaint(self,center,r,prosents):
        """drew clock
        :param center: the center of the clock. NOTE: if self.pNum==2, it put the clock on the second side of the screen
        :param r: the radius of the clock
        :param prosents: the prosents of full circle that the clock sow. prosents sowed as a float for example: 0.01 is 1%.if the prosents >1 it so the flout part.
        :type center: (int,int)
        :type r: int
        :type prosents: flout
        """
        
        prosents%=1
        if self.pNum==1:
            drawFilledArcIncription((255,255,255),r, center , -pi/2, 2*pi*prosents-pi/2)
        else:
            drawFilledArcIncription((255,255,255), r, (self.screen.get_width()-center[0],center[1]), -pi/2, 2*pi*prosents-pi/2)

class absMovinator:
    """each character has exactly 1 movinator and only one character has each movinator. this object responsible for displaying the animation.
    :param color: the rect color (for the case that the flag global_var.display_rects is True)
    :param size: the rect size (for the case that the flag global_var.display_rects is True)
    :param imgDir: the path form TheMainGame\images to the directory in which all the images for the charcter
    :param character: the character this movinator belongs to
    :type color: (int,int,int) in the RGB system
    :type size: (int,int)
    :type imgDir: string
    :type character: absCaracter
    """
    def __init__(self,color,size,imgDir,character):
        self.rectsize=size
        self.color=color
        self.imgDir= imgDir #the path to this charcter images directory from TheMainGame\images (relative to programRunner)
        self.c=character
        self.image=imgDir+"/charImg/standN"
        self.times= [-20]*2
        #last time that each of the folowing commands taked place
        #[0]- movingN
        #[1]- movingP
        self.timeStarted= [-20]*2
        #last time that each of the folowing commands stated to taked place
        #[0]- movingN
        #[1]- movingP
        self.t=0
        self.op= None #say which special ops the character did (displaying as the appropriate operation in the movinator), ops init called only when the operation take place
        self.img_indentation= None
        self.oldImg= None

    def imeges_loud(self):
        """loud all the images that in self.imgDir
        """
        #check is self.imgDir is existing directory
        try:
            os.listdir("TheMainGame/images/"+self.imgDir)
        except:
            return
        #start uplouding the images and there indentatins
        added={}
        added_indantation= {}
        toAdd= [self.imgDir]
        i=0
        while i< len(toAdd):
            dotP=toAdd[i].find(".")
            if dotP==-1:
                #toAdd[i] is directory
                directoryLst= os.listdir("TheMainGame/images/"+toAdd[i])
                for f in directoryLst:
                    toAdd.append(toAdd[i]+"/"+f)
            else:
                typeStr= toAdd[i][dotP+1:]
                if typeStr=="png":
                    #toAdd[i] is image
                    added[toAdd[i][:dotP]]= pygame.image.load("TheMainGame/images/"+toAdd[i])
                if toAdd[i][-13:]=="data file.txt":
                    #toAdd[i] is text file with indentations
                    f=open("TheMainGame/images/"+toAdd[i],"r")
                    for line in f:
                        parts= line.split(":")
                        added_indantation[parts[0]]= eval("("+parts[1]+")")
                    f.close()
                if toAdd[i][-18:]=="reference file.txt":
                    #toAdd[i] is file with the referens (names of files that need to lead to the same image)
                    f=open("TheMainGame/images/"+toAdd[i],"r")
                    for line in f:
                        parts= line[:-1].split("-")
                        added[toAdd[i][:-18]+parts[0]]= added[toAdd[i][:-18]+parts[1]]
                        added_indantation[toAdd[i][:-18]+parts[0]]= added_indantation[toAdd[i][:-18]+parts[1]]
                    f.close()
            i+=1
        #upending the uploded images and indentations
        TheMainGame.datafiles.imeges.imegesDict.update(added)
        TheMainGame.datafiles.imeges.img_indentation.update(added_indantation)
        
    def moveN(self):
        """called when the character moving to left. update the image in accordance.
        """
        if self.op==None:
            if self.times[0]!= self.t-1:
                self.timeStarted[0]= self.t
            self.image= self.getFrame(self.imgDir+"/walkN",self.t- self.timeStarted[0])
            self.times[0]= self.t
    def moveP(self):
        """called when the character moving to right. update the image in accordance.
        """
        if self.op==None:
            if self.times[1]!= self.t-1:
                self.timeStarted[1]= self.t
            self.image= self.getFrame(self.imgDir+"/walkP",self.t- self.timeStarted[1])
            self.times[1]= self.t

    def tick(self):
        """path one frame. after this operation its character took the image from the movinator and put it on the screen
        """
        #this function called after buttones check
        #this function appdate the x of self.c so the center (at x) will remine the same
        self.t+=1
        #image updating
        self.image_update()
        #updating filds for working
        self.rectsize= TheMainGame.datafiles.imeges.imegesDict[self.image].get_size()
        if self.img_indentation!=None:
            self.c_x_y_update()
        self.img_indentation= TheMainGame.datafiles.imeges.img_indentation[self.image]
        self.oldImg=self.image

    def image_update(self):
        """do last chenges to the image.in case that some function is writen in self.op, it will be done here.
        """
        if self.op==None:
            if not self.isMoving():
                self.image=self.imgDir+"/charImg/standN"
                if self.c.xDirection=="moveP":
                    self.image=self.imgDir+"/charImg/standP"

            if not self.c.onGround():
                self.image=self.imgDir+"/charImg/onAirN"
                if self.c.xDirection=="moveP":
                    self.image=self.imgDir+"/charImg/onAirP"
                    
            if self.c.stantimer!=0:
                self.image=self.imgDir+"/charImg/hited"
        else:
            self.op()

    def c_x_y_update(self):
        """update the x of self.c so the video will remaind be ok.
        update the y of self.c so character's bottom y will remained the same.
        assume that the self.img_indentation save the indantation at the previous image
        """
        
        self.c.x+= TheMainGame.datafiles.imeges.img_indentation[self.image][0]-self.img_indentation[0]
        oldY= TheMainGame.datafiles.imeges.imegesDict[self.oldImg].get_size()[1]
        newY= TheMainGame.datafiles.imeges.imegesDict[self.image].get_size()[1]
        self.c.y+= oldY- newY
        

    def isMoving(self):
        """check does the character moving
        """
        for x in self.times:
            if x==self.t-1:
                return True
        return False

    #helpfull commands

    def getFrame(self,directory,num,fram_num=-1):
        """return the image of the right frame of the video in the given directory
        :param directory: the directory of the animation
        :param num: the number of the frame
        :param fram_num: the number of frames in whitch put it on loop. so the returned frame would be num%fram_num (if fram_num==-1, this fanction will go according to the file "frames num.txt" in the same directory)
        :type directory: string
        :type num: int
        :type fram_num: int
        :return: the key for the image of the right frame in TheMainGame.datafiles.imeges.imegesDict
        :rtype: string
        """
        #directory never start with /
        if fram_num==-1:
            file= open("TheMainGame/images/"+directory+"/frames num.txt")
            fram_num= int(file.read())
            file.close()
        return directory+"/"+str((num)%fram_num)

class absErrow:
    """this class representslinear errow that disappire when it hit the walls (if you wont another shape of errow, chenge the fanctions: isHit, paint,TochingWalls)
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
    :param length: the length of the errow
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
    """
    # for linear errow (if you wont another shape, chenge the fanctions: isHit, paint,TochingWalls)
    def __init__(self,x,y,maneAnemy,a,destroyTime,v,floorlevel,leftWall,rightWall,blastSize,damege,length): #a-alpha
        self.x=x
        self.y=y
        self.maneAnemy=maneAnemy
        self.L=length
        self.a=a
        self.v=v
        self.distT=destroyTime #destroy time
        self.t=0 #time
        self.isActive=True
        self.fl=floorlevel
        self.lW=leftWall
        self.rW=rightWall
        self.blastSize=blastSize
        self.damege=damege

    def tick(self):
        """this function pass 1 frame to this errow and paint it
        """
        #update the position
        self.x+=self.v*cos(self.a)
        self.y+=self.v*sin(self.a)
        
        #update of case of crasing to wall or floor
        self.TochingWalls()

        #do modolo 2*pi on alpha
        self.a%=2*pi

        #checking for hitting
        en=self.isHit()
        if en!=None:
            self.onHit(en)

        #time update
        if self.t>=self.distT:
            self.isActive=False
        self.t+=1

        #painting
        self.paint()

    def onHit(self,en):
        """called when the errow hit an  enemy
        :param en: the enemy that the errow hits
        :type en: any object with the metode hit(blast,demeg)
        """
        en.hit((self.blastSize*cos(self.a),self.blastSize*sin(self.a)),self.damege)
        self.isActive=False

    def TochingWalls(self):
        """called when the errow hit a wall
        """
        #check is the errow tochs the walls and do somesing related to it (in defolt the arrow will disapire)
        if self.y+self.L*sin(self.a)>self.fl:
            self.isActive=False
            
        if self.x+self.L*cos(self.a)<self.lW:
            self.isActive=False

        if self.x+self.L*cos(self.a)>self.rW:
            self.isActive=False

    def isHit(self):
        """check does the errow hit one of the enemys and which of them
        :return: the enemy that the orrow hits (if it doesn't hit nobody, it return None)
        :rtype: object with the methode hit(blast,demeg,,stanT= number) or None"""
        for en in self.maneAnemy.supporters:
            if abs(self.a%180-pi/2)<0.0001:
                if en.x<self.x<en.x+en.size[0] and max(self.y,en.y)<min(self.y+self.L*sin(self.a), en.y+en.size[1]):
                    return en
            else:
                ds=[(en.x-self.x)/cos(self.a),(en.x+en.size[0]-self.x)/cos(self.a)]
                if not ((ds[0]<0 and ds[1]<0) or (ds[0]>self.L and ds[1]>self.L)):
                    ds=[self.edgesCut(ds[0]),self.edgesCut(ds[1])]
                    if max(min(self.y+ds[0]*sin(self.a),self.y+ds[1]*sin(self.a)),en.y)<=min(max(self.y+ds[0]*sin(self.a),self.y+ds[1]*sin(self.a)), en.y+en.size[1]):
                        return en
        return None

    def edgesCut(self,d):
        #d-the length of the errow for geting to some x
        return min(max(d,0),self.L)

    def paint(self):
        """paint the errow"""
        lineDrewIncription((150,150,150),(self.x,self.y),(self.x+self.L*cos(self.a),self.y+self.L*sin(self.a)))

class hitablePartBlock:
    """root with size wXh that you can hit him and he will send it to the plant. NOTE: this object append itself to the supporters of supportedChar on creeation
    :param parent: its creator object
    :param x: its x
    :param y: its y
    :param w: its w
    :param h: its h
    :param supportedChar: the character that the rect is on his side
    :param saveParam: any thing that you want to save in this object to
    :type parent: hitable object
    :type x: int
    :type y: int
    :type w: int
    :type h: int
    :type supportedChar: absCharacter
    :type saveParam: object (can be list as well)
    """
    
    def __init__(self,parent,x,y,w,h,supportedChar,saveParam=None):
        self.size=(w,h)
        self.x=x
        self.y=y
        self.parent=parent
        self.isActive=True
        self.saveParam=saveParam #some thing that you need to save in the object
        supportedChar.supporters.append(self)
        self.hp=100
    def paint(self):
        """paint this rect"""
        rectDrewIncription((0,255,0),(self.x,self.y,self.size[0],self.size[1]),2)

    def get_aiming_x(self):
        """get aiming x for the enemy
        """
        return self.x

    def get_aiming_y(self):
        """get aiming y for the enemy
        """
        return self.y

    def hit(self,blast,damage,stan=0):
        """called when hited and pass it to self.parent (to the method selfHit)
        :param blast: 2D vector to append to this character speed
        :param damage: the demege to this character
        :param stanT: how many time from now the stan should be
        :type blast: (int,int) or [int,int]
        :type damage: int
        :type stanT: int"""
        self.parent.selfHit(blast,damage)

    def isHit(self,enemys):
        """ check is it hiting one of the enemys
        :param enemys: its enemys
        :return: None -if it dosent hit any object
                 enemy that hited- if hiting
        :rtype: object with the methode hit(blast,demeg,,stanT= number) or None
        """
        ans=[]
        for en in enemys:
            if max(self.x,en.x)<min(self.x+self.size[0], en.x+en.size[0]) and max(self.y,en.y)<min(self.y+self.size[1], en.y+en.size[1]):
                ans.append(en)
        return ans

class plant:
    """plant
    :param x: its x
    :param y: its y
    :param rootSize: this plant will be constracted from rect with size of rootSizeXrootSize
    :param rectsForTick: appended rect in each fram
    :param torningMultiple: before uppending new rect,the plant is turning. the turning angle is torningMultiple*(the angle bitwin the plant and the enemy)
    :param maxT: after that amount of frames, the plant disapire
    :param parent: its creator
    :param dxForRect: the length that it move forword before the next rect
    :param selfDemegMultipel: the multiple that the hit operation doing for the demege
    :param hitingDamage: the demeg that the plant doing to the enemy on hit
    :param blastSize: the size of the blast when hitting the enemy
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
    :type hitingDamage: flout
    :type blastSize: flout
    :type turgetInd: int
    """
    def __init__(self,x,y,rootSize,rectsForTick,torningMultiple,maxT,parent,dxForRect,selfDemegMultipel,hitingDamage,blastSize,turgetInd): 
        self.a=-pi/2 #the angle relative to the x axis
        self.x=x
        self.y=y

        self.speed=rectsForTick
        self.torningMultiple=torningMultiple #omega
        self.maxT=maxT
        self.parent=parent
        self.dxForRect=dxForRect
        self.rootSize=rootSize
        self.selfDemegMultipel=selfDemegMultipel
        self.hitingDamage=hitingDamage
        self.blastSize=blastSize
        self.turgetInd=turgetInd

        self.isActive=True
        self.plantBlocks=[]
        self.hp=100
        self.time=0

        self.miny=y
        self.xSum=0

    def tick(self):
        """this function pass 1 frame to this plant and paint it
        """
        try:
            self.parent.enemy.supporters[self.turgetInd]
        except:
            #print("my enemy is out")
            self.hp=-1
            self.isActiveUpdate()
            return
        
        self.time+=1
        self.growing()

        self.hitEnemys()
        self.isActiveUpdate()
        self.hitPpaint()
        self.paramPaint()

    def growing(self):
        """grow self.speed aditional rects.
        """
        turgetP=self.turget()
        for i in range(self.speed):
            self.plantBlocks.append(hitablePartBlock(self,self.x,self.y,self.rootSize,self.rootSize,self.parent,self.a)) #uppands the new rect to all the enemys

            #update all moving parameters
                
            self.x+=self.dxForRect*cos(self.a)
            self.y+=self.dxForRect*sin(self.a)
            angleToTurget=(atan2(turgetP[1]-self.y,turgetP[0]-self.x)-self.a)%(2*pi)
            self.a+=self.torningMultiple*(pi-angleToTurget)
                
            if self.y<self.miny:
                self.miny=self.y
            self.xSum+=self.x

    def paramPaint(self):
        """paint this plant's parameters"""
        hpRectCode=prosentRestIncription(self.hp,100,20,(100,100,100))
        blitIncription(hpRectCode,(self.xSum/len(self.plantBlocks)-50,self.miny-30))

    def hitEnemys(self):
        """hit all the enemy that the plant touch"""
        blastSum=[0,0]
        blast=self.blastSize
        hitedEnemys=[]
        blastsSum=[]
        blastsCount=[]
        for block in self.plantBlocks:
            en=block.isHit(self.parent.enemy.supporters)
            if en!=[]:
                en=en[0]
                if en in hitedEnemys:
                    if block in self.plantBlocks[-5:]:
                        blastsSum[enInd][0]+= blast*cos(block.saveParam)
                        blastsSum[enInd][1]+= blast*sin(block.saveParam)
                        blastsCount[enInd]+=1
                        continue
                else:
                    enInd=len(hitedEnemys)
                    hitedEnemys.append(en)
                    blastsSum.append([0,0])
                    blastsCount.append(0)

                hitEnemy=en
                turgetP=(en.x+en.size[0]/2,en.y+en.size[0]/2)
                angleToTurget=(atan2(turgetP[1]-block.y,turgetP[0]-block.x)-block.saveParam)%(2*pi)
                if angleToTurget>pi:
                    blastA=block.saveParam-pi/2 #blast angle
                else:
                    blastA=block.saveParam+pi/2
                blastsSum[enInd][0]+=blast*cos(blastA)
                blastsSum[enInd][1]+=blast*sin(blastA)
                blastsCount[enInd]+=1

        for i in range(len(hitedEnemys)):
            hitedEnemys[i].hit((blastsSum[i][0]/blastsCount[i],blastsSum[i][1]/blastsCount[i]),self.hitingDamage)

    def isActiveUpdate(self):
        """check does the plant need to be exzist and distroy it (and all its blockes) if not"""
        if self.hp<=0 or self.time>self.maxT:
            self.isActive=False
            for block in self.plantBlocks:
                block.isActive=False

    def hitPpaint(self):
        """paint itself"""
        for block in self.plantBlocks:
            block.paint()
        
    def selfHit(self,blast,damage):
        """called when hitted
        :param blast: 2D vector to append to this character speed
        :param damage: the demege to this character
        :param stanT: how many time from now the stan should be
        :type blast: (int,int) or [int,int]
        :type damage: int
        :type stanT: int"""
        self.hp-=damage*self.selfDemegMultipel
        for block in self.plantBlocks:
            block.hp= self.hp

    def turget(self):
        """get the courdinate of the target
        :return: the courdinate of the target
        :rtype: (flout,flout)"""
        
        return (self.parent.enemy.supporters[self.turgetInd].get_aiming_x()+self.parent.enemy.supporters[self.turgetInd].size[0]/2,
                self.parent.enemy.supporters[self.turgetInd].get_aiming_y())

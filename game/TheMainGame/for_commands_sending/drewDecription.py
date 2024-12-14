from TheMainGame.for_commands_sending.drawFunctions import*
from usefull_classes.veriable_eval import type_eval
import TheMainGame.datafiles.imeges
import global_var

def decription(screen,string):
    """doing decription to one UDP mesege (which parpose is to drew one frame) according to the protocol betwin two claints.
    :param screen: the game screen
    :param string: the mesege
    :type screen: pygame.surface
    :type string: string"""
    commandLst=string.split("\n")

    try:
        for command in commandLst:
            singelCommandIncription(screen,command)
    except:
        print(string)
        raise Exception

def singelCommandIncription(screen,commandStr):
    """doing decription (do what it says) to one command according to the protocol betwin two claints. if it gets line with command inside command, it doing them bose
    :param screen: the game screen
    :param commandStr: the command
    :type screen: pygame.surface
    :type commandStr: string"""
    if commandStr=="":
        return

    if commandStr[:4]==".re ":
        return singelCommandIncription(screen,commandStr[4:].replace(":","|"))
    
    commandParts=commandStr.split("|")
    if commandParts[0]=="DFA":
        #the incription form: "DFA|"+str(color)+"|"+str(r)+"|"+str(center)+"|"+str(stA)+"|"+str(endA)+"\n"
        #comand stracture: drawFilledArc(screen,color,r,center,stA,endA)
        drawFilledArc(screen,type_eval(commandParts[1]),type_eval(commandParts[2]),type_eval(commandParts[3]),type_eval(commandParts[4]),type_eval(commandParts[5]))
        return
    if commandParts[0]=="ICI":
        #the incription form: ".re ICI:"+str(r)+":"+str(prosents)+":"+imageName
        #comand stracture: imegedClockImg(r,prosents,imageName)
        return imegedClockImg(type_eval(commandParts[1]),type_eval(commandParts[2]),commandParts[3])
    if commandParts[0]=="PR":
        #the incription form: ".re PR:"+str(prosent)+":"+str(width)+":"+str(hight)+":"+str(color)
        #comand stracture: prosentRest(prosent,width,hight,color)
        return prosentRest(type_eval(commandParts[1]),type_eval(commandParts[2]),type_eval(commandParts[3]),type_eval(commandParts[4]))
    if commandParts[0]=="RDUZ":
        #the incription form: "RD|"+str(color)+"|"+str(rectTuple)+"|"+str(width)+"\n"
        #comand stracture: pygame.draw.rect(surface, color, rect, width=0)
        size= type_eval(commandParts[3])
        pos= type_eval(commandParts[4])
        pygame.draw.rect(screen,type_eval(commandParts[1]),pygame.Rect(pos[0],pos[1],size[0],size[1]),type_eval(commandParts[2]))
        return
    if commandParts[0]=="RDZ":
        #the incription form: "RD|"+str(color)+"|"+str(rectTuple)+"|"+str(width)+"\n"
        #comand stracture: pygame.draw.rect(surface, color, rect, width=0)
        size= type_eval(commandParts[3])
        positions= type_eval(commandParts[4])
        for pos in positions:
            pygame.draw.rect(screen,type_eval(commandParts[1]),pygame.Rect(pos[0],pos[1],size[0],size[1]),type_eval(commandParts[2]))
        return
    if commandParts[0]=="CD":
        #the incription form: "CD|"+str(color)+"|"+str(r)+"|"+str(center)+"\n"
        #comand stracture: pygame.draw.circle(surface, color, center, radius)
        pygame.draw.circle(screen,type_eval(commandParts[1]),type_eval(commandParts[3]),type_eval(commandParts[2]))
        return
    if commandParts[0]=="LD":
        #the incription form: "LD|"+str(color)+"|"+str(start_pos)+"|"+str(end_pos)+"|"+str(width)+"\n"
        #comand stracture: pygame.draw.line(surface, color, start_pos, end_pos, width=1)
        pygame.draw.line(screen,type_eval(commandParts[1]),type_eval(commandParts[2]),type_eval(commandParts[3]),type_eval(commandParts[4]))
        return
    if commandParts[0]=="P":
        #the incription form: "P|"+str(color)+"|"+str(points)+"|"+str(width)+"\n"
        #comand stracture: pygame.draw.polygon(surface, color, points, width=0)
        pygame.draw.polygon(screen,type_eval(commandParts[1]),type_eval(commandParts[2]),type_eval(commandParts[3]))
        return
    if commandParts[0]=="TD":
        #the incription form: "TD|"+str(fontName)+"|"+str(fontNum)+"|"+str(text)+"|"+str(color)+"\n"
        font = pygame.font.SysFont(commandParts[1], type_eval(commandParts[2]))
        return font.render(commandParts[3], True, type_eval(commandParts[4]))
    if commandParts[0]=="RFSC":
        #the incription form: ".re FSC:"+str(size)+":"+str(color)
        surface=pygame.Surface(type_eval(commandParts[1])).convert_alpha()
        surface.fill(type_eval(commandParts[2]))
        return pygame.transform.rotate(surface,type_eval(commandParts[3]))
    if commandParts[0]=="RRI":
        #the incription form: ".re FSC:"+str(size)+":"+str(color)
        image=commandParts[1]
        if image[:4]==".re ":
            image=singelCommandIncription(screen,image)
        else:
            image=TheMainGame.datafiles.imeges.imegesDict[image]
        size_m= type_eval(commandParts[2])
        image= pygame.transform.scale(image,(size_m[0]*image.get_size()[0],size_m[1]*image.get_size()[1]))
        return pygame.transform.rotate(image,type_eval(commandParts[3]))
    if commandParts[0]=="B":
        #the incription form: "B|"+imageSrc+"|"+str(pos)+"\n"
        #comand stracture: screen.blit(image,pos)
        image=commandParts[1]
        if image[:4]==".re ":
            image=singelCommandIncription(screen,image)
        else:
            image=TheMainGame.datafiles.imeges.imegesDict[image]

        try:
            screen.blit(image,type_eval(commandParts[2]))
        except:
            global_var.done= True
            print(commandParts)
            raise Exception
        return
    
    print("incription error in the comand:"+commandStr)

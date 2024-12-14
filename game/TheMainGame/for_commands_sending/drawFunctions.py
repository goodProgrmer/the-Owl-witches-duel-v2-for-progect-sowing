import pygame
from math import*
import TheMainGame.datafiles.imeges

def drawFilledArc(screen,color,r,center,stA,endA):
    """draw filled with solid color arc that start on angle stA and end in endA
    :param screen: game screen
    :param color: filling color
    :param r: arc rudios
    :param center: arc center
    :param stA: the start angle of the arc according to x axis
    :param endA: the start angle of the arc according to x axis
    :type screen: pygame.surface
    :type color: RGB
    :type r: float
    :type center: (int,int)
    :type stA: float
    :type endA: float"""
    if pi-0.0001<=(endA-stA+pi)%(2*pi)<=pi+0.0001:
        pygame.draw.circle(screen,color,center,r)
        return
    #r-radios
    #stA- start angle
    #endA- end angle
    points=[center]
    for i in range(int((endA-stA)/(pi/45))+1):
        points.append((center[0]+r*cos(stA+i*pi/45),center[1]+r*sin(stA+i*pi/45)))
    points.append((center[0]+r*cos(endA),center[1]+r*sin(endA)))
    pygame.draw.polygon(screen,color,points)

def imegedClockImg(r,prosents,imageName):
    """return paint of clock with clock hand that turned to show the given prosent of the rect (0 is agenst y axis). it use the image as clock.
    :param r: clock rudios: (resize the image to fit the radios)
    :param prosents: the prosent of circle that the clock hand need to sow. 50% will be when prosent=0.5
    :param imageName: path to the image from wich the clock will be made
    :type r: float
    :type prosents: float
    :type imageName: string
    :return: the image described below
    :rtype: pygame.surface"""
    image=TheMainGame.datafiles.imeges.imegesDict[imageName]
    image= pygame.transform.scale(image,(2*r,2*r))
    prosents%=1
    imageSize= image.get_size()
    clockedImage=image.copy()
    if 0.0001<prosents<2*pi-0.0001:
        drawFilledArc(clockedImage,(50,50,50),r,(imageSize[0]/2,imageSize[1]/2),-pi/2-(1-prosents)*2*pi,-pi/2)
    clockedImage.set_alpha(200)
    #image=clockedImage
    image.blit(clockedImage,(0,0))
    return image

def prosentRest(prosent,width,hight,color):
    """return surface in which there is rect which length sow the prosent
    :param prosent: the prosent of the rect that will be filled. 50% will be when prosent=50.
    :param width: width of the surface
    :param hight: hight of the surface
    :param color: filling color of the prosent rect
    :type prosent: float
    :type width: float
    :type hight: float
    :type color: (int,int,int)
    :return: the surface described below
    :rtype: pygame.surface"""
    rect= pygame.Surface((width, hight))
    rect.fill((150,150,150))
    prosentRect=pygame.Surface((max(int(0.8*width*(prosent/100)),0), int(0.8*hight)))
    prosentRect.fill(color)
    rect.blit(prosentRect,(int(0.1*width),int(0.1*hight)))
    return rect

from PIL import Image
import os

def whiteLineErase(mat,w,h,start_p=(0,1),alredy_checked= {}):
    directions=((1,0),(0,1),(-1,0),(0,-1))
    to_check= [start_p]
    to_chenge= []
    max_len= 1
    while len(to_check)!=0:
        point= to_check.pop(-1)
        if 0<=point[0]<w and 0<=point[1]<h and (not point in alredy_checked) and mat[point[0],point[1]][3]==0:
            for direct in directions:
                to_check.append((point[0]+direct[0],point[1]+direct[1]))
        elif 0<=point[0]<w and 0<=point[1]<h and (not point in alredy_checked):
            to_chenge.append(point)
        
        if len(to_check)>max_len:
            max_len= len(to_check)
        alredy_checked[point]= True
    print(max_len)

    for p in to_chenge:
        mat[p[0],p[1]]= (255,255,255,0)

    return alredy_checked

def full_whiteLineErase(mat,w,h):
    alredy_checked= {}
    for x in range(w):
        for y in range(h):
            if mat[x,y][3]==0 and (not (x,y) in alredy_checked):
                alredy_checked= whiteLineErase(mat,w,h,(x,y),alredy_checked)


def img_update(file):
    file= (file).replace("\\","/") #get the path to the file
    #getting image matrix
    im = Image.open(file+".png")
    w, h = im.size
    mat= im.load()
    full_whiteLineErase(mat,w,h)

    #save the output image
    im.save(file+".png")

def dirupdate(toUpdate):
    i=0
    while i< len(toUpdate):
        dotP=toUpdate[i].find(".")
        if dotP==-1:
            #toAdd[i] is directory
            try:
                #print(toUpdate[i])
                directoryLst= os.listdir(toUpdate[i])
                for f in directoryLst:
                    toUpdate.append(toUpdate[i]+"/"+f)
                #print(toUpdate)
            except Exception as e:
                print(e)
        else:
            typeStr= toUpdate[i][dotP+1:]
            if typeStr=="png":
                img_update(toUpdate[i][:dotP])
        i+=1
dirupdate(["emity"])

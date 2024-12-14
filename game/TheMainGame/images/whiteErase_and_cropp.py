from PIL import Image
import os

def cropingRact(mat,w,h):
    """return the rect that you need to crop to throw out the empty space
    :param mat: image matrix after the earasing of white color
    :param w: image width
    :param h: image hight
    :type mat: matrix of the image. any cell is from RGBA type
    :type w: int
    :type h: int"""
    minY= h
    maxY= -1
    minX= w
    maxX= -1
    
    for y in range(1,h):
        if not is_empty_line(mat,(1,0),(1,y),w-1,h-1):
            minY= y
            break
    
    for y in range(h-2,-1,-1):
        if not is_empty_line(mat,(1,0),(1,y),w-1,h-1):
            maxY= y
            break
    
    for x in range(1,w):
        if not is_empty_line(mat,(0,1),(x,1),w-1,h-1):
            minX= x
            break
    
    for x in range(w-2,-1,-1):
        if not is_empty_line(mat,(0,1),(x,1),w-1,h-1):
            maxX= x
            break

    return (minX,minY,maxX-minX+1,maxY-minY+1)

def is_empty_line(mat,direction,startP,w,h):
    """check is line that starts in startP and go in given derction empty (the alpha of every cell in it is 0)
    :param mat: image matrix after the earasing of white color
    :param direction: the given direction
    :param startP: given start point
    :param w: image width
    :param h: image hight
    :type direction: (int,int)
    :type startP: (int,int)
    :type w: int
    :type h: int
    :return: is line that starts in startP and go in given derction empty (the alpha of every cell in it is 0)
    :rtype: bool"""
    i=0
    x,y=startP
    
    while x<w and y<h:
        #print(x,y,mat[x,y][3],startP)
        if mat[x,y][3]!=0:
            return False
        i+=1
        x,y=(startP[0]+direction[0]*i,startP[1]+direction[1]*i)
    return True

def whiteErase(mat,new_matt,w,h):
    """set all the pixels in new_matt to be the same as mat, just when the pixel in mat is white, it gives it alpha 0, and in any other case alpha=1
    :param mat: image matrix before the earasing of white color
    :param new_mat: matrix in the same size as mat with 4 places in each place
    :param w: image width
    :param h: image hight
    :type mat: matrix of the image. any cell is from RGBA type
    :type new_matt: matrix.any cell is from RGBA type
    :type w: int
    :type h: int"""
    for x in range(w):
        for y in range(h):
            if tupleLarger(mat[x,y],(250,250,250,-1)):
                new_matt[x,y]= (255,255,255,0)
            else:
                new_matt[x,y]= (mat[x,y][0], mat[x,y][1], mat[x,y][2],255)

def copy_mat(mat,new_matt,w,h):
    """copy mat to new_matt.
    :param mat: image matrix before the earasing of white color
    :param new_mat: matrix in the same size as mat
    :param w: image width
    :param h: image hight
    :type mat: matrix of the image. any cell is from RGBA type
    :type new_matt: matrix.any cell is from RGBA type
    :type w: int
    :type h: int"""
    for x in range(w):
        for y in range(h):
            new_matt[x,y]= mat[x,y]

def dfs_whiteErase(new_matt,w,h,start_p=(0,1)):
    """set all the pixels in new_matt to be the same as mat, just when the pixel in mat is white and has path through whight pixels to pixel (0,1),
    it gives it alpha 0, and in any other case alpha=1
    :param mat: image matrix before the earasing of white color
    :param new_mat: matrix in the same size as mat with 4 places in each place
    :param w: image width
    :param h: image hight
    :type mat: matrix of the image. any cell is from RGBA type
    :type new_matt: matrix.any cell is from RGBA type
    :type w: int
    :type h: int"""
    directions=((1,0),(0,1),(-1,0),(0,-1))
    to_check= [start_p]
    max_len= 1
    while len(to_check)!=0:
        point= to_check.pop(-1)
        if 0<=point[0]<w and 0<=point[1]<h and new_matt[point[0],point[1]][3]!=0 and tupleLarger(new_matt[point[0],point[1]],(250,250,250,0)):
            new_matt[point[0],point[1]]= (255,255,255,0)
            for direct in directions:
                to_check.append((point[0]+direct[0],point[1]+direct[1]))
        if len(to_check)>max_len:
            max_len= len(to_check)
    print(max_len)


def dfs_full_whiteErase(mat,new_matt,w,h):
    copy_mat(mat,new_matt,w,h)
    for x in range(w):
        for y in range(h):
            if tupleLarger(new_matt[x,y],(255,255,255,1)):
                dfs_whiteErase(new_matt,w,h,(x,y))

def tupleLarger(tup1,tup2):
    """check is any value in tup1>=the calu in tup2 in the same index. NOTE: this function usumes len(tup1)=len(tup2)
    :param tup1: given tup1 (explained in first line of the description)
    :param tup2: given tup2 (explained in first line of the description)
    :type tup1: tuple of floats
    :type tup2: tuple of floats"""
    #check is tup1>=tup2
    if len(tup1)!=len(tup2):
        raise Exception("error")
    
    for i in range(len(tup1)):
        if tup1[i]<tup2[i]:
            return False
    return True

def copyCroped(mat,new_matt,w,h,cropeTuple):
    """copy the crop purt of the given mat to new_matt.
    :param mat: image matrix
    :param new_matt: matrix in the size of the crop part of mat
    :param w: image width
    :param h: image hight
    :param cropeTuple: the part it need to crop from mat in the folowing format: (start x index, start y index, width, hight)
    :type mat: matrix
    :type new_matt: matrix
    :type w: int
    :type h: int
    :type cropeTuple: (int,int,int,int)"""
    for x in range(cropeTuple[2]):
        for y in range(cropeTuple[3]):
            new_matt[x,y]= mat[x+cropeTuple[0], y+cropeTuple[1]]

def updateImg(dirctory,file,dfs_full_erase=True):
    """get jpg image in the given directory with the given file name, erase the white pixels, crop the empty spaces from the sides and save it as png image with the same
    name and directory.apdate the data file.txt file with its indentation as well.
    :param dirctory: the given directory
    :param file: the given file. it don't include type ending
    :type dirctory: string
    :type file: string"""
    file= (dirctory+"/"+file).replace("\\","/") #get the path to the file
    #getting image matrix
    im = Image.open(file+".png")
    w, h = im.size
    mat= im.load()
    #erase the white partes
    mid_img= Image.new('RGBA', (w, h), (0,0,255,1))
    mid_mat= mid_img.load()
    if dfs_full_erase:
        dfs_full_whiteErase(mat,mid_mat,w,h)
    else:
        copy_mat(mat,new_matt,w,h)
        dfs_whiteErase(new_matt,w,h)
    #crop the matrix
    cropping_tuple= cropingRact(mid_mat,w,h)
    ans= Image.new('RGBA', (cropping_tuple[2], cropping_tuple[3]), (0,0,0,0))
    ans_mat= ans.load()
    copyCroped(mid_mat,ans_mat,w,h,cropping_tuple)

    #save the output image
    ans.save(file+".png")
    #apdate data file
    f= open(dirctory+"/data file.txt","a")
    f.write(file+":"+str(cropping_tuple[0])+","+str(cropping_tuple[1])+"\n")
    f.close()

def dirupdate(directory,use_dfs_erase=False):
    """doing updateImg function for any jpg image in given directory.
    :param directory: the given directory
    :type directory: string"""
    to_update= os.listdir(directory)
    for f in to_update:
        if f[-4:]==".png":
            updateImg(directory,f[:-4],use_dfs_erase)

import cv2
import miror_derectory
import whiteErase_and_cropp
import hight_normalization
import indent_normalization
from PIL import Image, ImageChops
import os

def videoToFram(file):
    """deviding video to frames and save them as jpg images. NOTE: it saves all the frames in new directory with the same name and directory as the file.
    :param file: the path to the file to divide. NOTE: the file need to be mp4 file and this paramter don't need to includ the ending .mp4
    :type file: string"""
    capture = cv2.VideoCapture(file+".mp4")

    os.mkdir(file)

    frNum=0
    cont=True

    while cont:
        cont, frame = capture.read()
        if cont:
            cv2.imwrite(file+"\\"+str(frNum)+".jpg", frame)
            frNum+=1

    capture.release()
    f=open(file+"\\frames num.txt","w")
    f.write(str(frNum))
    f.close()
    zip_dir(file)

def videoToFramR(file):
    """deviding video to frames in the revers order (the last frame will be saved as the first) and save them as jpg images.
    NOTE: it saves all the frames in new directory with the same name and directory as the file.
    :param file: the path to the file to divide. NOTE: the file need to be mp4 file and this paramter don't need to includ the ending .mp4
    :type file: string"""
    fram_num= int(input("fram num (enter -1 to return): "))
    if fram_num==-1:
        return
    
    capture = cv2.VideoCapture(file+".mp4")

    os.mkdir(file)

    frNum=0
    cont=True

    while cont:
        cont, frame = capture.read()
        if cont:
            cv2.imwrite(file+"\\"+str(fram_num-frNum-1)+".jpg", frame)
            frNum+=1

    capture.release()
    f=open(file+"\\frames num.txt","w")
    f.write(str(frNum))
    f.close()

def rename(directory):
    """rename the frames in the directory from the tool format to my programs format (for example from "frame000000000000.jpg" to "0.jpg").
    it appends file "frames num.txt" with the correct info as well
    :param directory:  path to the directory of the frames
    :type directory: string"""
    directory=directory.replace("\\","/")
    f=0
    try:
        while True:
            os.rename(directory+"/frame"+tolength(str(f),12)+'.png', directory+"/"+str(f)+'.png')
            f+=1
    except Exception as e:
        print(e)

    file=open(directory+"/frames num.txt","w")
    file.write(str(f))
    file.close()

def tolength(string,length):
    return "0"*(length-len(string))+string

def compere_mats(info1,info2):
    """compare mut of 2 images to say does they equel
    :param info1: (mat of image 1, width of image 1, hight  of image 1)
    :param info2: (mat of image 2, width of image 2, hight  of image 2)
    :type info1: tuple
    :type info2: tuple
    :return: does 2 muts equel
    :rtype: boolean"""
    #info= (mat,w,h)
    mat1,w1,h1= info1
    mat2,w2,h2= info2
    if w1!=w2 or h1!=h2:
        return False
    ans=True
    for x in range(w1):
        for y in range(h1):
            if mat1[x,y]!=mat2[x,y]:
                #print(mat1[x,y],mat2[x,y],x,y,"pppp")
                #ans= False
                return False
    return ans

def zip_dir(directory):
    """zipping frames directory by deleting dupliced images and puting referense to them in "reference file.txt" in the same directorry
    :param directory:  path to the directory of the frames
    :type directory: string"""
    #NOTE: this file compress only jpg images to each other
    directory= directory.replace("\\","/")
    list_dir= os.listdir(directory)
    checked_img_info= []
    checked_img_names= []
    append_string= ""
    for f in list_dir:
        if f[-4:]==".png":
            im = Image.open(directory+"/"+f)
            info= (im.load(),im.size[0],im.size[1])
            name= f[:-4]
            #print(f,info[1],info[2])
            #print(checked_img_info)
            check_result= True #has the image alredy sowed in the directory (True if not)
            for i in range(len(checked_img_info)):
                ans= compere_mats(checked_img_info[i],info)
                #print(ans)
                if ans:
                    os.remove(directory+"/"+f)
                    append_string+=name+"-"+checked_img_names[i]+"\n"
                    check_result=False
                    break
            
            if check_result:
                checked_img_info.append(info)
                checked_img_names.append(name)

    if append_string!="":
        f= open(directory+"/reference file.txt", "a")
        f.write(append_string)
        f.close()

def main():
    #constants:
    unregular_white_erase= True
    """give easy way to call all subfanctions"""
    print("""avileble inputs:
e- exit
v- videoToFram
vr- videoToFramR
rn- rename video derictory from grufic tool format to my program format
md- miror firectory
mf- miror image
cd- crop directory
cf- crop image
hn- high normalization
hnf- high normalization by first
in- indent normalization
z- zip directory by merging frames
vhs- video handeling shortcut
mvhs- mirror video handeling shortcut""")
    t= input("input: ")
    while t!="e":
        print("excpect files and directorys without type end (.)")
        if t=="v":
            f= input("file: ")
            videoToFram(f)
        elif t=="vr":
            f= input("file: ")
            videoToFramR(f)
        elif t=="rn":
            d= input("directory: ")
            rename(d)
        elif t=="md":
            f= input("directory: ")
            miror_derectory.dirupdate(f)
        elif t=="mf":
            f= input("file: ")+".jpg"
            miror_derectory.updateImg(f)
        elif t=="cd":
            #from the moment it was done, its derectory name can't chenge
            f= input("directory: ")
            whiteErase_and_cropp.dirupdate(f)
        elif t=="cf":
            #from the moment it was done, its derectory name can't chenge
            d= input("directory: ")
            f= input("file: ")
            whiteErase_and_cropp.updateImg(d,f,unregular_white_erase)
        elif t=="hn":
            f= input("directory: ")
            h=int(input("h: "))
            hight_normalization.dirupdate(f,h)
        elif t=="hnf":
            f= input("directory: ")
            h=int(input("h: "))
            hight_normalization.dirupdate_by_first(f,h)
        elif t=="in":
            d= input("directory: ")
            indent_normalization.normalize_x_indent(d)
        elif t=="z":
            d= input("directory: ")
            zip_dir(d)
        elif t=="vhs":
            d= input("directory: ")
            h=int(input("h: "))
            rename(d)
            print("renamed")
            zip_dir(d)
            print("ziped")
            whiteErase_and_cropp.dirupdate(d,unregular_white_erase)
            print("cropped")
            hight_normalization.dirupdate_by_first(d,h)
            print("h normalized")
            indent_normalization.normalize_x_indent(d)
        elif t=="mvhs":
            d= input("directory: ")
            h=int(input("h: "))
            rename(d)
            print("renamed")
            zip_dir(d)
            print("ziped")
            miror_derectory.dirupdate(d)
            print("mirrored")
            whiteErase_and_cropp.dirupdate(d,unregular_white_erase)
            print("cropped")
            hight_normalization.dirupdate_by_first(d,h)
            print("h normalized")
            indent_normalization.normalize_x_indent(d)
            
        print("""avileble inputs:
e- exit
v- videoToFram
vr- videoToFramR
rn- rename video derictory from grufic tool format to my program format
md- miror firectory
mf- miror image
cd- crop directory
cf- crop image
hn- high normalization
in- indent normalization
z- zip directory by merging frames
vhs- video handeling shortcut
mvhs- mirror video handeling shortcut""")
        t= input("input: ")

if __name__=="__main__":
    main()

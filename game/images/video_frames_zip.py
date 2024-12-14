import os
from PIL import Image, ImageChops

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
            for i in range(3):
                if abs(mat1[x,y][i]-mat2[x,y][i])>3:
                    #ans=False
                    #print(mat1[x,y][i]-mat2[x,y][i])
                    return False
    return ans

def zip_video_dir(directory):
    """zipping frames directory by deleting dupliced images and puting referense to them in "reference file.txt" in the same directorry
    :param directory:  path to the directory of the frames
    :type directory: string"""
    #NOTE: this file compress only jpg images to each other
    directory= directory.replace("\\","/")
    list_dir= os.listdir(directory)
    checked_img_info= []
    checked_img_names= []
    append_string= ""
    files_count=0
    for i in range(len(list_dir)):
        f= str(i)+".jpg"
        #print(f,list_dir)
        if f in list_dir:
            print(int(files_count*100/len(list_dir)),f)
            im = Image.open(directory+"/"+f)
            info= (im.load(),im.size[0],im.size[1])
            name= f[:-4]
            #print(f,info[1],info[2])
            #print(checked_img_info)
            check_result= True #has the image alredy sowed in the directory (True if not)
            for i in range(len(checked_img_info)-1,-1,-1):
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
            print(check_result)
        files_count+=1

    f= open(directory+"/reference file.txt", "a")
    f.write(append_string)
    f.close()

zip_video_dir("intro")

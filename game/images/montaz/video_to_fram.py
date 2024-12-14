import cv2
import os
import shutil

def videoToFram(file):
    """deviding video to frames and save them as jpg images. NOTE: it saves all the frames in new directory with the same name and directory as the file.
    :param file: the path to the file to divide. NOTE: the file need to be mp4 file and this paramter don't need to includ the ending .mp4
    :type file: string"""
    shutil.rmtree(file, True)
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


def main():
    videoToFram("emity")
    videoToFram("willow")

if __name__=="__main__":
    main()

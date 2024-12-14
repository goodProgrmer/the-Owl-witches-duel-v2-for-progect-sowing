import cv2
import os

file="temp"

frameSize = (1500, 800)

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter(file+".mp4",fourcc, 30, frameSize)

i=0
while os.path.exists(file+"/"+str(i)+".jpg"):
    #print(file+"/"+str(i)+".jpg")
    img = cv2.imread(file+"/"+str(i)+".jpg")
    print(file+"/"+str(i)+".jpg")
    out.write(img)
    i+=1

out.release()

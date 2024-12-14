from PIL import Image
import os

f="vika intro"
frame_num= 5

frameSize = (2272, 1280)

for i in range(frame_num):
    #print(file+"/"+str(i)+".jpg")
    im = Image.open(f+"/"+str(i)+".jpg")
    ans= im.resize(frameSize)
    ans.save(f+"/"+str(i)+".jpg")

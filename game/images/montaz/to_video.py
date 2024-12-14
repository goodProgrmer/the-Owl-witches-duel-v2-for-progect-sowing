import cv2

file="vika intro"
f=open(file+"/frames num.txt", "r")
frame_num= int(f.read())
f.close()

frameSize = (906, 922)

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter(file+".mp4",fourcc, 30, frameSize)

frame_multiple= 5
frame_num*= frame_multiple

for i in range(frame_num):
    #print(file+"/"+str(i)+".jpg")
    img = cv2.imread(file+"/"+str(i//frame_multiple)+".jpg")
    print(file+"/"+str(i//frame_multiple)+".jpg")
    out.write(img)

out.release()

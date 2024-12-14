import shutil

directory= "hunter"
src= directory+"/0.jpg"
length= 30

for i in range(1,length):
    shutil.copy(src, directory+"/"+str(i)+".jpg")

f= open(directory+"/frames num.txt", "w")
f.write(str(length))
f.close()

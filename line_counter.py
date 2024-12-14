import os

def line_counter(toAdd):
    ans=0
    i=0
    c=0
    c2=0
    f_c=0
    ans2=0
    ans3 = 0
    while i< len(toAdd):
        dotP=toAdd[i].find(".")
        if dotP==-1:
            #toAdd[i] is directory
            try:
                directoryLst= os.listdir(toAdd[i])
                for f in directoryLst:
                    toAdd.append(toAdd[i]+"/"+f)
                c+=1
            except:
                pass
        else:
            typeStr= toAdd[i][dotP+1:]
            if typeStr=="py":
                f=open(toAdd[i],"r")
                file= f.read()
                f.close()
                ans+= file.count("\n")
                ans2+= file.count("\nclass ")
                f_c+= file.count("def ")
                c2+=1
            elif typeStr in ("png","jpg","jpeg"):
                ans3 += 1
        i+=1
    print("lines:",ans,"\ndirectorys:",c,"\nfiles:",c2,"\nclasses:",ans2,"\nfunctions:",f_c,"\npictures:",ans3)

line_counter(["server","the Owl witches duel"])
#line_counter(["the Owl witches duel/TheMainGame/images/luz"])

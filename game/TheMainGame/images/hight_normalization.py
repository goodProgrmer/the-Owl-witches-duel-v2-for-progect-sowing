from PIL import Image
import os

def imgNormalization(f,f_indent_dict,h):
    """cheng png image hight to h and adjust other paramters to fit it.
    update its indentation in f_indent_dict as well. if its indentation mising in f_indent_dict, the fanction will not do nothing
    :param f: path to the file that it need to update
    :param f_indent_dict: indentation dictionery in the format that get_indent_dict fanction returns
    :param h: the final hight that the image should have
    :type f: string
    :type f_indent_dict: dictionery
    :type h: int"""
    try:
        indent1= f_indent_dict[f]
        im = Image.open(f+".png")
        w1, h1 = im.size
        zooming_m= h/h1
        w2= int(w1*zooming_m)
        h2=h
        ans= im.resize((w2,h2))
        f_indent_dict[f]= (int(indent1[0]*zooming_m), int(indent1[1]*zooming_m))

        ans.save(f+".png")
    except Exception as e:
        print(e)
        print("error in file:",f)
        return

def get_indent_dict(directory):
    """get from video directory indentation that store in the "data file.txt" file in it.
    :param directory: path to video directory
    :type directory: string
    :return: dictionery with the path to the image file for which the indentation was writen from TheMainGame\images as key and the indantation as value
    :rtype: dictionery"""
    ans={}
    f=open(directory+"/data file.txt","r")
    for line in f:
        parts= line.split(":")
        ans[parts[0]]= eval("("+parts[1]+")")
    f.close()
    return ans

def save_indent_dict(directory, indent_dict):
    """get indentation dictionery and save it to "data file.txt" file in the given directory in the right format
    :param directory: path to video directory
    :param indent_dict: indentation dictionery in the format that get_indent_dict fanction returns
    :type directory: string
    :type indent_dict: directory"""
    string= ""
    keys= indent_dict.keys()
    for k in keys:
        string+= k+":"+str(indent_dict[k][0])+","+str(indent_dict[k][1])+"\n"

    try:
        f= open(directory+"/data file.txt","w")
        f.write(string)
        f.close()
    except Exception as e:
        print(e)
        print("cant write to data file")
        print(string)


def dirupdate(directory,h):
    """update the hight for every png image in the directory
    :param directory: path to the directory that it need to update images in it
    :param h: the final hight that the images should have
    :type directory: string
    :type h: int"""
    f_indent_dict= get_indent_dict(directory)
    to_update= os.listdir(directory)
    for f in to_update:
        if f[-4:]==".png":
            imgNormalization(directory+"/"+f[:-4],f_indent_dict,h)
    save_indent_dict(directory,f_indent_dict)

def dirupdate_by_first(directory,h):
    """update the hight for every png image in the frames directory so the first frame will be with hight h, and other will change size in the same propotion
    :param directory: path to the directory that it need to update images in it
    :param h: the final hight that the images should have
    :type directory: string
    :type h: int"""
    #checking the number of frams
    f= open(directory+"/frames num.txt","r")
    frames_num= int(f.read())
    f.close()
    f_indent_dict= get_indent_dict(directory) #geting indentation directory
    m= get_zooming_m(directory,h) #find directury size multiple
    for i in range(frames_num):
        try:
            #updating image
            f=directory+"/"+str(i)
            indent1= f_indent_dict[f]
            im = Image.open(f+".png")
            w1, h1 = im.size
            im.resize((int(w1*m),int(h1*m))).save(f+".png")
            f_indent_dict[f]= (int(indent1[0]*m), int(indent1[1]*m))
        except Exception as e:
            print(e)
    save_indent_dict(directory,f_indent_dict) #saving indentation directory

def get_zooming_m(directory,h):
    im = Image.open(directory+"/0.png")
    w1, h1 = im.size
    return h/h1
    

if __name__=="__main__":
    h=80
    directory= "emity/slyme boble hitN"
    f_indent_dict= get_indent_dict(directory)
    to_update= os.listdir(directory)
    imgNormalization("emity/slyme boble hitN/0",f_indent_dict,h)
    imgNormalization("emity/slyme boble hitN/1",f_indent_dict,h)
    save_indent_dict(directory,f_indent_dict)

    directory= "emity/slyme boble hitP"
    f_indent_dict= get_indent_dict(directory)
    to_update= os.listdir(directory)
    imgNormalization("emity/slyme boble hitP/0",f_indent_dict,h)
    imgNormalization("emity/slyme boble hitP/1",f_indent_dict,h)
    save_indent_dict(directory,f_indent_dict)

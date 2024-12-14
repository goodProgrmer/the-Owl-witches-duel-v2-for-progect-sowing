def get_indent_dict(directory):
    """get from  video directory indentation that store in the "data file.txt" file in it.
    :param directory: path to video directory
    :type directory: string
    :return: dictionery with the path to the image file for which the indentation was writen from TheMainGame\images as key and the indantation as value
    :rtype: dictionery"""
    ans={}
    f=open(directory+"/data file.txt","r")
    for line in f:
        parts= line.split(":")
        ans[parts[0]]= eval("["+parts[1]+"]")
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

def normalize_x_indent(directory):
    """normalize x indentations in video directory so first frame x indentation will be 0. works only on video directorys.
    :param directory: path to video directory
    :type directory: string"""
    indent_dict= get_indent_dict(directory)
    zero_indent= indent_dict[directory+"/0"][0]
    for k in indent_dict.keys():
        indent_dict[k][0]-= zero_indent

    save_indent_dict(directory,indent_dict)

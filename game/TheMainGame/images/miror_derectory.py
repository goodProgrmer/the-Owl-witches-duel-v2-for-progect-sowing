from PIL import Image
import os

def updateImg(file):
    """chenge the jpg image to miror reflection of itself."""
    img = Image.open(file)
     
    # flip horizontal
    flip_img = img.transpose(Image.FLIP_LEFT_RIGHT)
     
    flip_img.save(file)

def dirupdate(directory):
    """chenge all jpg images in directory to miror reflection of itself.
    :param directory: the directory to cheng
    :type directory: string"""
    to_update= os.listdir(directory)
    for f in to_update:
        if f[-4:]==".jpg" or f[-4:]==".png":
            updateImg(directory+"/"+f)

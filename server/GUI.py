from tkinter import *
from PIL import Image, ImageTk
import subprocess
import threading
import global_server_op

def find_IP():
    string= subprocess.check_output(["ipconfig"]).decode()
    string= string.replace("\r","")
    lines= string.split("\n")
    ips= []
    networks= []
    
    for l in lines:
        if l!="" and l[0]!=" " and len(networks)>len(ips):
            networks.pop(-1)
            in_zerotier=False
        if l!="" and l[0]!=" ":
            networks.append(l)
        if l[:15]=="   IPv4 Address":
            ips.append(l[39:])
    
    if len(networks)>len(ips):
        networks.pop(-1)

    if len(ips)!=len(networks):
        print("find ip error")
    
    ans= (networks,ips)
    if zerotier_ip:
        ans= ([],[])
        for i in range(len(networks)):
            if networks[i][:25]=="Ethernet adapter ZeroTier":
                ans[0].append(networks[i])
                ans[1].append(ips[i])
        
    return ans

def ips_zip(ips):
    num= 0
    letters="0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    digit=1
    for ip in ips:
        splited= ip.split(".")
        for n in splited:
            num+=int(n)*digit
            digit*=256
    ans=""
    while(num>0):
        ans+=letters[num%len(letters)]
        num= num//len(letters)
    return ans

def ips_unzip(string):
    letters="0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    num= 0
    digit=1
    for l in string:
        num+= letters.find(l)*digit
        digit*=len(letters)
    print(num)
    ans=[]
    while(num>0):
        ans.append([])
        for i in range(4):
            ans[-1].append(str(num%256))
            num= num//256

    for i in range(len(ans)):
        ans[i]= ".".join(ans[i])
    return ans

def user_button():
    global zerotier_ip
    zerotier_ip=True
    enter_code_blit()

def programer_button():
    global zerotier_ip
    zerotier_ip=False
    enter_code_blit()

def enter_code_blit():
    global code
    global bg
    if "code" in globals():
        code.destroy()
    
    text= ips_zip(find_IP()[1])
    if text=="":
        bg_img = no_network_img
    else:
        bg_img = network_img
    bg.config(image= bg_img)

    if text!="":
        width= 40
        code = Text(root, height=len(text)//width+1, width=40, borderwidth=0) #enterence code widget
        code.insert(1.0, text)
        code.configure(font = ("Arial",20),state="disabled")
        code.place(x = 100, y = 325)

    #button color changing
    if zerotier_ip:
        for_programmer.configure(bg= "#C8C8C8")
        for_user.configure(bg= "#646464")
    else:
        for_programmer.configure(bg= "#646464")
        for_user.configure(bg= "#C8C8C8")

def main():
    global done
    global zerotier_ip
    global bg
    global root
    global no_network_img
    global network_img
    global for_user
    global for_programmer
    

    zerotier_ip=False #is the entering code including only zerotier networks IP or any IP of the computer
    
    root = Tk()
    root.geometry("800x800")
    root.title("server")

    no_network_img = PhotoImage(file="window no network resized.png")
    network_img = PhotoImage(file="resized window.png")
      
    #Show image using label 
    bg = Label( root, image = no_network_img) 
    bg.place(x = 0, y = 0)

    #creating buttons
    for_user= Button(root, font = ("Arial",20), text = 'with ZeroTeir', bg="#C8C8C8", command = user_button)
    for_programmer= Button(root, font = ("Arial",20), text = 'without ZeroTeir', bg="#646464", command = programer_button)
    #placing buttons (I am not placing them right now so the user manual will be easyer)
    #for_user.place(x=500,y=650)
    #for_programmer.place(x=100,y=650)
    
    #enterence code bliting
    enter_code_blit()

    root.mainloop()
    print("GUI out")
    global_server_op.done= True
    
    

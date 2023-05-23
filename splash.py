from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
import os
from PIL import Image, ImageTk

root=Tk()

height=630
width=1138
x=(root.winfo_screenwidth()//2)-(width//2)
y=(root.winfo_screenheight()//2)-(height//2)
root.geometry('{}x{}+{}+{}'.format(width,height,x,y))
root.overrideredirect(True)

#root.config(background="#000000")
image = Image.open('splash.jpg')
imag = ImageTk.PhotoImage(image)
bg_l=Label(root,image=imag,bg="#000000")
bg_l.place(x=0,y=0)

progress_l=Label(root,text="Loading...",font=("Trebuchet Ms",18,"bold"),fg="#000000",bg="#FFDD9C")
progress_l.place(x=530,y=520)

progress=ttk.Style()
progress.theme_use("clam")
progress.configure("red.Horizontal.TProgressbar",background="#108cff")

progress=Progressbar(root,orient=HORIZONTAL,length=600,mode="determinate",style="red.Horizontal.TProgressbar")
progress.place(x=300,y=570)

def new():
    root.withdraw()
    os.system("python mu1.py")
    root.destroy()
i=0

def load():
    global i
    if i<=10:
        txt="Loading.."+(str(10*i)+"%")
        progress_l.config(text=txt)
        progress_l.after(300,load)
        progress["value"]=10*i
        i+=1
    else:
        new()
        
load()
root.resizable(False,False)
root.mainloop()

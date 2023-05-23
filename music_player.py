from tkinter import *
from tkinter.filedialog import askdirectory
import pygame
import os
from mutagen.mp3 import MP3
import threading
from tkinter.messagebox import *
from tkinter import ttk
import time
from PIL import Image, ImageTk


class Player:
    def __init__(self,root):
        self.root=root
        pygame.init()
        pygame.mixer.init()
       
        mute = "🔇"
        unmute = u"\U0001F50A"
        vol_mute = 0.0
        vol_unmute = 1
        
        
        #listbox
        self.scroll = Scrollbar(root)
        self.play_list = Listbox(root, font="Sansarif 13 bold", bd=4,bg="#040227",fg="white", width=43, height=25, selectbackground="white",selectforeground="black",relief="sunken")
        self.scroll.place(x=1110, y=76, height=510, width=15)
        self.play_list.place(x=700, y=77)
        self.scroll.config(command=self.play_list.yview)
        self.play_list.config(yscrollcommand=self.scroll.set)
        
        file="bg.jpg"
        self.back_img=Image.open(file)
        self.back_img=self.back_img.resize((640,460),Image.ANTIALIAS)
        self.img=ImageTk.PhotoImage(self.back_img)
        self.img_label=Label(root,bg="#040227")
        self.img_label.grid(row=0,column=0)    
        self.img_label["image"]=self.img
        
        
        #========================
       
        def add():
            try:
                directory=askdirectory()
                os.chdir(directory)
                song_list=os.listdir()
                song_list.reverse()
                for song in song_list:
                    pos=0
                    if song.endswith(('mp3')):
                        self.play_list.insert(pos,song)
                    pos+=1
                index=0
                self.play_list.selection_set(index)
                self.play_list.see(index)
                self.play_list.activate(index)
                self.play_list.selection_anchor(index)
                
            except:
                showerror("File error","Please choose a folder containing mp3 files.")
                
        def add_songs():
            threads=threading.Thread(target=add)
            threads.start()
        

        def show_time():
            global next_play
            current_time=pygame.mixer.music.get_pos() / 1000
            formated_time=time.strftime("%H:%M:%S",time.gmtime(current_time))
            next_play=self.play_list.curselection()
            song=self.play_list.get(next_play)
            song_timer=MP3(song)
            song_length=int(song_timer.info.length)
            format_for_length=time.strftime("%H:%M:%S",time.gmtime(song_length))
            self.label_time.config(text=f"{format_for_length}/{formated_time}") 
            self.progress["maximum"]=song_length
            self.progress["value"]=int(current_time)
            root.after(100,show_time)
            
        def play_music():
            try:
                track=self.play_list.get(ACTIVE)
                pygame.mixer.music.load(track)
                self.var.set(track)
                pygame.mixer.music.play()
                show_time()
            except:
                showerror("No Music","Please load the music you want to listen to.")
        
        def repeat():
            try:
                index=0
                self.play_list.select_clear(0,END)
                self.play_list.selection_set(index,last=None)
                self.play_list.see(index)
                self.play_list.activate(index)
                self.play_list.select_anchor(index)
                track=self.play_list.get(index)
                pygame.mixer.music.load(track)
                self.var.set(track)
                pygame.mixer.music.play()
            except:
                showerror("Playist not selected","Please add folder of music playlist")
        
        def repeat():
            threads=threading.Thread(target=repeat)
            threads.start()
            
        def pausing():
            pygame.mixer.music.pause()  
            file6="play.jpg"
            self.b_img5=Image.open(file6)
            self.im5=ImageTk.PhotoImage(self.b_img5)
            self.pause=Button(self.root,bd=0,command=unpausing,bg="#040227",relief="raised",fg="#040227",activebackground="#040227")
            self.pause.place(x=270,y=530)
            self.pause["image"]=self.im5  
        
        def unpausing():
            pygame.mixer.music.unpause()  
            file6="pause.jpg"
            self.b_img5=Image.open(file6)
            self.im5=ImageTk.PhotoImage(self.b_img5)
            self.pause=Button(self.root,bd=0,command=pausing,bg="#040227",relief="raised",fg="#040227",activebackground="#040227")
            self.pause.place(x=270,y=530)
            self.pause["image"]=self.im5
        
        def play():
            threads=threading.Thread(target=play_music)
            threads.start()
                  
        root.bind("<space>",lambda x:play)
        
        def volume(x):
            pygame.mixer.music.set_volume(self.volume_slider.get())
            
        def muted():
            if self.mute["text"]==unmute:
                pygame.mixer.music.set_volume(vol_mute)
                self.volume_slider.set(vol_mute)
                self.mute["fg"]="red"
                self.mute["text"]=mute
            elif self.mute["text"]==mute:
                pygame.mixer.music.set_volume(vol_mute)
                self.volume_slider.set(vol_mute)
                self.mute["fg"]="black"
                self.mute["text"]=unmute
        
        def next_song():
            try:
                next_play=self.play_list.curselection()
                next_play=next_play[0]+1
                song=self.play_list.get(next_play)
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
                self.play_list.select_clear(0,END)
                self.play_list.activate(next_play)
                self.play_list.selection_set(next_play,last=None)
                self.var.set(song)
                show_time()
                self.play_list.see(next_play)
            except:
                pygame.mixer.music.pause()
                showerror("No Next song", "There is no music after this one.")
                pygame.mixer.music.unpause()    
        def next():
            threads=threading.Thread(target=next_song)
            threads.start()
            
        
        def prev_song():
            try:
                
                next_play=self.play_list.curselection()
                next_play=next_play[0]-1
                song=self.play_list.get(next_play)
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
                self.play_list.select_clear(0,END)
                self.play_list.activate(next_play)
                self.play_list.selection_set(next_play,last=None)
                self.var.set(song)
                show_time()
                self.play_list.see(next_play)
            except:
                pygame.mixer.music.pause()
                showerror("No previous Song", "There are no more prior songs.")
                pygame.mixer.music.unpause()
                
            
        def prev():
            threads=threading.Thread(target=prev_song)
            threads.start()
            
        self.root.bind("<Left>",lambda x:prev())
        self.root.bind("<Right>",lambda x:next())
                              
        #==================
        
        self.var=StringVar()
        self.var.set("...............................................................")
        self.song_title=Label(root,font="Helvetica 16 bold",bg="#040227",fg="white",width=60,textvariable=self.var)
        self.song_title.place(x=1,y=0)    
        
        file1="playb.png"
        self.b_img=Image.open(file1)
        self.im=ImageTk.PhotoImage(self.b_img)
        self.play=Button(self.root,bd=0,bg="#040227",relief="raised",command=play,fg="#040227",activebackground="#040227")
        self.play.place(x=255,y=160)
        self.play["image"]=self.im
        
        
        #prev
        file2="prev.jpg"
        self.b_img1=Image.open(file2)
        self.im1=ImageTk.PhotoImage(self.b_img1)
        self.prev=Button(self.root,bd=0,bg="#040227",relief="raised",command=prev,fg="#040227",activebackground="#040227")
        self.prev.place(x=200,y=540)
        self.prev["image"]=self.im1
       
        #next
        file3="next.jpg"
        self.b_img2=Image.open(file3)
        self.im2=ImageTk.PhotoImage(self.b_img2)
        self.next=Button(self.root,bd=0,bg="#040227",relief="raised",command=next,fg="#040227",activebackground="#040227")
        self.next.place(x=365,y=540)
        self.next["image"]=self.im2
        
        #pause
        file4="pause.jpg"
        self.b_img3=Image.open(file4)
        self.im3=ImageTk.PhotoImage(self.b_img3)
        self.pause=Button(self.root,bd=0,command=pausing,bg="#040227",relief="raised",fg="#040227",activebackground="#040227")
        self.pause.place(x=270,y=530)
        self.pause["image"]=self.im3
        
        
        #repeta
        file5="loop.jpg"
        self.b_img4=Image.open(file5)
        self.im4=ImageTk.PhotoImage(self.b_img4)
        self.rep=Button(self.root,bd=0,bg="#040227",command=repeat,relief="raised",fg="#040227",activebackground="#040227")
        self.rep.place(x=80,y=545)
        self.rep["image"]=self.im4  
        
        
        self.load_music=Button(self.root,text=" OPEN PLAYLIST ",command=add_songs,relief="raised",width=30,bd=5,bg="white",fg="#040227",font="Sansarif 16 bold")
        self.load_music.place(x=700,y=25)
        #volume
        self.mute=Button(self.root,text=unmute,command=muted,width=3,bd=0,bg="white",fg="black",font="Helvetica 20 bold")
        self.mute.place(x=480,y=550)
        
        
        self.style=ttk.Style()
        self.style.configure("myStyle.Horizontal.Tscale",background="#505050")
        self.volume_slider=ttk.Scale(self.root,from_=0,to=1,command=volume,orient=HORIZONTAL,value=1,length=130,style="myStyle.Horizontal.TScale")
        self.volume_slider.place(x=550,y=560)
        
        self.progress=ttk.Progressbar(self.root,orient=HORIZONTAL,value=0,length=480,mode="determinate")
        self.progress.place(x=20,y=500)
        
        #time
        self.label_time=Label(root,text="00:00:00/00:00:00",width=15,font="Helvetica,10",bg="white",fg="black")
        self.label_time.place(x=505,y=497)
        
  
def main():
    window1=Tk()
    ui=Player(window1)
    height=630
    width=1138
    x=(window1.winfo_screenwidth()//2)-(width//2)
    y=(window1.winfo_screenheight()//2)-(height//2)
    window1.geometry('{}x{}+{}+{}'.format(width,height,x,y))
    
    window1.title("mp3 music player")
    window1.configure(bg="#040227")
    window1.resizable(width=0,height=0)
    window1.mainloop()
    
if __name__=="__main__":
    main()
    
    
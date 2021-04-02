import tkinter as tk
from tkinter import *
from tkinter import messagebox
import cv2, os
from cv2 import *
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
from pandas import *
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
#from gtts import gTTS
#from playsound import playsound
import random
import win32com.client
import turtle
from time import strftime


def s(dic={"1":"st","2":"nd","3":"rd"}):
    x=strftime("%d")
    y=strftime(" %A,%B,%Y")
    res=x+ ('th' if x[-2]=='1' else dic.get(x[1],'th'))+y
    date1.config(text=res)
    
def get_time():
    time_string=time.strftime("%I:%M:%S %p")
    clock1.config(text=time_string)
    clock1.after(200,get_time)
'''
def clock():
    wn=turtle.Screen()
    wn.bgcolor("black")
    wn.setup(width=400,height=400)
    wn.title("Vidyalankar Clock-System")
    wn.tracer(0)

    pen=turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.pensize(3)

    def draw_clock(h,m,s,pen):
        pen.up()
        pen.goto(0,110)
        pen.setheading(180)
        pen.color("green")
        pen.pendown()
        pen.circle(110)

        pen.penup()
        pen.goto(0,0)
        pen.setheading(90)

        for i in range(12):
            pen.fd(98)
            pen.pendown()
            pen.fd(10)
            pen.penup()
            pen.goto(0,0)
            pen.rt(30)

        for i in range(60):
            pen.fd(90)
            pen.pendown()
            pen.fd(7)
            pen.penup()
            pen.goto(0,0)
            pen.rt(6)
        #hrs hand
        pen.penup()
        pen.goto(0,0)
        pen.color("white")
        pen.setheading(90)
        angle=(h/12)*360
        pen.rt(angle)
        pen.pendown()
        pen.fd(65)
        #minutes hand
        pen.penup()
        pen.goto(0,0)
        pen.color("#333")
        pen.setheading(90)
        angle=(m/60)*360
        pen.rt(angle)
        pen.pendown()
        pen.fd(80)
        #seconds hand
        pen.penup()
        pen.goto(0,0)
        pen.color("Red")
        pen.setheading(90)
        angle=(s/60)*360
        pen.rt(angle)
        pen.pendown()
        pen.fd(94)    
    while True:
        h=int(time.strftime("%I"))
        m=int(time.strftime("%M"))
        s=int(time.strftime("%S"))

        draw_clock(h,m,s,pen)
        wn.update()
        #time.sleep(1)
        pen.clear()
    
    wn.mainloop()
'''

    
def open_window():
    c=Toplevel()
    
    def TakeImages():
        name=(t1.get("1.0","end-1c"))
        Id=(t2.get())
        if(isinstance(Id,str) and isinstance(name,str)):
            s3=win32com.client.Dispatch("SAPI.SpVoice")
            s3.speak("Wait for the Image to be clicked")
            #convert_to_audio2(n3)
            cam = cv2.VideoCapture(0)
            harcascadePath= "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
        
            sampleNum=0
        
            while(True):
                ret,img= cam.read()
                gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces= detector.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                    sampleNum=sampleNum+1
                    cv2.imwrite("TrainingImages\ " + name +"." + Id + '.' +str(sampleNum) + ".jpg",gray[y:y+h,x:x+h])
                    cv2.imshow('Frame',img)
                if(cv2.waitKey(50) & 0xff == ord('q')):
                    break
                elif sampleNum >90:
                    break
                
            cam.release()
            cv2.destroyAllWindows()
            s1=win32com.client.Dispatch("SAPI.SpVoice")
            s1.speak("Images has been Saved")
            #convert_to_audio(n1)

            res = "Images Saved for Name:"+name
            row = [Id,name]
            with open('StudentDetails\studentDetails.csv','a',newline="") as csvFile:
                writer=csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            with open('Attendance\Attendance.csv','a',newline="") as csvFile:
                writer=csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            att=read_csv('StudentDetails\studentDetails.csv')
            att.sort_values(by=['Id'],inplace=True)
            att.to_csv('StudentDetails\studentDetails.csv',index=False)
            
            ss=read_csv('Attendance\Attendance.csv')
            ss.sort_values(by=['Id'],inplace=True)
            ss.to_csv('Attendance\Attendance.csv',index=False)
            t4.configure(text=res)
        else:
            if(is_number(Id)):
                res =" Enter Alphabetical Name"
                t4.configure(text =res)
            if(name.isalpha()):
                res =" Enter Numerical Id"
                t4.configure(text =res)
        
    
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

    def TrainImages():
        recognizer = cv2.face_LBPHFaceRecognizer.create()
        detector= cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        faces, Ids = getImagesAndLabels('TrainingImages')
        recognizer.train(faces, np.array(Ids))
        recognizer.save('TrainingImageLabel/Trainner.yml')
        res = "Image Trained"  # +",".join(str(f) for f in Id)
        s4=win32com.client.Dispatch("SAPI.SpVoice")
        s4.speak("Images successfully trained")
        t4.configure(text=res)

    def getImagesAndLabels(path):
        imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
        faceSamples=[]
        Ids=[]
        for imagePath in imagePaths:
            pilImage=Image.open(imagePath).convert('L')
            imageNp=np.array(pilImage,'uint8')
            Id=int(os.path.split(imagePath)[-1].split(".")[1])
            faceSamples.append(imageNp)
            Ids.append(Id)
        return faceSamples,Ids

        
    
    c.title("Attendance-System")
    c.geometry('1024x720+200+40')
    c.resizable(0,0)
    c.iconbitmap(r'v-ttendance.ico')

    dialog_title="Quit"
    dialog_text='Are you sure?'

    w=Canvas(c,width=1024,height=720)
    image=ImageTk.PhotoImage(Image.open("register.jpg"))
    w.create_image(0,0,anchor=NW,image=image)
    w.pack()

    c.grid_rowconfigure(0,weight=1)
    c.grid_columnconfigure(0,weight=1)

    s=win32com.client.Dispatch("SAPI.SpVoice")
    s.speak("Welcome to Vidyalankar Attendance system")

    message=tk.Label(c,text="STUDENT'S  PORTAL",bg="Black",fg="White",width=34,height=3,font=('times',30,'bold '))
    message.place(x=100, y=20)

    l1=tk.Label(c,text="Enter Name",bg="Black",fg="orange",width=10,height=1,font=('times',22))
    l1.place(x=150, y=200)
    l11=tk.Label(c,text=":",bg="Black",fg="orange",width=1,height=1,font=('times',22))
    l11.place(x=400, y=200)

    t1=tk.Text(c,height=1,bg="Black",fg="orange",width=22,font=('times',20),border=10)
    t1.place(x=530, y=195)

    l2=tk.Label(c,text="Enter Roll-No.",bg="Black",fg="Orange",width=10,height=1,font=('times',22))
    l2.place(x=150, y=300)
    l22=tk.Label(c,text=":",bg="Black",fg="orange",width=1,height=1,font=('times',22))
    l22.place(x=400, y=300)
    t2=tk.Entry(c,bg="Black",fg="orange",width=22,font=('times',20),border=10)
    t2.place(x=530, y=294)


    l4=tk.Label(c,text="Notification",bg="Black",fg="Lightgrey",width=10,height=1,font=('times',22,'bold'),)
    l4.place(x=150, y=400)
    l44=tk.Label(c,text=":",bg="Black",fg="orange",width=1,height=1,font=('times',22))
    l44.place(x=400, y=400)
    t4=tk.Label(c,bg="Black",fg="Green",width=24,font=('times',20),border=10)
    t4.place(x=510, y=394)

    takeImage=tk.Button(c,text="Take Image",command=TakeImages,bg="Black",fg="White",activebackground="#333",width=10,height=1,font=('times',22),border=8,activeforeground="orange")
    takeImage.place(x=60, y=490)

    trainImage=tk.Button(c,text="Train Image",command=TrainImages,bg="Black",fg="White",activebackground="#333",width=10,height=1,font=('times',22),border=8,activeforeground="orange")
    trainImage.place(x=305, y=490)

    backs=tk.Button(c,text="← Back",command=c.destroy,bg="Black",fg="White",activebackground="#333",width=10,height=1,font=('times',22),border=8,activeforeground="brown")
    backs.place(x=550, y=490)

    quitWindows=tk.Button(c,text="Quit",command=top.destroy,bg="Black",fg="White",activebackground="#333",width=10,height=1,font=('times',22),border=8,activeforeground="Red")
    quitWindows.place(x=790, y=490)



    tt=tk.Label(c,fg="black",width=20,font=('times',22),border=0,)
    tt.place(x=103, y=135)
    m=Canvas(tt,width=810,height=20,bg="Black")
    m.pack(fill=BOTH,expand=True)

    while True:
        m1=-10
        oval=m.create_text(m1,10,fill="Orange",text="Welcome  To  Vidyalankar  Institute  Of  Technology")
        for i in range(1000):
            m.move(oval,1,0)
            c.update()
            time.sleep(0.01)
        
        m1=m1-10
    
    
        oval=m.create_text(m1,10,fill="Orange",text="Please  Register  Your  Following  Detail's")

        for i in range(1000):
            m.move(oval,1,0)
            c.update()
            time.sleep(0.01)
    
    
    c.mainloop()

def open_window1():
    c1=Toplevel()
    
    c1.title("Attendance-System")
    c1.geometry('1024x720+200+40')
    c1.resizable(0,0)
    c1.iconbitmap(r'v-ttendance.ico')

    dialog_title="Quit"
    dialog_text='Are you sure?'
    
    def TrackImages():
        recognizer = cv2.face_LBPHFaceRecognizer.create()
        recognizer.read('TrainingImageLabel/Trainner.yml')
        faceCascade= cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        df=pd.read_csv("StudentDetails/studentDetails.csv")

        s3=win32com.client.Dispatch("SAPI.SpVoice")
        s3.speak("Say cheeeeeeeeeeeeeeezzz")
        
        cam=cv2.VideoCapture(0)
        font=cv2.FONT_HERSHEY_SIMPLEX
        col_names=[ 'Id', 'Name', 'Date', 'Time']
        attendance=pd.DataFrame(columns=col_names)
        while True:
            ret,img=cam.read()
            gray=cv2.cvtColor(img,COLOR_BGR2GRAY)
            faces=faceCascade.detectMultiScale(gray,1.3,5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                Id,conf=recognizer.predict(gray[y:y+h,x:x+w])
                if(conf<50):
                    ts=time.time()
                    date=datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    timeStamp=datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa=df.loc[df['Id'] == Id]['Name'].values
                    tt=str(Id)+"-"+aa
                    attendance.loc[len(attendance)]=[Id,aa,date,timeStamp]
                else:
                    Id='Unknown'
                    tt=str(Id)
                #if(conf>75):
                    #noOfFile=len(os.listdir("ImagesUnknown"))+1
                    #cv2.imwrite("ImagesUnknown/Image"+str(noOfFile)+".jpg",img[y:y+h,x:x+w])
                cv2.putText(img,str(tt),(x,y+h),font,1,(255,255,255),2)
            attendance=attendance.drop_duplicates(subset=['Id'],keep='first')
            cv2.imshow('im',img)
            if(cv2.waitKey(50) & 0xff == ord('q')):
                break
        ts=time.time()
        #Hour,Minute,Second=timeStamp.split(":")
        date=datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
        fileName="Attendance/Attendance.csv"
        cam.release()
        cv2.destroyAllWindows()
        df1=read_csv(fileName)
        (x,y)=attendance.shape
        (x1,y1)=df1.shape
        dict1=dict(attendance["Id"])
        l1=[]
        i=0
        j=0
        for j in dict1.values():
            l1.append(j)
        dict2=dict(df1["Id"])
        j=0
        z=0
        l2=[]
        for j in dict2.values():
            l2.append(j)
        j=0
        for i in df1.columns:
            date1=i
        if(str(date1)!=str(date)):
            df1[date]='A' 
        for i in range(0,x):
            for j in range(0,x1):
                if(l1[i]==l2[j]):
                    df1.loc[j,date]='P'
        df1.sort_values(by=['Id'],inplace=True)
        print(df1) 
        df1.to_csv(fileName,index=False)

        
        i=0
        with open("Attendance/Attendance.csv", 'r') as csvFile:
            lines=csv.reader(csvFile)
            for line in lines :
                if(i==0):
                    s= "    ".join(line)
                    listbox.insert(END,s)
                else:
                    s="      ".join(line)
                    listbox.insert(END,s)
                i=i+1
                

    w2=Canvas(c1,width=1024,height=720)
    image=ImageTk.PhotoImage(Image.open("register.jpg"))
    w2.create_image(0,0,anchor=NW,image=image)
    w2.pack()


   
    tt1=tk.Frame(c1,bg="black",width=5,border=0,)
    tt1.place(x=200,y=210,anchor=NW)
    m111=Canvas(tt1,width=245,height=200,bg="Black")
    i=ImageTk.PhotoImage(Image.open("sir.jpg.jfif"))
    m111.pack(fill=BOTH,expand=True)
    m111.create_image(0,0,image=i,anchor=NW)
    
    
    message=tk.Label(c1,text="TEACHER'S  PORTAL",bg="Black",fg="White",width=35,height=3,font=('times',30,'bold'))
    message.place(x=100, y=20)

    trackImage=tk.Button(c1,text='''Mark\nAttendance''',command=TrackImages,bg="Black",fg="White",activebackground="#333",width=10,height=1,font=('times',22),border=8,activeforeground="brown")
    trackImage.place(x=650, y=275)

    backt=tk.Button(c1,text="← Back",command=c1.destroy,bg="Black",fg="White",activebackground="#333",width=10,height=1,font=('times',22),border=8,activeforeground="brown")
    backt.place(x=800, y=510)

    quitWindowt=tk.Button(c1,text="Quit",command=top.destroy,bg="Black",fg="White",activebackground="#333",width=10,height=1,font=('times',22),border=8,activeforeground="Red")
    quitWindowt.place(x=800, y=610)
    
    l5=tk.Label(c1,text="Attendance",bg="Black",fg="Lightgrey",width=10,height=1,font=('times',22,'bold'))
    l5.place(x=100, y=445)
    l55=tk.Label(c1,text=":",bg="Black",fg="orange",width=1,height=1,font=('times',22))
    l55.place(x=320, y=445)

    t5=tk.Label(c1,text="",bg="Black",fg="Green",width=60,height=9,font=('times',15))
    t5.place(x=100, y=490)

    scrollbar=Scrollbar(t5) 
    scrollbar.pack(side=RIGHT ,ﬁll="y")
    listbox=Listbox(t5,yscrollcommand=scrollbar.set,bg="Black",fg="Green",width=60,height=9,font=('times',15)) 
    listbox.pack(expand=True,ﬁll="both") 
    scrollbar.conﬁg(command=listbox.yview)

    ttt=tk.Label(c1,fg="black",width=20,font=('times',22),border=0,)
    ttt.place(x=480, y=300)
    n=Canvas(ttt,width=150,height=20,bg="Black")
    n.pack(fill=BOTH,expand=True)

    while True:
        n1=-10
        line=n.create_text(n1,10,fill="Orange",text="------------>")
        for i1 in range(300):
            n.move(line,1,0)
            c1.update()
            time.sleep(0.01)
        
        n1=n1-10
        line=n.create_text(n1,10,fill="lightblue",text="----------->")
        for i1 in range(300):
            n.move(line,1,0)
            c1.update()
            time.sleep(0.01)

    
    c1.mainloop()    

top=tk.Tk()

top.title("Attendance-System")
top.geometry('1024x720+200+40')
top.resizable(0,0)
top.iconbitmap(r'v-ttendance.ico')

global un
global p
global tlb1
global tlb2
global e


e="Show"


tt1=tk.Frame(top,bg="black",border=0,)
tt1.place(x=0,y=130,anchor=NW)

w1=Canvas(top,width=1024,height=720)
image=ImageTk.PhotoImage(Image.open("register.jpg"))
i1=ImageTk.PhotoImage(Image.open("vidyalogo.png"))
w1.pack(fill=BOTH,expand=True)
w1.create_image(0,0,anchor=NW,image=image)
w1.create_image(410,150,image=i1,anchor=NW)

ttt1=tk.Frame(top,bg="black",border=0,)
ttt1.place(x=810,y=145,anchor=NW)
clock1=tk.Label(ttt1,fg="orange",bg="black",width=10,height=1,font=('times',15,),border=5,relief=SUNKEN)
clock1.pack()
get_time()

tttt1=tk.Frame(top,bg="black",border=0,)
tttt1.place(x=100,y=150,anchor=NW)
date1=tk.Label(tttt1,text="",fg="orange",bg="black",width=20,height=1,font=('times',11,),border=5,relief=SUNKEN)
date1.pack()
s()

message=tk.Label(top,text="V-ATTENDANCE",bg="Black",fg="White",width=35,height=2,font=('times',30,'bold'))
message.place(x=100, y=20)

un=StringVar()
p=StringVar()


lbl1=tk.Label(top,text="USERNAME",bg="black",fg="orange",width=10,height=1,font=('times',22))
lbl1.place(x=170,y=310)
lbl11=tk.Label(top,text=":",bg="black",fg="orange",width=1,height=1,font=('times',22))
lbl11.place(x=410,y=310)
tlb1=tk.Entry(top,textvariable=un,bg="Black",fg="orange",width=22,font=('times',20),border=10)
tlb1.place(x=540,y=312)

lbl2=tk.Label(top,text="PASSWORD",bg="black",fg="Orange",width=10,height=1,font=('times',22))
lbl2.place(x=170,y=410)
lbl22=tk.Label(top,text=":",bg="black",fg="orange",width=1,height=1,font=('times',22))
lbl22.place(x=410,y=413)
tlb2=tk.Entry(top,textvariable=p,bg="Black",fg="orange",width=22,font=('times',20),border=10,show="*")
tlb2.place(x=540,y=405)



def error1():
    messagebox.showerror("Error","Invalid Creadentials")
    
def login():
    usern=un.get()
    password=p.get()
    uname="1"
    pword="1"
    if usern==uname and password==pword:
        s=win32com.client.Dispatch("SAPI.SpVoice")
        s.speak("you have successfully logged in")
        tlb1.delete(0,END)
        tlb2.delete(0,END)
        e="show"
        cb2=tk.Button(top,relief=FLAT,text=e,command=show,fg="orange",bg="black",width=4,height=1,activeforeground="red",activebackground="black",font=('times',15))
        cb2.place(x=814,y=411)
        open_window1()
        
    elif(len(un.get())==0 and len(p.get())==0):
        s=win32com.client.Dispatch("SAPI.SpVoice")
        s.speak("Please enter your Username and password")
        e="show"
        cb2=tk.Button(top,relief=FLAT,text=e,command=show,fg="orange",bg="black",width=4,height=1,activeforeground="red",activebackground="black",font=('times',15))
        cb2.place(x=814,y=411)
    elif(len(un.get())==0):
        s=win32com.client.Dispatch("SAPI.SpVoice")
        s.speak("Please enter your Username")
        e="show"
        cb2=tk.Button(top,relief=FLAT,text=e,command=show,fg="orange",bg="black",width=4,height=1,activeforeground="red",activebackground="black",font=('times',15))
        cb2.place(x=814,y=411)
    elif(len(p.get())==0):
        s=win32com.client.Dispatch("SAPI.SpVoice")
        s.speak("Please enter your password")
    
    else:
        s=win32com.client.Dispatch("SAPI.SpVoice")
        s.speak("Error occured;please retry")
        error1()
        tlb1.delete(0,END)
        tlb2.delete(0,END)
        e="show"
        cb2=tk.Button(top,relief=FLAT,text=e,command=show,fg="orange",bg="black",width=4,height=1,activeforeground="red",activebackground="black",font=('times',15))
        cb2.place(x=814,y=411)
    return top.destroy

def show():
    e="Hide"
    tlb2=tk.Entry(top,textvariable=p,bg="Black",fg="orange",width=22,font=('times',20),border=10)
    tlb2.place(x=540,y=405)
    cb2=tk.Button(top,relief=FLAT,text=e,command=show1,fg="orange",bg="black",width=4,height=1,activeforeground="red",activebackground="black",font=('times',15))
    cb2.place(x=807,y=412)

def show1():
    e='Show'
    tlb2=tk.Entry(top,textvariable=p,bg="Black",fg="orange",width=22,font=('times',20),border=10,show="*")
    tlb2.place(x=540,y=405)
    cb2=tk.Button(top,relief=FLAT,text=e,command=show,fg="orange",bg="black",width=4,height=1,activeforeground="red",activebackground="black",font=('times',15))
    cb2.place(x=807,y=412)   

'''
cbc=tk.Button(top,text='ANALOUGE-CLOCK',command=clock,bg="Black",fg="White",activebackground="#333",width=17,height=1,font=('times',12),border=0,activeforeground="Red",relief=FLAT)
cbc.place(x=100,y=150)
'''

cb1=tk.Button(top,text='''TEACHER'S\nPORTAL''',command=login,bg="Black",fg="White",activebackground="#333",width=15,height=2,font=('times',22),border=8,activeforeground="orange")
cb1.place(x=70,y=550)



cb2=tk.Button(top,relief=FLAT,text=e,command=show,fg="orange",bg="black",width=4,height=1,activeforeground="red",activebackground="black",font=('times',15))
cb2.place(x=807,y=412) 


cb=tk.Button(top,text='''STUDENT'S\nPORTAL''',command=open_window,bg="Black",fg="White",activebackground="#333",width=15,height=2,font=('times',22),border=8,activeforeground="orange")
cb.place(x=415,y=550)

quitWindow1=tk.Button(top,text="Quit",command=top.destroy,bg="Black",fg="White",activebackground="#333",width=11,height=2,font=('times',22),border=8,activeforeground="Red")
quitWindow1.place(x=760, y=550)

tt1=tk.Label(top,fg="black",width=20,font=('times',22),border=0,)
tt1.place(x=115, y=88)
mm=Canvas(tt1,width=810,height=20,bg="Black")
mm.pack(fill=BOTH,expand=True)

while True:
    m11=-10
    oval=mm.create_text(m11,10,fill="Orange",text="Welcome  To  Vidyalankar  Institute  Of  Technology")
    for i in range(1000):
        mm.move(oval,1,0)
        top.update()
        time.sleep(0.01)
        
    m11=m11-10
    
    
    oval=mm.create_text(m11,10,fill="lightBlue",text="Welcome  To  Vidyalankar  Institute  Of  Technology")

    for i in range(1000):
        mm.move(oval,1,0)
        top.update()
        time.sleep(0.01)


top.mainloop()

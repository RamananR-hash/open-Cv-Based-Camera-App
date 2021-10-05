import cv2#pip install opencv-python
from datetime import datetime
import threading
import os
from tkinter import filedialog
import tkinter as tk
def submit():
        global name_val
        global name_val2
        name=name_var.get()
        password=passw_var.get()
        name_var.set("")
        passw_var.set("")
        name_val=name
        name_val2=password
        var.set(1)
        isChecked()
        #print("Function Called")
root=tk.Tk()
cb = tk.IntVar()
root.title("CAMERA")
name_var=tk.StringVar()
passw_var=tk.StringVar()
var=tk.IntVar()
def isChecked():
    global cap
    if cb.get() == 1:
        cap=cv2.VideoCapture(1)
    else:
        cap=cv2.VideoCapture(0)
chk=tk.Checkbutton(root, text="Secondary Camera", variable=cb, onvalue=1, offvalue=0)
name_label = tk.Label(root, text = 'FIRST NAME', font=('calibre',10, 'bold'))
name_entry = tk.Entry(root,textvariable = name_var, font=('calibre',10,'normal'))
passw_label = tk.Label(root, text = 'SECOND NAME', font = ('calibre',10,'bold'))
passw_entry=tk.Entry(root, textvariable = passw_var, font = ('calibre',10,'normal'))
sub_btn=tk.Button(root,text = 'Submit',  command=submit)
chk.grid(row=2,column=1)
name_label.config(width="10",height="1")
name_label.grid(row=0,column=0)
name_entry.grid(row=0,column=1)
passw_label.grid(row=1,column=0)
passw_entry.grid(row=1,column=1)
sub_btn.grid(row=3,column=1)
sub_btn.wait_variable(var)
path=filedialog.askdirectory()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()
recordControl = 0
camreadTrigger=0
#osd Variables
font = cv2.FONT_HERSHEY_SIMPLEX
org1 = (screen_width+30, screen_height-(screen_height+20))#Recoring
time_pos=(50,screen_height-50)#time position
date_pos=(50,screen_height-100)#date position
Name_pos=(screen_width-200,50)#first Name Position
name_pos2=(screen_width-200,screen_height-50)#second Name Position
displaySize=(screen_width,screen_height)#screen Size
fontScale = 1
blue = (255, 0, 0)
red = (0,0,255)
thickness = 2
lock=False
def show_video():
        global recordControl,escape
        m = 0  # 
        lock = False 
        while True:
                ret, frame = cap.read()
                now = datetime.now()
                time = datetime.time(now)
                name = "capture_" + now.strftime("%y%m%d") + time.strftime("%H%M%S") + ".jpg"
                if ret is True:
                        if lock is True:        
                                imS = cv2.resize(frame, displaySize)
                                image = cv2.putText(imS,name_val,(Name_pos),font,fontScale,blue,thickness,cv2.LINE_AA)
                                image = cv2.putText(imS,str(time.strftime("Time:-"+"%H"+ ":"+"%M"+":"+"%S")),time_pos,font,fontScale,blue,thickness,cv2.LINE_AA)
                                image = cv2.putText(imS,str(now.strftime("Date:-"+"%d"+ ":"+"%m"+":"+"%y")),date_pos,font,fontScale,blue,thickness,cv2.LINE_AA)
                                image = cv2.putText(imS,name_val2,name_pos2,font,fontScale,blue,thickness,cv2.LINE_AA)
                                image = cv2.putText(imS, '.', (50,50), font, 5, red, 20, cv2.LINE_AA)
                                image = cv2.putText(imS, str(time.strftime("%H"+ ":"+"%M"+":"+"%S")), (50,50), font, fontScale, red, 2, cv2.LINE_AA)
                                cv2.imshow("CAMERA", image)
                        else:
                                imS = cv2.resize(frame, displaySize)
                                print(time_pos,displaySize)
                                image = cv2.putText(imS,name_val,(Name_pos),font,fontScale,blue,thickness,cv2.LINE_AA)
                                image = cv2.putText(imS,str(time.strftime("Time:-"+"%H"+ ":"+"%M"+":"+"%S")),time_pos,font,fontScale,blue,thickness,cv2.LINE_AA)
                                image = cv2.putText(imS,str(now.strftime("Date:-"+"%d"+ ":"+"%m"+":"+"%y")),date_pos,font,fontScale,blue,thickness,cv2.LINE_AA)
                                image = cv2.putText(imS,name_val2,name_pos2,font,fontScale,blue,thickness,cv2.LINE_AA)
                                cv2.imshow("CAMERA", image)
                        k = cv2.waitKey(1) & 0Xff
                        #print(k)
                        if k == ord('v'):
                                if lock is False:
                                        recordControl = 0
                                        m+=1
                                        threadName = 'recordThread' + str(m)  # everytime find new name
                                        threadObj = recordVideo(name=threadName)
                                        threadObj.start()
                                        lock = True
                        elif k == 27:  # Quit program and recording
                                escape=1
                                if recordControl != 2:  # make sure that out child process is complet
                                        recordControl = 2
                                threadObj.join()
                                break
                        elif k == ord('c'):  # capture Image
                                cv2.imwrite(os.path.join(path,name), image)
                        elif k == ord('b'):  # stop recording
                                recordControl = 2
                                threadObj.join()
                                lock = False
                        elif k == ord('p'):  # pause recording 
                                recordControl = 1
                        elif k == ord('r'):  # resume recording
                                recordControl = 0
                        elif k == ord('g'):  # OPEN file
                                os.listdir(path)
                else:
                        break
class recordVideo(threading.Thread):  # thread class to record video
        def run(self):
                now = datetime.now()
                time = datetime.time(now)
                name = "capture_V_" + now.strftime("%y%m%d") + time.strftime("%H%M%S") + ".avi"
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(os.path.join(path,name), fourcc, 30.0, (640, 480))
                while True:
                        ret, frame = cap.read()
                        image = cv2.putText(frame,name_val,(550,15),font,0.5,blue,thickness,cv2.LINE_AA)
                        image = cv2.putText(frame,name_val2,(550,450),font,0.5,blue,thickness,cv2.LINE_AA)
                        image = cv2.putText(frame,str(time.strftime("Time:-"+"%H"+ ":"+"%M"+":"+"%S")),(50,440),font,0.5,blue,thickness,cv2.LINE_AA)
                        image = cv2.putText(frame,str(now.strftime("Date:-"+"%d"+ ":"+"%m"+":"+"%y")),(50,460),font,0.5,blue,thickness,cv2.LINE_AA)
                        if recordControl == 0:
                                out.write(image)
                        elif recordControl == 2:
                                break
                out.release()
if (cap.isOpened()):
        show_video()
else:
        cap.open()
        show_video()
cap.release()
cv2.destroyAllWindows()

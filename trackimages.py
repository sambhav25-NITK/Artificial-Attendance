# -*- coding: utf-8 -*-
"""
Created on Wed May 20 15:35:11 2020

@author: sambh
"""
import cv2,os
import pandas as pd
import datetime
import time

recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
recognizer.read("TrainingImageLabel\Trainner.yml")
harcascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(harcascadePath);    
df=pd.read_csv("StudentDetails\StudentDetails.csv")
cam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX        
col_names =  ['Id','Name','Date','Time']
attendance = pd.DataFrame(columns = col_names)    
while True:
    ret, im =cam.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, 1.2,5)    
    for(x,y,w,h) in faces:
        cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
        Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
        if(conf < 50):
            ts = time.time()      
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            aa=df.loc[df['Id'] == Id]['Name'].values
            #print(aa)
            tt=str(Id)+"-"+aa
            attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
            
        else:
            Id='Unknown'                
            tt=str(Id)  
        if(conf > 75):
            noOfFile=len(os.listdir("ImagesUnknown"))+1
            cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
        cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
    attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
    cv2.imshow('im',im) 
    if (cv2.waitKey(1)==ord('q')):
        break
ts = time.time()      
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
Hour,Minute,Second=timeStamp.split(":")
fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
attendance.to_csv(fileName,index=False)
cam.release()
cv2.destroyAllWindows()
#print(attendance)
res=attendance
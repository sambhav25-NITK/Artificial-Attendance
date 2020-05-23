import cv2,os
import csv



Id = input("Enter your id ")
name = input("Enter your name ")
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)


sampleNum=0
while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)        
        #incrementing sample number 
        sampleNum=sampleNum+1
        #saving the captured face in the dataset folder TrainingImage
        cv2.imwrite("Dataset\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
        #display the frame
    cv2.imshow('frame',img)
    #wait for 100 miliseconds 
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    # break if the sample number is morethan 100
    elif sampleNum>60:
        break
cam.release()
cv2.destroyAllWindows() 
res = "Images Saved for ID : " + Id +" Name : "+ name
row = [Id , name]
with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
    
    writer = csv.writer(csvFile)
    file_is_empty = os.stat('StudentDetails\StudentDetails.csv').st_size == 0
        
    if file_is_empty:
        writer.writerow(['Id','Name'])
    writer.writerow(row)
    
csvFile.close()

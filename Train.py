# -*- coding: utf-8 -*-
"""
Created on Wed May 20 15:28:35 2020

@author: sambh
"""


import cv2,os

import numpy as np
from PIL import Image

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    
    #create empth face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

recognizer = cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
harcascadePath = "haarcascade_frontalface_default.xml"
detector =cv2.CascadeClassifier(harcascadePath)
faces,Id = getImagesAndLabels("Dataset")
recognizer.train(faces, np.array(Id))
recognizer.save("TrainingImageLabel\Trainner.yml")
res = "Image Trained"#+",".join(str(f) for f in Id)
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
import pytesseract
import os
from PIL import Image
os.environ['TESSDATA_PREFIX'] = r"C:\Program Files\Tesseract-OCR"
pytesseract.pytesseract.tesseract_cmd='C:/Program Files/Tesseract-OCR/tesseract.exe'

class reader:
    def reading(self):
        
        img=cv2.imread("a.jpeg")
        #resize the image to width 500
        img=imutils.resize(img,width=500)
        cv2.imshow("tey",img)
        cv2.waitKey(0)
        
        #convert image to gray scale
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        cv2.imshow("in gray",gray)
        cv2.waitKey(0)
        
        #reduce the noise from img
        gray=cv2.bilateralFilter(gray,11,17,17)
        cv2.imshow("after filer, smoother",gray)
        cv2.waitKey(0)
        
        #finding edges
        edges=cv2.Canny(gray,200,200)
        cv2.imshow("after finding edge",edges)
        cv2.waitKey(0)
        
        #now find the contours
        
        find_contour,new=cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        new_img=img.copy()
        cv2.drawContours(new_img,find_contour,-1,(0,255,0),3)
        cv2.imshow("canny after contour",new_img)
        cv2.waitKey(0)
        
        find_contour=sorted(find_contour,key=cv2.contourArea,reverse=True)[:30]
        number_plate_count=None
        new_img2=img.copy()#create copy of original image
        cv2.drawContours(new_img2,find_contour,-1,(0,255,0),3)
        cv2.imshow("top 30",new_img2)
        cv2.waitKey(0)
        
        location=0
        name=1
        
        for i in find_contour:
            perimeter=cv2.arcLength(i,True) #perimeter=arclength
            approx=cv2.approxPolyDP(i,0.02*perimeter,True)
            if(len(approx)==4): #here 4 means it has four corners
                number_plate_count=approx
                #croping the rectangle part
                
                x,y,w,h=cv2.boundingRect(i)
                cropped=img[y:y+h,x:x+w]
                cv2.imwrite(str(name)+'.png',cropped)
                name+=1
                break
        cv2.drawContours(img,[number_plate_count],-1,(0,255,0),3)
        cv2.imshow("done",img)
        cv2.waitKey(0)
        
        #now crop the required part
        crop_img="1.png"
        cv2.imshow("cropped img",cv2.imread(crop_img))
        cv2.waitKey(0)

        #using tesseract
        read_img=pytesseract.image_to_string(crop_img,lang="eng")
        print("number:",read_img)
        cv2.waitKey(0)
        
         ##using easy ocr
        result=easyocr.Reader(['en'])
        result=result.readtext(crop_img)
        print(result[0][1])
        
        
        
                
                
                
            
        
r=reader()
r.reading()        
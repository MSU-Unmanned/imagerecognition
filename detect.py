# Modified from https://www.geeksforgeeks.org/how-to-detect-shapes-in-images-in-python-using-opencv/

import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

SHAPES_DICT={3:'Triangle',4:'Quadrilateral',5:'Pentagon',6:'Hexagon',0:'Circle'}
IMG_BASE_PATH='generated_images'

def detect_shapes_in_img(img_path):
    # reading image
    img = cv2.imread(img_path)
    
    # converting image into blurredscale image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray',gray)

    #### Adding gaussian blur
    blurred=cv2.GaussianBlur(gray, (7,7), 0)
    cv2.imshow('blur',blurred)

    # setting threshold of blurred image
    _, threshold = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
    
    # using a findContours() function
    contours, _ = cv2.findContours(
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # list for storing names of shapes
        # here we are ignoring first counter because 
        # findcontour function detects whole image as shape
    for contour in contours[1:]:
        # cv2.approxPloyDP() function to approximate the shape
        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)
        
        # using drawContours() function
        cv2.drawContours(img, [contour], 0, (0, 0, 255), 2)
    
        # finding center point of shape
        M = cv2.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])
    
        # putting shape name at center of each shape
        shape_name=SHAPES_DICT[len(approx)] if len(approx) in SHAPES_DICT.keys() else 'Circle'
        cv2.putText(img, shape_name, (x, y),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
    
    # displaying the image after drawing contours
    cv2.imshow('shapes', img)
    cv2.waitKey(0)
    

if __name__=='__main__':
    img_paths=os.listdir(IMG_BASE_PATH)
    img_paths=[os.path.join(IMG_BASE_PATH,path) for path in img_paths]

    for img_path in img_paths:
        print(img_path)
        detect_shapes_in_img(img_path)

    cv2.destroyAllWindows()
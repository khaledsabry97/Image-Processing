import cv2
import numpy as np
import math
from skimage.color import rgb2gray,rgb2hsv


'python color.py'
cam = cv2.VideoCapture(0)
while(cam.isOpened()):
    # read image
    ret, frame = cam.read()
    hsv2 = cv2.cvtColor(frame,cv2.COLOR_RGB2HSV)
  
   
    cv2.imshow("image", frame)
    cv2.imshow("hsv2",hsv2)
    k = cv2.waitKey(10)
    if k== 27:   
      break
cam.release()
cv2.destroyAllWindows()

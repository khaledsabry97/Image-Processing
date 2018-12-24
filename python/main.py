import time
import cv2
from HandDetection import HandDetection
from FrameDefects import FrameDefects
from UI import UI
from Input import Input

previousFrame = None
count = 0
test = 0
temp_frame = None
rect = None
usedThresh = None  
globalmask = None
isShow = [True,True,True,True,True,True]

if  __name__ == "__main__":

    #record videos
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #out = cv2.VideoWriter('try14.avi',fourcc, 20.0, (640,480))

    camera =cv2.VideoCapture("try10.avi")  # this for mobil connection cam
    #camera =cv2.VideoCapture(0) 
    #camera =cv2.VideoCapture("http://192.168.0.101:4747/video")
    time.sleep(0.25)
    while camera.isOpened():  
        ret, frame = camera.read()
        input = Input()
        #out.write(frame)
        #Check if the next camera read is not null
        if ret:
            #track hand by motion (dynamically)
            detection = HandDetection()
            frame, previousFrame = detection.traceHand(frame,previousFrame)
            
            # get defects
            defect = FrameDefects()
            defects = defect.getDefects()
            if defects is not None:
                #draw the defects
                defect.drawDefects(frame,defects)
                # show some windows
                interface = UI()
                interface.showBasicWindows(frame)
        else:
            print("Video Finished")
            close = False
            while not close:
                close = input.getKey()
            break
        close = False
        close = input.getKey()
        if close:
            print("Bye")
            break
    camera.release()
    cv2.destroyAllWindows()
import cv2
import math
from HandDetection import HandDetection
from UI import UI

cnt = []
class FrameDefects:  
    def getDefects(self):
        from main import globalmask
        #get the contour for all the white areas in the frame
        _, contours, _ = cv2.findContours(globalmask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        
        #get the index of the largest contour
        detection = HandDetection()
        index = detection.getLargestCountour(contours)
        global cnt
        # if the index is -1 then there was no contours from the begining then move
        if index >=0 and index <= len(contours) -1:
            cnt = contours[index]
            #get the points of the parameter that shape the outer convex
            #false parameter means to retrieve with the hull the convexity  defects (the tie between two fingers)
            hull = cv2.convexHull(cnt,returnPoints = False)

            #get the ties
            defects = cv2.convexityDefects(cnt,hull)
        else: 
            defects = None
        return defects
    
    # draws the defects
    def drawDefects(self, frame, defects):
        if defects is None:
            return
        #put inside each element the tie x,y and the color   true==> red   &  false ==> blue  & start of the finger and change in x and change in y
        vec = []

        #blue refer to reverse hand
        #count number of blue ties
        countDefectsBlue = 0

        #red refer to straight hand
        #count number of red ties
        countDefectsRed = 0
        countDefectsYellow = 0
        global cnt
        try:
            for i in range(defects.shape[0]):

                s,e,f,d = defects[i,0]
                start = tuple(cnt[s][0]) #finger tip
                end = tuple(cnt[e][0]) #another finger tip
                tie = tuple(cnt[f][0]) # tie between them

                #if the distance between start line with end to the tie is less than 1000 this means that this not a tie (noise for example)
                if d < 1000: 
                    continue

                cv2.line(frame,start,end,[0,255,0],2)  

                # find length of all sides of triangle
                a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2) # distance between finger tip and another finger tip
                b = math.sqrt((tie[0] - start[0])**2 + (tie[1] - start[1])**2) # distance between finger tip and a tie
                c = math.sqrt((end[0] - tie[0])**2 + (end[1] - tie[1])**2) # distance between another finger tip and a tie

                # apply cosine rule here
                angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 180/3.14
                
                #get distance between finger tips in X and Y
                dx = abs(start[0] - end[0])
                dy = abs(start[1] - end[1])

                #if the angle between fingers tips is less than 60 and difference in X is larger than Y it can be W, V, A or M
                if angle <= 60:
                    if(dx > dy):                  
                        if abs(tie[1] - start[1])> dy and abs(tie[1] - end[1]) > dy:
                            # if the tie y axis is less than y axis for any of the two finger tips then  the hand is reversed
                            if tie[1] < start[1] or tie[1] <end[1]:
                                countDefectsBlue+= 1 # increment the blue defects
                                vec.append((start,tie,1,end)) # push the tie into the array to print later
                            # if the tie y axis is larger than y axis for any of the two finger tips then  the hand is straight
                            elif tie[1] > start[1] or tie[1] > end[1]:
                                countDefectsRed += 1 # increment the red defects
                                vec.append((start,tie,0,end)) # push the tie into the array to print later
                #if the angle between fingers tips is 90 to 110 it can be L
                elif angle < 110 and angle >=90:
                        # y0 is the finger tip with less Y 
                        y0,y1 =start,end
                        if start[1] < end[1]:
                            y0 = start
                            y1 = end
                        else:
                            y0 = end
                            y1 = start
                        #if the change in x axis between the finger and the tie is less than the shorter finger and the tie
                        if abs(y0[0] - tie[0]) < abs(y1[0] - tie[0]) and abs(y0[1] - tie[1]) > 1.5* abs(y1[1] - tie[1]):   
                            countDefectsYellow += 1 # increment the yellow defects
                            vec.append((start,tie,2,end)) # push the tie into the array to print later

            interface = UI()
            #print the ties
            interface.printTies(frame,vec,countDefectsRed,countDefectsBlue,countDefectsYellow)  
            #print Characters by count and color of points
            interface.identifyChar(frame,countDefectsRed,countDefectsBlue,countDefectsYellow)    
            
        except Exception as e:
                print(e)

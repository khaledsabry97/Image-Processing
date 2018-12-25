import cv2
import numpy as np
from UI import UI

class HandDetection:
    # track hand by motion
    def traceHand(self,frame,prev):
        import main
        kernelErosion = np.ones((1,1),np.uint8) #kernel for erosion
        kernelDilation = np.ones((8,8),np.uint8) #kernel for dilation
        frame = cv2.blur(frame, (9,9)) # blur the original frame "very important for the final image"
        previousFrame = prev
    
        #if it's the first frame just take a copy
        if previousFrame is None:
            previousFrame = frame.copy()
            return frame, previousFrame
        
        # get difference between frames
        frameDiff = cv2.absdiff(previousFrame, frame)    
        # apply binary thresholding on the difference
        thresh = cv2.threshold(frameDiff, 20, 255, cv2.THRESH_BINARY)[1]
        # convert thresholded image to gray-scale
        thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
        # get histogram of thresholded image
        hist = cv2.calcHist([thresh], [0], None, [256], [0,256])
        
        # if white pixels is more than 5000 update newThresh and apply erosion and dialation and threshold it by 250
        if hist[255] >= 5000 :
            previousFrame = frame.copy() #save previous frame
            main.usedThresh = thresh # important  
            main.usedThresh = cv2.erode(main.usedThresh,kernelErosion,iterations =1)
            main.usedThresh = cv2.dilate(main.usedThresh, kernelDilation, iterations=5)
            main.usedThresh = cv2.threshold(main.usedThresh, 250, 255, cv2.THRESH_BINARY)[1]

        # update newThresh and mask if None
        if main.usedThresh is None:
                main.usedThresh = thresh

        #find the contours from the remaining threshold image 
        _, cnts, _ = cv2.findContours(main.usedThresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        #search for any movement
        frame = self.detectMovementAndMask(cnts, frame)        
        return frame, previousFrame

    def detectMovementAndMask(self,contours, frame):
        import main
        #get the index of the largest contour
        index = self.getLargestCountour(contours)
        masks = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if index >=0 and index <= len(contours) -1:
            cnt = contours[index]
            M = cv2.moments(cnt) #get some properties from the biggest countour
            # make a mask with largest contour
            contourmask = np.zeros((frame.shape[0],frame.shape[1]),dtype=np.uint8) 
            cv2.fillPoly(contourmask, pts =[cnt], color=(255,255,255))
            # make a mask with the bounding rectangle of largest contour
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w+10,y+h+10),(0,255,0),2)     
            
            rectanglemask = np.zeros((frame.shape[0],frame.shape[1]),dtype=np.uint8)        
            cv2.rectangle(rectanglemask,(x,y),(x+w+20,y+h+10),(255,255,255),-1)

            framehsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # get hue , saturation and value ranges for hand
            lowHue,lowSat,lowVal,highHue,highSat,highVal = self.getRanges(framehsv,contourmask)
            
            
            # mask framehsv with the rectangle mask
            masked = framehsv.copy()
            masked = cv2.bitwise_and(framehsv,masked,mask = rectanglemask)
            # mask the masked frame with low and high values for each chanel
            masks = self.mask(masked,lowHue,lowSat,lowVal,highHue,highSat,highVal)
            # calculate histogram of the output inside the rectangle only 
            maskHist = cv2.calcHist([masks],[0], rectanglemask, [256], [0,256])
            #if white pixels are more than half of black pixels update globalmask
            if main.globalmask is None or maskHist[255] > 0.45* maskHist[0]:
                main.globalmask = masks    
        return frame

    # get ranges for all channels
    def getRanges(self, framehsv,contourmask):
        hue = framehsv[:,:,0]
        lowHue, highHue = self.getChanelRange(hue,contourmask)
        
        framehsv[:,:,1] = cv2.blur( framehsv[:,:,1], (9,9))
        sat = framehsv[:,:,1]
        lowSat, highSat = self.getChanelRange(sat,contourmask)

        framehsv[:,:,2] = cv2.blur( framehsv[:,:,2], (19,19))        
        val = framehsv[:,:,2]  
        gamma = 1.3
        val = self.gamma_correction(val,gamma)
        lowVal, highVal = self.getChanelRange(val,contourmask)
        return lowHue,lowSat,lowVal,highHue,highSat,highVal

    # get range of pixels in chanel
    def getChanelRange(self, chanel, mask):
        # get histogram of chanel inside mask
        Hist = cv2.calcHist([chanel], [0], mask, [256], [0,256])
        # get the range of significant pixel values
        threshold1,threshold2 = self.getHistPeak(Hist) 
        return threshold1, threshold2
    
    # identify range of  pixel values that has most of pixels
    def getHistPeak(self,hist):
        maxIndex = 0
        c =0
        ci = cj = 0
        i=0
        j =255
        begin = True
        end = 255
        start = 0
        try:
            while end - start >20:
                while j > i:
                    ci += hist[i]
                    cj += hist[j]
                    j -=1
                    i +=1
                if begin == True:
                    begin = False
                    c = ci + cj + hist[128]
                if ci >= cj:
                    i =start
                    j =int((end+start)/2)
                    end = j   
                if ci < cj:
                    i = int((end+start)/2)
                    j =end
                    start = i
                ci = 0
                cj = 0
            maxIndex = int((start + end) / 2)
        except Exception as e: 
                print(e)
        startIndex , endIndex = self.getThreshold(hist,maxIndex,c)
        return startIndex , endIndex

    def getThreshold(self,hist,maxIndex,count):
        threshold1 = maxIndex -1
        threshold2 = maxIndex +1
        p = 0
        while p < 0.65 and threshold2 - threshold1 < 30:
            p1,p2 = 0,0
            if threshold1 > 2:
                p1 = (hist[threshold1] + hist[threshold1-1]+ hist[threshold1-2])/count 
            if threshold2 < 254:
                p2 = (hist[threshold2]+hist[threshold2+1]+hist[threshold2+2])/count
            if p1 > p2 and threshold1 > 2:
                p += (hist[threshold1] + hist[threshold1-1]+ hist[threshold1-2])/count 
                threshold1 -=3
            elif p1 <= p2 and threshold2 < 254:   
                p += (hist[threshold2]+hist[threshold2+1]+hist[threshold2+2])/count
                threshold2  += 3
            if p1 == p2 and p2 == 0:
                break
        return threshold1 , threshold2 

    def mask(self,frame,lowHue,lowSat,lowVal,highHue,highSat,highVal):
    #this is the limit threshold the lowest from the average value and the highest from the average value
        try:
            kernelDilation = np.ones((3,3),np.uint8) #kernel for dilation
            kernelErosion = np.ones((2,2),np.uint8) #kernel for erosion
            
            #get mask for each chanel separately
            lower_blue = np.array([lowHue  ,lowSat - 255 ,lowVal -255])
            upper_blue = np.array([highHue ,highSat + 255,highVal + 255 ])       
            mask1 = cv2.inRange(frame, lower_blue, upper_blue)
            mask1 = cv2.erode(mask1,kernelErosion,iterations =1)
            mask1 = cv2.dilate(mask1,kernelDilation,iterations = 2)
            
            lower_blue = np.array([lowHue - 255  ,lowSat, lowVal -255])
            upper_blue = np.array([highHue + 255 ,highSat ,highVal + 255 ])      
            mask2 = cv2.inRange(frame, lower_blue, upper_blue)
            
            lower_blue = np.array([lowHue - 255  ,lowSat -255  ,lowVal - 25 ])
            upper_blue = np.array([highHue + 255 ,highSat + 255 ,highVal+25 ])
            mask3 = cv2.inRange(frame, lower_blue, upper_blue)
            mask3 = cv2.dilate(mask3,kernelDilation,iterations = 2)
            
            # get intersection of hue and value channels 
            masks = cv2.bitwise_and(mask1, mask3)
            masks = cv2.erode(masks,kernelErosion,iterations = 1)
            masks = cv2.dilate(masks,kernelDilation,iterations = 2)

            from main import isShow
            interface = UI()
            if isShow[3]:
                interface.showWindow('hue',mask1)
            elif interface.isOpen('hue'):
                interface.closeWindow('hue')
            if isShow[4]:
                interface.showWindow('sat',mask2)
            elif interface.isOpen('sat'):
                interface.closeWindow('sat')
            if isShow[5]:
                interface.showWindow('val',mask3)
            elif interface.isOpen('val'):
                interface.closeWindow('val')
            
        except Exception as e:
            print(e)
            return frame

        return masks
    
    #return only  the index of the largest contour
    def getLargestCountour(self,contours):
        largestArea = 0
        index = 0
        for i in range(len(contours)):
            area = cv2.contourArea(contours[i])
            if (area>largestArea):
                    largestArea=area
                    index= i
        return index

    # apply gamma correction on a frame
    def gamma_correction(self,frame,gamma):
        frame = frame/255
        frame = cv2.pow(frame, gamma)
        frame = np.uint8(frame*255)
        return frame

    '''
    def getHistPeak(self,Hist,levelRange):
        PixelsCount = 0
        maxIndex = 0
        maxPixels = 0
        
        count = 0
        for i in range(256):
            count += Hist[i]
            if i+levelRange >255:
                break
            for j in range(i,i+levelRange):
                PixelsCount += Hist[j]
                
            if PixelsCount > maxPixels:
                maxIndex = i
                maxPixels = PixelsCount
            PixelsCount = 0
        startIndex , endIndex = getThreshold(Hist,maxIndex + int(levelRange/2),count)
        return startIndex , endIndex
    '''


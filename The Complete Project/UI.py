import cv2

class UI:
    #to print each tie according to the blue and red color and position
    def printTies(self,frame,vec,red,blue,yellow):
        if self.checkPoints(red,blue,yellow) == False:
            return
        for obj in vec:
            start = obj[0]
            tie = obj[1]
            color = obj[2]
            end = obj[3]
            if color == 0: #red
                cv2.circle(frame,tie,5,[0,0,255],-1)
            elif color == 1: #blue
                cv2.circle(frame,tie,5,[255,0,0],-1)
            elif color == 2: #yellow
                cv2.circle(frame,tie,5,[0,255,255],-1)       
            cv2.line(frame,start,tie,[150,150,150],2)     
            cv2.line(frame,end,tie,[150,150,150],2)
        vec.clear()  
    
    # deciede characters by color and count of points
    def identifyChar(self,frame,red,blue,yellow):
        if self.checkPoints(red,blue,yellow) == False:
            return
        if red == 1: #v
            self.showText(frame,"V")
        elif red == 2: #w
            self.showText(frame,"W")
        elif blue == 1: #a
            self.showText(frame,"A")
        elif blue == 2: #m
            self.showText(frame,"M")
        elif yellow == 1: #L
            self.showText(frame,"L")

    def showBasicWindows(self,frame):
        import main
        if main.isShow[0]:
            self.showWindow('frame',frame)
        elif self.isOpen('frame'):
            self.closeWindow('frame')
        if main.isShow[1]:
            self.showWindow('globalmask',main.globalmask)
        elif self.isOpen('globalmask'):
            self.closeWindow('globalmask')
        if main.isShow[2]:
            self.showWindow('Thresh',main.usedThresh)
        elif self.isOpen('Thresh'):
            self.closeWindow('Thresh')

    def showWindow(self,name,frame):
        cv2.namedWindow(name,cv2.WINDOW_NORMAL)
        cv2.resizeWindow(name, 800,600)
        cv2.imshow(name, frame)
        #cv2.imshow("mask", globalmask)
    
    def closeWindow(self,name):
        cv2.destroyWindow(name)
    
    def isOpen(self,name):
        return cv2.getWindowProperty(name, cv2.WND_PROP_AUTOSIZE) >= 0

    def showText(self,frame,text):
        cv2.putText(frame,text, (30, 70), cv2.FONT_HERSHEY_COMPLEX , 4, (50,50,200))  

     #check if the points are valid
    def checkPoints(self,red,blue,yellow):
        if red > 0:
            #if blue > 0 or yellow > 0 or red > 2: 
            if blue > 0 or red > 2:
                return False
        if blue > 0:
            #if red > 0 or yellow > 0 or blue > 2:
            if red > 0 or blue > 2:
                return False
        if yellow > 0:
            if red > 0 or blue > 0 or yellow >1:
                return False        
        return True


    
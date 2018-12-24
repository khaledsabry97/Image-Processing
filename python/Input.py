import cv2
class Input:
    def getKey(self):
        import main
        close = False
        key = cv2.waitKey(3) & 0xFF
        if key == ord('f'):
            main.isShow[0] = not main.isShow[0]
        if key == ord('m'):
            main.isShow[1] = not main.isShow[1]
        if key == ord('t'):
            main.isShow[2] = not main.isShow[2]
        if key == ord('h'):
            main.isShow[3] = not main.isShow[3]
        if key == ord('s'):
            main.isShow[4] = not main.isShow[4]
        if key == ord('v'):
            main.isShow[5] = not main.isShow[5]
        if key == 27:
            close = True
        return close
    
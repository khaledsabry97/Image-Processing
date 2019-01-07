import cv2
class Input:
    def getKey(self):
        import main
        close = False
        key = cv2.waitKey(3) & 0xFF
        if key == ord('f'):                         # frame window
            main.isShow[0] = not main.isShow[0]
        if key == ord('m'):                         # global mask window
            main.isShow[1] = not main.isShow[1]
        if key == ord('t'):                         # threshold window
            main.isShow[2] = not main.isShow[2]
        if key == ord('h'):                         # hue window
            main.isShow[3] = not main.isShow[3]
        if key == ord('s'):                         # satuaration window
            main.isShow[4] = not main.isShow[4]
        if key == ord('v'):                         # value window
            main.isShow[5] = not main.isShow[5]
        if key == 27:
            close = True
        return close
    
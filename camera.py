import cv2

class Camera:
    def capture(self):
        cam = cv2.VideoCapture(0)
        winName = "image"
        cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)
        while True:
            ret, frame = cam.read()
            cv2.imshow("image", frame)
            if not ret:
                break
            k = cv2.waitKey(1)

            if k%256 == 27:
                # ESC pressed
                print("closing...")
                break
            elif k%256 == 32:
                # SPACE pressed
                img_name = "test.png"
                cv2.imwrite(img_name, frame)
                print("picture saved!")
                break
        cam.release()
        cv2.destroyAllWindows()


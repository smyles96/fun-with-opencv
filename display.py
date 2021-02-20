import numpy as np
import cv2

cap = cv2.VideoCapture('troll.mp4')
while(cap.isOpened()):
    
    ret, frame = cap.read() 
    #cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    #cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    
    if ret:
        cv2.imshow("Image", frame)
    else:
       cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

'''
img = cv2.imread('bars.jpg')
cv2.imshow('image', cv2.resize(img, (1500, 900)))

k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
'''
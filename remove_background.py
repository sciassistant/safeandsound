import numpy as np
import cv2

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
video = cv2.VideoCapture(0)

while(True):

    ret,frame = video.read()
    blur_frame = cv2.blur(frame,ksize = (1000,1000))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:

        face = frame [y:y+h,x:x+w]
        blur_frame = cv2.blur(frame,ksize = (15,15))
        blur_frame[y:y+h,x:x+w] = face

    cv2.imshow("original",blur_frame)
    #cv2.imshow("original",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
video.release()
cv2.destroyAllWindows()

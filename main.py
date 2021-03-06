#!/usr/bin/env python
'''
Sources used:
https://docs.opencv.org/4.5.1/
https://myrusakov.ru/python-opencv-move-detection.html
https://www.youtube.com/watch?v=hneuiKpZDcs
'''

import cv2
import time
time.sleep(5)

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
video = cv2.VideoCapture(0)

# Create an object
test_video = cv2.VideoCapture('simples\source_video.mp4') # import frames a video file
#test_video = cv2.VideoCapture(0); # web cam frames

# first and second frame
ret, frame_1 = test_video.read()
ret, frame_2 = test_video.read()

while test_video.isOpened(): # Continue looping until video is completed

    diff = cv2.absdiff(frame_1, frame_2) # React if there is distance between two frames
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) # Convert to grayscale
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    ret, thresh = cv2.threshold(blurred, 20, 255, cv2.THRESH_BINARY) # Threshold
    dilated = cv2.dilate(thresh, None, iterations = 3) #  Dilation
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # Find Contours (Array)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour) # Coordinate transformations
        print(cv2.contourArea(contour)) # Calculate area of the fixed object at any one time

        if cv2.contourArea(contour) < 3500: # If the fixed aria less than 3500 px
            continue

        blur_frame = cv2.blur(frame_1, ksize = (1000,1000))
        gray = cv2.cvtColor(frame_1, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 3, 5)
        for (x,y,w,h) in faces:

            face = frame_1 [y:y+h,x:x+w]
            blur_frame = cv2.blur(frame_1,ksize = (15,15))
            blur_frame[y:y+h,x:x+w] = face

        cv2.imshow("original",blur_frame)
        #cv2.rectangle(frame_1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #cv2.putText(frame_1, "{}".format("Attention"), (500, 400), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255), 3, cv2.LINE_AA) # Alarm text

    cv2.imshow("frame1", frame_1)
    frame_1 = frame_2
    ret, frame_2 = test_video.read()

    if cv2.waitKey(40) == 27:
        break

# Release the video capture object and close the frames
test_video.release()
cv2.destroyAllWindows()

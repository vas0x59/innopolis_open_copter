import ColorClassifier.RegColor as rc
import cv2
import numpy as np 


cap = cv2.VideoCapture(2)


while cv2.waitKey(1) != ord('q'):
    ret, frame = cap.read()
    color = rc.regSum(frame)
    cv2.imshow("frame", frame)
    print(color)
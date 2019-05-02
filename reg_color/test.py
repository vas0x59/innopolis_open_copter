import RegColor as rc
import cv2
import numpy as np 


cap = cv2.VideoCapture(1)


while cv2.waitKey(1) != ord('q'):
    ret, frame = cap.read()
    color = rc.regSum(frame)
    print(color)
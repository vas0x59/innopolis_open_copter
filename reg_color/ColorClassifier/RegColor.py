import cv2
import numpy as np

labels = ["red", "yellow", "green", "blue", "none"]
colors = {
    "red":(20, 10, 80), "yellow":(0, 125, 125), "green":(70, 100, 60), "blue":(100, 150, 180)
}

def regSum(img):
    color = "none"
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #bgr
    r_mean = np.mean(img[:, :, 2]) 
    g_mean= np.mean(img[:, :, 1]) 
    b_mean = np.mean(img[:, :, 0]) 
    a = np.array((b_mean ,g_mean, r_mean))
    max_c = "none"
    max_d = 0
    for i in colors:
        b = np.array(colors[i])
        dist = 1-np.linalg.norm(a-b) / 255
        # print(dist)
        if dist > 0.6:
            if dist  > max_d:
                max_c = i
                max_d = dist
    color = max_c
    return color

def regConturs(img):
    color = "none"
    return color
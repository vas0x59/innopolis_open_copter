import cv2
import numpy as np

labels = ["red", "yellow", "green", "blue", "none"]
colors = {
    "red":[
        (0, 180, 180), (20, 230, 230)
    ], 
    "yellow":[
        (20, 190, 170), (64, 220, 190)
    ], 
    "green":[
        (64, 100, 160), (90, 130, 190)
    ], 
    "blue":[
        (90, 180, 215), (140, 210, 225)
    ]
}
def regSum(img):
    color = "none"
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    c_mean = 0
    for c in colors:
        color_l = colors[c][0]
        color_u = colors[c][1]
        cc_mean = np.mean(cv2.inRange(img, color_l, color_u)[:, :]) / 255
        # print(cc_mean)
        if cc_mean > 0.2 and cc_mean > c_mean:
            color = c
    
    # #bgr
    # r_mean = np.mean(img[:, :, 2]) 
    # g_mean= np.mean(img[:, :, 1]) 
    # b_mean = np.mean(img[:, :, 0]) 
    # a = np.array((b_mean ,g_mean, r_mean))
    # print(a)
    # max_c = "none"
    # max_d = 0
    # for i in colors:
    #     b = np.array(colors[i])
    #     dist = 1-np.linalg.norm(a-b) / 255
    #     # print(dist)
    #     if dist > 0.6:
    #         if dist  > max_d:
    #             max_c = i
    #             max_d = dist
    # color = max_c
    return color

def regSumE(img):
    color = "none"
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #bgr
    r_mean = np.mean(img[:, :, 2]) 
    g_mean= np.mean(img[:, :, 1]) 
    b_mean = np.mean(img[:, :, 0]) 
    a = np.array((b_mean ,g_mean, r_mean))
    print(a)
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
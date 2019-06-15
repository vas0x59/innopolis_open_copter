import cv2
import numpy as np

labels = ["red", "yellow", "green", "blue", "none"]
colors = {
    "red":[
        (0, 116, 180), (13, 255, 255), (161, 116, 180), (180, 255, 255)
    ], 
    "yellow":[
        (13,  56, 132), (45, 255, 255) #13  56 132] [ 45 255 255
    ], 
    "green":[
        (55, 80, 50), (100, 255, 255) #72 103  65] [ 89 255 255
    ], 
    "blue":[
        (100, 116, 131), (153, 255, 255)
    ]
}
def regSum(img):
    color = "none"
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    c_mean = 0
    for c in colors:
        if len(colors[c]) == 2:
            color_l = colors[c][0]
            color_u = colors[c][1]
            cc_mean = np.mean(cv2.inRange(img, color_l, color_u)[:, :]) / 255
            if cc_mean > 0.2 and cc_mean > c_mean:
                color = c   
        elif len(colors[c]) == 4:
            color_l = colors[c][0]
            color_u = colors[c][1]
            color_l_2 = colors[c][2]
            color_u_2 = colors[c][3]
            mask1 = cv2.inRange(img, color_l, color_u)[:, :]
            mask2 = cv2.inRange(img, color_l_2, color_u_2)[:, :]
            mask = mask1 | mask2
            # cv2.imshow("mask", mask)
            cc_mean = np.mean(mask) / 255
            if cc_mean > 0.2 and cc_mean > c_mean:
                color = c   
        # print(cc_mean)
        
    
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
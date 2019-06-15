from ColorClassifier import RegColor
import rospy
import cv2
import numpy as np 
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


rospy.init_node('regColor')
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_AUTO_WB, 0)
image_pub = rospy.Publisher("image_topic_debug",Image)
string_pub = rospy.Publisher("color_reg", String)
# def callback(data):
#     try:
#       cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
#     except CvBridgeError as e:
#       print(e)

#     (rows,cols,channels) = cv_image.shape
#     cv2.imshow("Image window", cv_image)
#     cv2.waitKey(3)

bridge = CvBridge()

# image_sub = rospy.Subscriber("image_topic",Image,callback)
skip_i = 0
while True:
    _, cv_image = cap.read()
    if skip_i % 2:
        cv_image = cv2.resize(cv_image, (40, 40))
        image_pub.publish(bridge.cv2_to_imgmsg(cv_image, "bgr8"))
        color = RegColor.regSum(cv_image)
        # print(color)
        string_pub.publish(color)
    if skip_i >= 2000:
        skip_i = 0
    else:
        skip_i+=1
    # cv2.imshow("Image window", cv_image)
    # cv2.waitKey(1)
cap.release()
rospy.spin()
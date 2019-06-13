from ColorClassifier import RegColor
import rospy
import cv2
import numpy as np 
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


rospy.init_node('regColor')
# image_pub = rospy.Publisher("image_topic_2",Image)
def callback(data):
    try:
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)
    
    # (rows,cols,channels) = cv_image.shape
    # cv2.imshow("Image window", cv_image)
    # cv2.waitKey(3)

bridge = CvBridge()
image_sub = rospy.Subscriber("image_topic",Image,callback)

rospy.spin()
import rospy
from clever import srv
from std_srvs.srv import Trigger
from mavros_msgs.srv import CommandBool
import math
import time
import Utils

points = {"takeoff":(2.3, 2, 1.3),"ring":(2.8, 1.4, 0.5),"gate":(1.9, 0.5, 0.5),"land": (0.27, 2.05, 1.3)}
corners = {"upper-right":(2.4, 0.5, 0.5), "upper-left":(0.2, 0.2, 0.5)}
copter = Utils.Copter(markers_flipped=True)
copter.start_coord = points["takeoff"]
copter.callib_zero_z()

copter.takeoff(1.5)
print("takeoff compl")
rospy.sleep(0.5)

print("go to tk point")
copter.go_to_point(points["takeoff"])
print("hold tk point")
rospy.sleep(3)

print("going to ring")
copter.go_to_point(points["ring"])

copter.go_to_point(corners["upper-right"])
print("going to gate")

copter.go_to_point(points["gate"])
print("going to landing point")

copter.go_to_point(corners["upper-left"])

print("go to tk land")
copter.go_to_point(points["land"])
print("hold tk land")
rospy.sleep(3)
print("land")
copter.land()
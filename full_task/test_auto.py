import rospy
from clever import srv
from std_srvs.srv import Trigger
from mavros_msgs.srv import CommandBool
import math
import time

import Utils

points = {"takeoff":(2.76, 1.5, 1.3), "land": (0.33, 1.5, 1.3)}

magnit = Utils.Magnet()
magnit.off()

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

print("go to tk land")
copter.go_to_point(points["land"])
print("hold tk land")
rospy.sleep(3)
# magnit.off()
print("land")
copter.land()
# copter.go_to_point((0, 0, 1.8))


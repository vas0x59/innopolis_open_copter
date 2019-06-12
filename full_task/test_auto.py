import rospy
from clever import srv
from std_srvs.srv import Trigger
from mavros_msgs.srv import CommandBool
import math
import time

import Utils

points = {"takeoff":(0, 0, 1.5), "land": (1, 0, 1.5)}

magnit = Utils.Magnet()
magnit.off()

copter = Utils.Copter(markers_flipped=True)
copter.start_coord = points["takeoff"]
copter.zero_z()

copter.takeoff(1.5)
rospy.sleep(0.5)


copter.go_to_point(points["takeoff"])
rospy.sleep(5)
copter.go_to_point(points["land"])

# magnit.off()

copter.land()
# copter.go_to_point((0, 0, 1.8))


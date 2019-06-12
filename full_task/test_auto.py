import rospy
from clever import srv
from std_srvs.srv import Trigger
from mavros_msgs.srv import CommandBool
import math
import time

import Utils
magnit = Utils.Magnet()
# magnit.off()

copter = Utils.Copter(markers_flipped=True)
copter.zero_z()

copter.takeoff(1.5)

time.sleep(5)
magnit.off()

copter.land()
# copter.go_to_point((0, 0, 1.8))


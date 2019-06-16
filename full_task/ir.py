import rospy
from clever import srv
from std_srvs.srv import Trigger
from mavros_msgs.srv import CommandBool
import math
import time
import Utils

rospy.init_node("flight")
points = {
    "takeoff":(2.3, 1.85, 0.8),
    # "ring":(2.8, 1.4, 0.5),
    # "gate":(1.9, 0.5, 0.5),
    "land": (0.355, 1.85, 1.3),
    "land_2": (0.355, 1.85, 0.185)
}
gate_points = {
    "gate_1":(2.2, -0.3, 0.5),
    "gate_2":(1, -0.3, 0.5)
}
ungrab_points = {
    "ungrab_hover":(0.29, -0.15, 0.7)
    # "grab":(1, 1, 0.4)
}
grab_points = {
    "grab_hover":(0.29, -0.15, 0.7)
    # "grab":(1, 1, 0.4)
}
ring_points = {
    "ring_1":(2.35, 1.8, 0.35),
    "ring":(2.35, 1, 0.35),
    "ring_2":(2.35, 0.18, 0.35)
}
corners = {
    "upper-right":(2.4, 0.2, 1), 
    "upper-left":(0.2, 0.2, 1),
    "lower-right":(2.4, 2.4, 1), 
    "lower-left":(0.2, 0.4, 1)
}
monitoring_points = {
    "1":(2.45, 1.6, 0.4),
    "2":(2.45, -0.3, 0.4),
    "3":(0.355, 1.55, 0.4),
    "4":(0.355, 1.75, 0.4),
}

def takeoff():
    copter.takeoff(1)
    print("takeoff compl")
    rospy.sleep(0.5)
    print("go to tk point")
    copter.go_to_point(points["takeoff"])
    print("hold tk point")
    rospy.sleep(8)
def mon1():
    copter.go_to_point(monitoring_points["1"], yaw=math.radians(90))
    rospy.sleep(2)
    rospy.sleep(3)

def land():
    print("go to land")
    copter.go_to_point(points["land"], tolerance=0.19)
    print("hold land")
    rospy.sleep(4)
    copter.go_to_point(points["land_2"])
    rospy.sleep(0.5)
    print("land")
    copter.land()
ir = Utils.IR()
rospy.init_node("flight")
copter = Utils.Copter(markers_flipped=True)
copter.start_coord = points["takeoff"]
# copter.zero_z = 2.5
copter.callib_zero_z()
# ir_cmds = {"qw2e":"land"}
tasks = {"land":land, "takeoff":takeoff, "mon1":mon1}
missions = {"qw2e":["land", "takeoff", "mon1"]}
while True:
    try:
        d = ir.waitData()
        # ir_cmd = ir_cmds[d]
        mission = missions[d]
        print(mission)
        for i in mission:
            tasks[i]()
    except KeyboardInterrupt:
        break

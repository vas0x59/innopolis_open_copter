import rospy
from clever import srv
from std_srvs.srv import Trigger
from mavros_msgs.srv import CommandBool
import math
import time
import Utils

points = {
    "takeoff":(2.3, 2, 1.3),
    # "ring":(2.8, 1.4, 0.5),
    # "gate":(1.9, 0.5, 0.5),
    "land": (0.27, 2.05, 1.3)
}
gate_points = {
    "gate_1":(2.2, 0.5, 0.5),
    "gate_2":(1.4, 0.5, 0.5)
}
grab_points = {
    "grab_hover":(1, 1,0.4)
    # "grab":(1, 1, 0.4)
}
ring_points = {
    "ring_1":(2.8, 1.7, 0.5),
    "ring_2":(2.8, 0.8, 0.5)
}
corners = {
    "upper-right":(2.4, 0.2, 1), 
    "upper-left":(0.2, 0.2, 1),
    "lower-right":(2.4, 2.4, 1), 
    "lower-left":(0.2, 0.4, 1)
}
monitoring_points = {
    "1":(),
    "2":(),
    "3":(),
    "4":(),
}

rospy.init_node("flight")

color_sub = Utils.ColorReg()

copter = Utils.Copter(markers_flipped=True)
copter.start_coord = points["takeoff"]
copter.zero_z = 2.5


def gate():
    print("going to gate_1")
    copter.go_to_point(gate_points["gate_1"])
    print("going to gate_2")
    copter.go_to_point(gate_points["gate_2"])
    print("gate done")

def takeoff():
    copter.takeoff(1.5)
    print("takeoff compl")
    rospy.sleep(0.5)
    print("go to tk point")
    copter.go_to_point(points["takeoff"])
    print("hold tk point")
    rospy.sleep(3)

def ring():
    print("going to ring_1")
    copter.go_to_point(ring_points["ring_1"])
    print("going to ring_2")
    copter.go_to_point(ring_points["ring_2"])
    print("ring done")
def land():
    print("go to land")
    copter.go_to_point(points["land"])
    print("hold land")
    rospy.sleep(3)
    print("land")
    copter.land()
def grab():
    print("going to grab")
    copter.go_to_point(grab_points["grab_hover"])
    copter.land()
    rospy.sleep(5)
    copter.takeoff(1.5)
    copter.go_to_point(grab_points["grab_hover"])
    print("grab done")
def monitoring():
    pass
    
# def grab():



# ros_tools = Utils.RosTools()


# copter.callib_zero_z()

takeoff()
ring()
gate()
land()
copter.arming(False)
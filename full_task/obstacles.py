import rospy
from clever import srv
from std_srvs.srv import Trigger
from mavros_msgs.srv import CommandBool
import math
import time
import Utils
from Leds import Leds
from rpi_ws281x import Color

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
    "ungrab_hover":(0.29, -0.15, 0.6)
    # "grab":(1, 1, 0.4)
}
grab_points = {
    "grab_hover":(1.54, 0.68, 0.6),
    "grab_grab":(1.54, 0.68, 0.20)
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
stand_points = {
    "stand_1_up_approach":(2, 1.85, 1.4),
    "stand_1_down_approach":(2, 1.85, 0.4),
    "stand_2_up_approach":(0.6, 1.85, 1.4),
    "stand_2_down_approach":(0.6, 1.85, 0.4)
}

led = Leds(21)

magnet = Utils.Magnet()

rospy.init_node("flight")

color_sub = Utils.ColorReg()

copter = Utils.Copter(markers_flipped=True)
copter.start_coord = points["takeoff"]
copter.zero_z = 2.54
# copter.callib_zero_z()


def gate():
    print("going to gate_1")
    copter.go_to_point(gate_points["gate_1"])
    print("going to gate_2")
    copter.go_to_point(gate_points["gate_2"])
    print("gate done")

def takeoff():

    led.setPixelsColor(Utils.led_colors["takeoff"])
    copter.takeoff(1)
    led.setPixelsColor(Utils.led_colors["none"])

    print("takeoff compl")
    rospy.sleep(0.5)
    print("go to tk point")
    copter.go_to_point(points["takeoff"])
    print("hold tk point")
    
    led.setPixelsColor(Utils.led_colors["wait"])
    rospy.sleep(5)
    led.setPixelsColor(Utils.led_colors["none"])

def ring():
    print("going to ring_1")
    copter.go_to_point(ring_points["ring_1"])
    rospy.sleep(2)
    print("going to ring")
    copter.go_to_point(ring_points["ring"], speed=0.8)
    print("going to ring_2")
    copter.go_to_point(ring_points["ring_2"], speed=0.8)
    rospy.sleep(2)
    print("ring done")

def land():
    print("go to land")
    copter.go_to_point(points["land"], tolerance=0.19)
    print("hold land")
    rospy.sleep(4)

    led.setPixelsColor(Utils.led_colors["land"])
    copter.go_to_point(points["land_2"])
    rospy.sleep(0.5)
    print("land")
    copter.land()
    led.setPixelsColor(Utils.led_colors["none"])

def ungrab():
    print("going to ungrab")
    copter.go_to_point(ungrab_points["ungrab_hover"], tolerance=0.19)
    rospy.sleep(3)
    copter.land()
    rospy.sleep(4)
    print("magnet off")
    magnet.off()
    rospy.sleep(3)
    copter.takeoff(1.5)
    copter.go_to_point(ungrab_points["ungrab_hover"])
    print("ungrab done")

def mon1():
    copter.go_to_point(monitoring_points["1"], yaw=math.radians(90))
    rospy.sleep(2)
    color_sub.color = "blue"
    led.setPixelsColor(Utils.led_colors[color_sub.color])
    rospy.sleep(3)
    led.setPixelsColor(Utils.led_colors["none"])

def mon2():
    copter.go_to_point(monitoring_points["2"], yaw=math.radians(90))
    rospy.sleep(2)
    color_sub.color = "red"
    led.setPixelsColor(Utils.led_colors[color_sub.color])
    rospy.sleep(3)
    led.setPixelsColor(Utils.led_colors["none"])

def mon3():
    copter.go_to_point(monitoring_points["3"], yaw=math.radians(270))
    rospy.sleep(2)
    color_sub.color = "yellow"
    led.setPixelsColor(Utils.led_colors[color_sub.color])
    rospy.sleep(3)
    led.setPixelsColor(Utils.led_colors["none"])

def mon4():
    copter.go_to_point(monitoring_points["4"], yaw=math.radians(270))
    rospy.sleep(2)
    color_sub.color = "green"
    led.setPixelsColor(Utils.led_colors[color_sub.color])
    rospy.sleep(3)
    led.setPixelsColor(Utils.led_colors["none"])

def stand(p):
    speed = 0.8
    delay_time = 1
    if p == "up":
        copter.go_to_point(stand_points["stand_1_up_approach"], tolerance=0.2, speed=speed)
        rospy.sleep(delay_time)
        copter.go_to_point(stand_points["stand_2_up_approach"], tolerance=0.2, speed=speed)
        rospy.sleep(delay_time)
        copter.go_to_point(stand_points["stand_2_down_approach"], tolerance=0.2, speed=speed)
        rospy.sleep(delay_time)
        copter.go_to_point(stand_points["stand_1_down_approach"], tolerance=0.2, speed=speed)
        rospy.sleep(delay_time)
    elif p == "down":
        copter.go_to_point(stand_points["stand_1_down_approach"], tolerance=0.2, speed=speed)
        rospy.sleep(delay_time)
        copter.go_to_point(stand_points["stand_2_down_approach"], tolerance=0.2, speed=speed)
        rospy.sleep(delay_time)
        copter.go_to_point(stand_points["stand_2_up_approach"], tolerance=0.2, speed=speed)
        rospy.sleep(delay_time)
        copter.go_to_point(stand_points["stand_1_up_approach"], tolerance=0.2, speed=speed)
        rospy.sleep(delay_time)

# def mon(i):
#     copter.go_to_point(monitoring_points[str(i)])
#     rospy.sleep(4)
    
def grab():
    print("going to grab")
    copter.go_to_point(grab_points["grab_hover"], tolerance=0.19)
    rospy.sleep(3)
    # copter.land()
    # rospy.sleep(4)
    print("magnet on")
    magnet.on()
    for i in range(6):
        copter.go_to_point(grab_points["grab_grab"], tolerance=0.25, speed=0.8)
        rospy.sleep(1)
        copter.go_to_point(grab_points["grab_hover"], tolerance=0.28, speed=0.8)
        rospy.sleep(0.5)

    # copter.takeoff(1.5)
    copter.go_to_point(grab_points["grab_hover"])
    print("grab done")



# ros_tools = Utils.RosTools()


magnet.off()

takeoff()
grab()

# mon1()
# ring()
# mon2()
# gate()
# ungrab()
mon3()
# mon4()
magnet.off()

land()
print("disarm")
copter.arming(False)
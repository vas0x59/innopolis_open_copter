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
    "takeoff_up":(0.155, 0.138, 1.8),
    "takeoff_up_up":(0.155, 0.138, 1.5),
    "takeoff_2":(0.156, 0.143, 2.88),
    "takeoff_down":(0.155, 0.138, 1.8),
    # "ring":(2.8, 1.4, 0.5),
    # "gate":(1.9, 0.5, 0.5),
    "land": (2.9, 0.26, 2.0),
    "land_2": (2.9, 0.26, 2.88)
}
gate_points = {
    "gate_1":(1.17, 2.76, 2.67),
    "gate_2":(2.03, 2.76, 2.67)
}
ungrab_points = {
    "ungrab_hover":(3, 2.87, 2),
    "ungrab_ungrab": (3, 2.87, 2.5)
    
    # "grab":(1, 1, 0.4)
}
grab_points = {
    "grab_hover":(1.47, 1.53, 2),
    "grab_grab":(1.61, 1.61, 2.8)
    # "grab":(1, 1, 0.4)
}
ring_points = {
    "ring_1":(0.255, 0.8,  2.3),
    "ring":(0.085, 1.5,  2.22),
    "ring_2":(0.255, 1.93, 2.3)
}
corners = {
    "upper-right":(2.4, 0.2, 1), 
    "upper-left":(0.2, 0.2, 1),
    "lower-right":(2.4, 2.4, 1), 
    "lower-left":(0.2, 0.4, 1)
}
monitoring_points = {
    "1":(0.32,  0.40, 1.91),
    "2":(0.28,  2.15,  1.85),
    "3":(3.12, 0.22, 2.0),
    "4":(3.06, 2.08,  2.1)
}
stand_points = {
    "stand_1_up_approach":(0.35, 0.242, 1.25),
    "stand_1_down_approach":(0.35, 0.242, 2.67),
    "stand_2_up_approach":(2.60, 0.245, 1.28),
    "stand_2_down_approach":(2.60, 0.245, 2.67)
}

super_gate_points = {
    "1": (0.9, 2.9, 2.64),
    "2": (1.83, 2.9, 2.67),
    "3": (1.83, 2.9, 1.6),
    "4": (0.9, 2.9, 1.6)
}

super_ring_points = {
    "1": (0.255, 1.88, 2.3),
    "2": (0.255, 1.08, 2.3),
    "3": (0.255, 1.08, 1.6),
    "4": (0.255, 1.88, 1.6)
}

ir_points = {
    "1":(0.18, 2.95, 2.25),
    "2":(0.18, 2.95, 1.5)
}

led = Leds(21)

magnet = Utils.Magnet()

rospy.init_node("flight")

color_sub = Utils.ColorReg()

copter = Utils.Copter(markers_flipped=True)
copter.start_coord = points["takeoff_down"]
copter.zero_z = 3
# copter.callib_zero_z()


def gate():
    print("going to gate_1")
    copter.go_to_point(gate_points["gate_1"])
    print("going to gate_2")
    copter.go_to_point(gate_points["gate_2"])
    print("gate done")

def takeoff(p):

    led.setPixelsColor(Utils.led_colors["takeoff"])
    copter.takeoff(1)
    led.setPixelsColor(Utils.led_colors["none"])

    print("takeoff compl")
    rospy.sleep(0.5)
    print("go to tk point")
    if p == "up":
        copter.go_to_point(points["takeoff_up"])
    else:
        copter.go_to_point(points["takeoff_down"])

    print("hold tk point")
    
    # led.setPixelsColor(Utils.led_colors["wait"])
    # rospy.sleep(11)
    rospy.sleep(11)
    led.setPixelsColor(Utils.led_colors["none"])

def ring():
    print("going to ring_1")
    copter.go_to_point(ring_points["ring_1"], speed=0.35)
    rospy.sleep(2)
    # print("going to ring")
    # copter.go_to_point(ring_points["ring"], speed=0.35)
    print("going to ring_2")
    copter.go_to_point(ring_points["ring_2"], speed=0.35)
    rospy.sleep(2)
    print("ring done")

def land():
    print("go to land")
    copter.go_to_point(points["land"], tolerance=0.19, speed=0.35)
    print("hold land")
    rospy.sleep(2)

    led.setPixelsColor(Utils.led_colors["land"])
    copter.go_to_point(points["land_2"])
    rospy.sleep(0.5)
    print("land")
    copter.land()
    led.setPixelsColor(Utils.led_colors["none"])

def ungrab():
    print("going to ungrab")
    copter.go_to_point(ungrab_points["ungrab_hover"], tolerance=0.19, speed=0.35)
    rospy.sleep(2)
    copter.go_to_point(ungrab_points["ungrab_ungrab"], tolerance=0.19)
    # rospy.sleep(0.5)
    # copter.land()
    # rospy.sleep(2)
    # print("magnet off")
    magnet.off()
    # rospy.sleep(2)
    # copter.takeoff(1)
    
    # rospy.sleep(3)
    copter.go_to_point(ungrab_points["ungrab_hover"])
    print("ungrab done")

def mon1():
    copter.go_to_point(monitoring_points["1"], speed=0.35)
    rospy.sleep(1)
    color_sub.color = "red"
    led.setPixelsColor(Utils.led_colors[color_sub.color])
    rospy.sleep(4)
    led.setPixelsColor(Utils.led_colors["none"])

def mon2():
    copter.go_to_point(monitoring_points["2"], speed=0.35)
    rospy.sleep(1)
    color_sub.color = "green"
    led.setPixelsColor(Utils.led_colors[color_sub.color])
    rospy.sleep(4)
    led.setPixelsColor(Utils.led_colors["none"])

def mon3():
    copter.go_to_point(monitoring_points["3"], speed=0.35)
    rospy.sleep(1)
    color_sub.color = "yellow"
    led.setPixelsColor(Utils.led_colors[color_sub.color])
    rospy.sleep(4)
    led.setPixelsColor(Utils.led_colors["none"])

def mon4():
    copter.go_to_point(monitoring_points["4"], speed=0.35)
    rospy.sleep(1)
    color_sub.color = "blue"
    led.setPixelsColor(Utils.led_colors[color_sub.color])
    rospy.sleep(4)
    led.setPixelsColor(Utils.led_colors["none"])

def stand(p):
    speed = 0.6
    delay_time = 1.2
    magnet.on()
    if p == "up":
        copter.go_to_point(stand_points["stand_1_up_approach"], tolerance=0.2, speed=speed)
        rospy.sleep(delay_time)
        copter.go_to_point(stand_points["stand_2_up_approach"], tolerance=0.2, speed=speed)
        rospy.sleep(delay_time)

        mon3()


        copter.go_to_point(stand_points["stand_2_down_approach"], tolerance=0.2, speed=speed)
        rospy.sleep(delay_time)
        copter.go_to_point(stand_points["stand_1_down_approach"], tolerance=0.2, speed=speed)
        rospy.sleep(delay_time+1)
        magnet.off()
    elif p == "down":
        copter.go_to_point(stand_points["stand_1_down_approach"], tolerance=0.2, speed=speed)
        rospy.sleep(delay_time)
        copter.go_to_point(stand_points["stand_2_down_approach"], tolerance=0.2, speed=speed)
        rospy.sleep(delay_time)

        mon3()

        copter.go_to_point(stand_points["stand_2_up_approach"], tolerance=0.2, speed=speed)
        rospy.sleep(delay_time)
        copter.go_to_point(stand_points["stand_1_up_approach"], tolerance=0.2, speed=speed)
        rospy.sleep(delay_time+1)
        magnet.off()

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
    for i in range(4):
        copter.go_to_point(grab_points["grab_grab"], tolerance=0.25, speed=0.35)
        rospy.sleep(1)
        copter.go_to_point(grab_points["grab_hover"], tolerance=0.245, speed=0.35)
        rospy.sleep(0.5)

    # copter.takeoff(1.5)
    copter.go_to_point(grab_points["grab_hover"])
    print("grab done")

def super_ring():
    speed = 0.35
    delay_time = 0.5
    copter.go_to_point(super_ring_points["1"], tolerance=0.2, speed=speed)
    rospy.sleep(delay_time)
    copter.go_to_point(super_ring_points["2"], tolerance=0.2, speed=speed)
    rospy.sleep(delay_time)
    copter.go_to_point(super_ring_points["3"], tolerance=0.2, speed=speed)
    rospy.sleep(delay_time)
    copter.go_to_point(super_ring_points["4"], tolerance=0.2, speed=speed)
    rospy.sleep(delay_time)
    copter.go_to_point(super_ring_points["1"], tolerance=0.2, speed=speed)

def super_gate():
    speed = 0.35
    delay_time = 0.5
    copter.go_to_point(super_gate_points["1"], tolerance=0.2, speed=speed)
    rospy.sleep(delay_time)
    copter.go_to_point(super_gate_points["2"], tolerance=0.2, speed=speed)
    rospy.sleep(delay_time)
    copter.go_to_point(super_gate_points["3"], tolerance=0.2, speed=speed)
    rospy.sleep(delay_time)
    copter.go_to_point(super_gate_points["4"], tolerance=0.2, speed=speed)
    rospy.sleep(delay_time)
    copter.go_to_point(super_gate_points["1"], tolerance=0.2, speed=speed)

def super_landing_blue():
    led.setPixelsColor(Utils.led_colors["blue"])
    copter.go_to_point(ir_points["2"])
    copter.go_to_point(points["takeoff_up_up"])
    rospy.sleep(2)
    copter.go_to_point(points["takeoff_2"])

    rospy.sleep(0.5)
    print("land")
    copter.land()
    copter.arming(False)
    led.setPixelsColor(Utils.led_colors["none"])
    rospy.sleep(5)
    takeoff("down")
    copter.go_to_point(points["takeoff_up_up"])
    copter.go_to_point(ir_points["2"])

def super_landing_purple():
    led.setPixelsColor(Utils.led_colors["takeoff"])
    copter.go_to_point(ir_points["2"])
    copter.go_to_point(points["takeoff_up_up"])
    rospy.sleep(2)
    copter.go_to_point(points["takeoff_2"])

    rospy.sleep(0.5)
    print("land")
    copter.land()
    copter.arming(False)
    led.setPixelsColor(Utils.led_colors["none"])
    rospy.sleep(5)
    takeoff("down")
    copter.go_to_point(points["takeoff_up_up"])
    copter.go_to_point(ir_points["2"])

def super_desk():
    led.setPixelsColor(Utils.led_colors["yellow"])
    copter.go_to_point(ir_points["1"])

    # gate()

    copter.go_to_point(grab_points["grab_hover"])
    rospy.sleep(2)
    # copter.go_to_point(grab_points["grab_grab"])

    # rospy.sleep(0.5)
    # print("land")
    # copter.land()
    # copter.arming(False)
    # copter.takeoff(1)
    # copter.go_to_point(grab_points["grab_hover"])
    led.setPixelsColor(Utils.led_colors["none"])
    # rospy.sleep(5)
    # takeoff()
# def


# ros_tools = Utils.RosTools()


# magnet.off()
ir = Utils.IR()

magnet.on()

takeoff("down")
mon1()
stand("down")
# copter.go_to_point((2.38,0.69,1.2))
ring()

# grab()
# ungrab()
# print("stoooop")
# rospy.sleep(5)

copter.go_to_point(ir_points["1"])
rospy.sleep(1)
# tasks = {"land":land, "takeoff":takeoff, "ring":ring}
# missions = {"b04f":["ring", ""]}
desription = {
    "6897":"Noose through Ring", 
    "9867":"Noose through Gate", 
    "b04f":"Fly to start point with purple led and landing", 
    "30cf":"Fly to start point with blue led and landing", 
    "18e7":"Fly to payload zone with yellow led and landing"
}
ir_cmds = ["6897", "9867", "b04f", "30cf", "18e7"]

ccc = ir.waitData(ir_cmds)
# ccc = "9867"
print(desription[ccc])
rospy.sleep(0.2)
if ccc == "6897":
    print("Ring")
    super_ring()
elif ccc == "9867":
    print("Gate")
    super_gate()
elif ccc == "b04f":
    print("Purple_Landing")
    led.setPixelsColor(Utils.led_colors["takeoff"])
    super_landing_purple()
elif ccc == "30cf":
    print("Blue_Landing")
    led.setPixelsColor(Utils.led_colors["blue"])
    super_landing_blue()
elif ccc == "18e7":
    led.setPixelsColor(Utils.led_colors["yellow"])
    print("Yellow_Desk")
    super_desk()
else:
    print("None")

copter.go_to_point(ir_points["1"])
# mon2()
gate()
mon4()
# mon3()
grab()

# stand("down")
# mon1()
# mon4()
# mon3()

# grab()
ungrab()
# grab()

# mon1()

# mon2()
# gate()
# ungrab() 
# mon3()
# mon4()
# magnet.off()

land()
print("disarm")
copter.arming(False)
magnet.off()
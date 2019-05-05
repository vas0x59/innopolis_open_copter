# -*- coding: utf-8 -*-

import rospy
from clever import srv
from std_srvs.srv import Trigger
import math

from Leds import Leds
from rpi_ws281x import Color
import time

led = Leds(36)
led_colors = {"takeoff":Color(200,0,200), "wait":Color(140,220,0), "rec":Color(0,0,0), "land":Color(225,90,0)}
start_coord = [0.5, 0.5]


rospy.init_node('flight')

from mavros_msgs.srv import CommandBool
arming = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

def get_distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)


def navigate_wait(x=0, y=0, z=0, speed=0, frame_id='aruco_map', auto_arm=False, tolerance=0.2, yaw=float('nan')):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)
    while True:
        telem = get_telemetry(frame_id=frame_id)
        # Вычисляем расстояние до заданной точки
        if get_distance(x, y, z, telem.x, telem.y, telem.z) < tolerance:
            # Долетели до необходимой точки
            break
        rospy.sleep(0.2)


z = 1

led.setPixelsColor(led_colors["takeoff"])
print("takeoff")

tolerance = 0.2
start = get_telemetry()

navigate(z=z, speed=0.56, frame_id="body", auto_arm=True)

rospy.sleep(2)

z = 1.3

print("go to wait point")
navigate_wait(x=start_coord[0], y=start_coord[1], z=z, speed=0.5, frame_id="aruco_map", yaw=float('nan'))
led.setPixelsColor(led_colors["wait"])

print("wait")
rospy.sleep(5.5)

led.setPixelsColor(led_colors["land"])
print("land")
land()

rospy.sleep(3)
print("disarm")
arming(False)
led.setPixelsColor(Color(0, 0, 0))
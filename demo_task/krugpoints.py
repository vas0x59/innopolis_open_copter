# -*- coding: utf-8 -*-

import rospy
from clever import srv
from std_srvs.srv import Trigger
import math

from Leds import Leds
from rpi_ws281x import Color
import time
import numpy as np
circle_center = [1.25, 1.25]
def circle(c,r,n):
  a = []
  for i in np.arange(0, 361, 360/n):
    a.append([round(math.cos(math.radians(i)) * r + c[0], 2), round(math.sin(math.radians(i)) * r + c[1], 2)])
  return a
points = circle(circle_center,1,12)
led = Leds(36)
led_colors = {"takeoff":Color(200,0,200), "wait":Color(0,90,140), "rec":Color(225,50,5), "land":Color(225,90,0)}
start_coord = [1.8, 1]
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
        if get_distance(x, y, z, telem.x, telem.y, telem.z) < tolerance:
            break
        rospy.sleep(0.2)


z = 1

led.setPixelsColor(led_colors["takeoff"])
print("takeoff")

tolerance = 0.2
start = get_telemetry()

navigate(z=z, speed=0.56, frame_id="body", auto_arm=True)

rospy.sleep(2)

z = 1

navigate_wait(x=start_coord[0], y=start_coord[1], z=z, speed=0.5, frame_id="aruco_map")
led.setPixelsColor(led_colors["wait"])

rospy.sleep(3)

RADIUS = 1   # m
SPEED = 0.18  # rad / s


start_stamp = rospy.get_rostime()
circle_done=0
angle = 0
led.setPixelsColor(led_colors["rec"])

for i in points:
	navigate_wait(x=i[0], y=i[1], z=z, speed=0.5, frame_id="aruco_map")

navigate_wait(x=start_coord[0], y=start_coord[1], z=z, speed=0.5, frame_id="aruco_map")
led.setPixelsColor(led_colors["wait"])
rospy.sleep(2)
led.setPixelsColor(led_colors["land"])
land()

rospy.sleep(4)
arming(False)
led.setPixelsColor(Color(0, 0, 0))

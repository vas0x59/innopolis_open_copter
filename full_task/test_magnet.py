# -*- coding: utf-8 -*-
import time
from Leds import Leds
from rpi_ws281x import Color
import time
import rospy
from clever import srv
from std_srvs.srv import Trigger
import pigpio
led = Leds(30)
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
print(get_telemetry(frame_id="body"))
led_colors = {"takeoff":Color(200,0,200), "wait":Color(140,220,0), "rec":Color(0,0,0), "land":Color(225,90,0)}
pi = pigpio.pi()
pi.set_mode(15, pigpio.OUTPUT)
pi.write(15, 1)
led.setPixelsColor(led_colors["wait"])
print("WAITING 5 SECONDS")
time.sleep(5)
print("TURNING OFF THE MAGNET")
pi.write(15, 0)
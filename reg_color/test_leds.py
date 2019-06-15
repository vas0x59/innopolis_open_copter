from Leds import Leds
from rpi_ws281x import Color
import time
import rospy
from clever import srv
from std_srvs.srv import Trigger

led = Leds(21)

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
print(get_telemetry(frame_id="body"))

led_colors = {"takeoff":Color(200,0,200), "wait":Color(140,220,0), "rec":Color(0,0,0), "land":Color(225,90,0)}

led.setPixelsColor(led_colors["takeoff"])

time.sleep(1)

led.setPixelsColor(led_colors["wait"])

time.sleep(1)

led.setPixelsColor(led_colors["land"])

time.sleep(1)

led.setPixelsColor(Color(0, 0, 0))


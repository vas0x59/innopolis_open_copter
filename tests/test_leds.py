from Leds import Leds
from rpi_ws281x import Color
import time
import rospy
from clever import srv
from std_srvs.srv import Trigger

led = Leds(36)

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
print(get_telemetry(frame_id="body"))
led.setPixelsColor(Color(200, 0, 200))

time.sleep(2)

led.setPixelsColor(Color(0, 0, 0))


from Leds import Leds
from rpi_ws281x import Color
import time

led = Leds(36)

led.setPixelsColor(Color(200, 0, 200))

time.sleep(2)

led.setPixelsColor(Color(0, 0, 0))

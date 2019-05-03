from Leds import Leds
import time

led = Leds(36)

led.setPixelsColor(200, 0, 200)

time.sleep(2)

led.setPixelsColor(0, 0, 0)

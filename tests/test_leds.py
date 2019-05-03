from Leds import Leds
import time

led = Leds(36)

led.setPixelsColor(100, 100, 0)

time.sleep(2)

led.setPixelsColor(0, 0, 0)

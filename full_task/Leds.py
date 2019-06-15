# -*- coding: utf-8 -*-

import time
from rpi_ws281x import Adafruit_NeoPixel
from rpi_ws281x import Color

class Leds:
    def __init__(self, count, pin=21, br=20):
        """
        LEDs
        """
        self.LED_COUNT = count
        LED_PIN        = pin      # GPIO пин, к которому вы подсоединяете светодиодную ленту
        LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = br     # Set to 0 for darkest and 255 for brightest
        LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL    = 0       # Set to '1' for GPIOs 13, 19, 41, 45 or 53

        self.strip = Adafruit_NeoPixel(self.LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)
        self.strip.begin()
    def setPixelsColor(self, color):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def setPixelColor(self, color, i):
        self.strip.setPixelColor(i, color)
        self.strip.show()

    def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)
# SPDX-FileCopyrightText: Melissa LeBlanc-Williams for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!
#
# Ported to Pillow by Melissa LeBlanc-Williams for Adafruit Industries from Code available at:
# https://learn.adafruit.com/adafruit-oled-displays-for-raspberry-pi/programming-your-display

# Imports the necessary libraries...
import socket
import fcntl
import struct
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# This function allows us to grab any of our IP addresses
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(
        fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack("256s", str.encode(ifname[:15])),
        )[20:24]
    )


STATUS = ""

# Very important... This lets py-gaugette 'know' what pins to use in order to reset the display
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(64, 32, i2c)

# This sets TEXT equal to whatever your IP address is, or isn't
try:
    STATUS = get_ip_address("wlan0")  # WiFi address of WiFi adapter. NOT ETHERNET
except IOError:
    try:
        STATUS = get_ip_address("eth0")  # WiFi address of Ethernet cable. NOT ADAPTER
    except IOError:
        STATUS = "NO INTERNET!"

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load a font in 2 different sizes.
font = ImageFont.load("./tom-thumb.pil")

# Draw the text
draw.text((0, 0), "Your IP Address is:", font=font, fill=255)
draw.text((0, 7), STATUS, font=font, fill=255)

# Display image
image.rotate(180) # the display is upside down
oled.image(image)
oled.show()


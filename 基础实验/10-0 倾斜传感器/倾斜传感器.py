from machine import Pin
import time


p13 = Pin(13, Pin.IN)

while True:
    print(p13.value())
    time.sleep(0.1)

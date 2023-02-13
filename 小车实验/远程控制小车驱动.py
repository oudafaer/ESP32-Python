from machine import Pin
import time


# 定义GPIO引脚
# 控制1个电机
p13 = Pin(13, Pin.OUT)
p12 = Pin(12, Pin.OUT)
# 控制1个电机
p14 = Pin(14, Pin.OUT)
p27 = Pin(27, Pin.OUT)
# 控制1个电机
p15 = Pin(15, Pin.OUT)
p2 = Pin(2, Pin.OUT)
# 控制1个电机
p4 = Pin(4, Pin.OUT)
p16 = Pin(16, Pin.OUT)


def move_left():
    p13.value(1)
    p12.value(0)
    p14.value(0)
    p27.value(1)
    p15.value(0)
    p2.value(1)
    p4.value(1)
    p16.value(0)


def move_right():
    p13.value(0)
    p12.value(1)
    p14.value(1)
    p27.value(0)
    p15.value(1)
    p2.value(0)
    p4.value(0)
    p16.value(1)


def move_up():
    p13.value(1)
    p12.value(0)
    p14.value(1)
    p27.value(0)
    p15.value(1)
    p2.value(0)
    p4.value(1)
    p16.value(0)


def move_down():
    p13.value(0)
    p12.value(1)
    p14.value(0)
    p27.value(1)
    p15.value(0)
    p2.value(1)
    p4.value(0)
    p16.value(1)


def stop():
    p13.value(0)
    p12.value(0)
    p14.value(0)
    p27.value(0)
    p15.value(0)
    p2.value(0)
    p4.value(0)
    p16.value(0)



# move_up()
# stop()

"""
move_up()
time.sleep(2)
move_down()
time.sleep(2)
move_right()
time.sleep(2)
move_left()
time.sleep(2)
stop()
"""

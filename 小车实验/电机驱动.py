from machine import Pin
import time


# 定义GPIO引脚
# 控制1个电机
p13 = Pin(13, Pin.OUT)
p12 = Pin(12, Pin.OUT)
# 控制1个电机
p14 = Pin(14, Pin.OUT)
p27 = Pin(27, Pin.OUT)


while True:
    # 2个电机朝1个方向转2秒
    p13.value(1)
    p12.value(0)
    p14.value(1)
    p27.value(0)
    time.sleep(2)

    # 2个电机停止转动
    p13.value(0)
    p12.value(0)
    p14.value(0)
    p27.value(0)
    time.sleep(1)

    # 2个电机朝另外1个方向转2秒
    p13.value(0)
    p12.value(1)
    p14.value(0)
    p27.value(1)
    time.sleep(2)

    # 2个电机停止转动
    p13.value(0)
    p12.value(0)
    p14.value(0)
    p27.value(0)
    time.sleep(1)


import random
from machine import Pin, SPI,RTC
import st7789py
from romfonts import vga2_bold_16x32 as font
import time
import network
import ntptime

# 创建显示屏对象
tft = st7789py.ST7789(SPI(2, 10000000), 240, 240, reset=Pin(15), dc=Pin(2), cs=Pin(5), backlight=Pin(22), rotation=0)

# 屏幕显示蓝色
tft.fill(0)

week = ['Monday', 'Tuesday', 'Wednesay', 'Thursday', 'Friday', 'Saturday', 'Sunday']
time_list = ['', '', '']

class Clock:
    def __init__(self, wifi, password):
        self.rtc = RTC()
        self.wifi = wifi
        self.password = password
        self.ntp()  # 调用这个方法来联网设置时间
        
    def connect_wifi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            wlan.connect(self.wifi, self.password)

    def ntp(self):
        self.connect_wifi()
        time.sleep(2)
        ntptime.host="ntp1.aliyun.com"
        ntptime.NTP_DELTA = 3155644800  # 东八区 UTC+8偏移时间（秒）
        try:
            ntptime.settime()
            print("联网成功...")
        except Exception as e:
            pass
    def show_time(self):
        # 获取真正的时间
        datetime = self.rtc.datetime()
        tft.text(font, str(datetime[0]) + '-' + str(datetime[1]) + '-' + str(datetime[2]) + '' + week[datetime[3]], 0, 0, st7789py.color565(255, 0, 0), st7789py.color565(0, 0, 0))

        # 显示时间需要判断时、分、秒的值否小于 10，如果小于 10，则在显示前面补“0”以
        # 达到较佳的显示效果
        for i in range(4, 7):
            if datetime[i] < 10:
                time_list[i - 4] = "0"
            else:
                time_list[i - 4] = ""
        # 显示时间
        tft.text(font,time_list[0] + str(datetime[4]) + ':' + time_list[1] + str(datetime[5]) + ':' + time_list[2] + str(datetime[6]), 0, 25, st7789py.color565(255, 0, 0), st7789py.color565(0, 0, 0))

# 1. 创建对象
clock = Clock("JC-12", "jc888888")

# 2. 调用显示
while True:
    clock.show_time()
    time.sleep(1)


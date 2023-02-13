import time
from machine import Pin, RTC
import network
import ntptime

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
        date = self.rtc.datetime()
        print(date)
        
# 1. 创建对象
clock = Clock("@PHICOMM_30", "13612423540")

# 2. 调用显示
while True:
    clock.show_time()
    time.sleep(1)



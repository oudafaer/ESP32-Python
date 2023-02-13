from machine import Pin, SoftI2C  #从机器导入GPIO模块和软件I2C模块
import ssd1306                    #导入之前已经上传的ssd1306.py库
from time import sleep

# ESP32 Pin assignment 
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

# ESP8266 Pin assignment
#i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.text_16X16('56789',0,16)
oled.chinese('你好呀',0,0) 
oled.show()


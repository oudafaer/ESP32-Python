import machine
import time
led = machine.Pin(2,machine.Pin.OUT)  #定义led为输出
sw = machine.Pin(0,machine.Pin.IN)    #定义sw为输入

def blink_led_ntimes(num, t_on, t_off, msg):
    counter = 0
    while (counter < num):
        led.on()
        time.sleep(t_on)
        led.off()
        time.sleep(t_off)
        counter += 1
    print (msg)
    
#CPU轮询        
while True:
    if(sw.value() == 0):  #按键按下
        blink_led_ntimes(3, 0.1, 0.2, 'Done.')

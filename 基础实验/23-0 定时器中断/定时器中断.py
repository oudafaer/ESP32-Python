import machine

timer=machine.Timer(0)
led = machine.Pin(2,machine.Pin.OUT)  #定义led为输出
def zhongduan(timer):
    led.value(not led.value())  #led取反
        
        
timer.init(period=1000, mode=machine.Timer.PERIODIC, callback=zhongduan)


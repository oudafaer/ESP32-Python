import machine
led = machine.Pin(2,machine.Pin.OUT)  #定义led为输出
sw = machine.Pin(0,machine.Pin.IN)    #定义sw为输入

def handle_interrupt(pin):        #中断服务函数
    led.value(not led.value())  #led取反
    
#外部中断定义 下降沿触发 并命名中断服务函数
sw.irq(trigger=machine.Pin.IRQ_FALLING, handler=handle_interrupt)

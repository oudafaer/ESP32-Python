import machine

sw1 = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)    #定义sw1为按键输入 内部上拉
sw2 = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)    #定义sw2为按键输入 内部上拉
dr1 = machine.Pin(22, machine.Pin.OUT)               #电机驱动引脚1
dr2 = machine.Pin(23, machine.Pin.OUT)               #电机驱动引脚2

#全局变量
press = False #限位开关（按键）状态
irq_pin = 0   #限位开关（按键）引脚号

def handle_interrupt(pin):        #中断服务函数
    global press
    press = True
    global irq_pin
    irq_pin = int(str(pin)[4:-1]) #获取引脚号

sw1.irq(trigger=machine.Pin.IRQ_FALLING, handler=handle_interrupt) #外部中断定义 下降沿触发 并定义中断服务函数
sw2.irq(trigger=machine.Pin.IRQ_FALLING, handler=handle_interrupt) #外部中断定义 下降沿触发 并定义中断服务函数

while True:
    if press:
        print (irq_pin)
        press = False
        
        if(irq_pin == 15):
            dr1.value(0)
            dr2.value(1)
            print('counter')
        elif(irq_pin == 21):
            dr1.value(1)
            dr2.value(0)
            print('clockwise')
        else:
            pass

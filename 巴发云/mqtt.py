from umqtt.simple import MQTTClient
import time
from machine import Timer

#需要修改的地方
wifiName = "@PHICOMM_30"                   #wifi 名称，不支持5G wifi
wifiPassword = "13612423540"       #wifi 密码
clientID = "4c1492f5aaf0d0810aef872944fdb85a"            # Client ID ，密钥，巴法云控制台获取
myTopic='oudafa'                     # 需要订阅的主题值，巴法MQTT控制台创建

#默认设置
serverIP = "bemfa.com"    # mqtt 服务器地址
port = 9501

# WIFI 连接函数
def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(wifiName, wifiPassword)
        while not sta_if.isconnected():
            pass
    print('connect  WiFi ok')
    

# 接收消息，并处理
def MsgOK(topic, msg):          # 回调函数，用于收到消息
        print((topic, msg))             # 打印主题值和消息值
        if topic == myTopic.encode():     # 判断是不是发给myTopic的消息
            if msg == b"on":                # 当收到on
                print("rec on")
            elif msg == b"off":             #  当收到off
                print("rec off")


#初始化mqtt连接配置
def connect_and_subscribe():
  client = MQTTClient(clientID, serverIP,port)  
  client.set_callback(MsgOK)
  client.connect()
  client.subscribe(myTopic)
  print("Connected to %s" % serverIP)
  return client
  
def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()
  
  

#开始连接WIFI
do_connect() 

#开始连接MQTT
try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()
 

while True:
  try:
    client.check_msg() 
  except OSError as e: #如果出错就重新启动
    print('Failed to connect to MQTT broker. Reconnecting...')
    restart_and_reconnect() 


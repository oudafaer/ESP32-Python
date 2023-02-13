from machine import Pin, SPI
import st7789_itprojects


tft = st7789_itprojects.ST7889_Image(SPI(2, 80000000), dc=Pin(2), cs=Pin(5), rst=Pin(15))
tft.fill(st7789_itprojects.color565(0, 0, 0))  # 背景设置为黑色

'''
# 因为用到了14张图片，所以这里创建14个文件对象
f_list = [open("img{}.dat".format(i), "rb") for i in range(1, 14)]

def show_img():
    while True:
        for f in f_list:  # 遍历14个文件，显示图片
            f.seek(0)
            for row in range(0, 240, 24):
                buffer = f.read(11520)
                tft.show_img(0, row, 239, row+24, buffer)
'''
def show_img():
    with open("text_img.dat", "rb") as f:
        for row in range(240):
            buffer = f.read(480)
            tft.show_img(0, row, 239, row, buffer)


show_img()

from machine import Pin, SPI
import framebuf
import epaper


# 1. 创建对应的引脚
miso = Pin(19)
mosi = Pin(23)
sck = Pin(18)
cs = Pin(33)
dc = Pin(32)
rst = Pin(19)
busy = Pin(35)
spi = SPI(2, baudrate=10000000, polarity=0, phase=0, sck=sck, miso=miso, mosi=mosi)

# 2. 创建墨水屏驱动对象
e = epaper.EPD(spi, cs, dc, rst, busy)
e.init()

# 3. 定义要显示的内容宽度高度
w = 296
h = 128

# 4. 创建需要的对象
buf = bytearray(w * h // 8)  # 296 * 128 // 8 = 4736
fb = framebuf.FrameBuffer(buf, h, w, framebuf.MONO_HLSB)


def show_black_white():
    black = 0
    white = 1
    fb.fill(white)
    # fb.fill(black)
    e.display_frame(buf)


def show_image():
    from image_array import image_array
    # 注意：实际的图片多大这里就写多大，例如实际的图片是118x296，那么就将下面的128改为118
    fbImage = framebuf.FrameBuffer(image_array, 128, 296,  framebuf.MONO_HLSB)
    fb.blit(fbImage, 0, 0)
    e.display_frame(buf)


if __name__ == "__main__":
    # show_black_white()
    show_image()


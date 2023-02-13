from machine import Pin, SPI
import newframebuf
import time
import epaper


def show_text():
    black = 0
    white = 1
    fb.fill(white)
    fb.text('Hello World', 30, 10, black, size=2)
    """
    e.display_frame(buf)
    time.sleep(0.5)
    fb.pixel(30, 10, black)
    e.display_frame(buf)
    time.sleep(0.5)
    fb.hline(30, 30, 10, black)
    e.display_frame(buf)
    time.sleep(0.5)
    fb.vline(30, 50, 10, black)
    fb.line(30, 70, 40, 80, black)
    fb.rect(30, 90, 10, 10, black)
    fb.fill_rect(30, 110, 10, 10, black)
    for row in range(0,36):
        fb.text(str(row), 0, row*8, black)
    fb.text('Line 36', 0, 268, black)
    """
    e.display_frame(buf)


if __name__ == "__main__":
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
    fb = newframebuf.FrameBuffer(buf, h, w, newframebuf.MHMSB)
    fb.rotation = 3  # 调整显示的方向，可以在0/1/2/3之间选择

    # 5. 显示文字
    show_text()


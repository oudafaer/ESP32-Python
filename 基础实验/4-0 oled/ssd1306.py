import framebuf
import font

# register definitions
SET_CONTRAST        = const(0x81)
SET_ENTIRE_ON       = const(0xa4)
SET_NORM_INV        = const(0xa6)
SET_DISP            = const(0xae)
SET_MEM_ADDR        = const(0x20)
SET_COL_ADDR        = const(0x21)
SET_PAGE_ADDR       = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP       = const(0xa0)
SET_MUX_RATIO       = const(0xa8)
SET_COM_OUT_DIR     = const(0xc0)
SET_DISP_OFFSET     = const(0xd3)
SET_COM_PIN_CFG     = const(0xda)
SET_DISP_CLK_DIV    = const(0xd5)
SET_PRECHARGE       = const(0xd9)
SET_VCOM_DESEL      = const(0xdb)
SET_CHARGE_PUMP     = const(0x8d)


class SSD1306:
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        # Note the subclass must initialize self.framebuf to a framebuffer.
        # This is necessary because the underlying data buffer is different
        # between I2C and SPI implementations (I2C needs an extra byte).
        self.poweron()
        self.init_display()

    def init_display(self):
        for cmd in (
            SET_DISP | 0x00, # off
            # address setting
            SET_MEM_ADDR, 0x00, # horizontal
            # resolution and layout
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01, # column addr 127 mapped to SEG0
            SET_MUX_RATIO, self.height - 1,
            SET_COM_OUT_DIR | 0x08, # scan from COM[N] to COM0
            SET_DISP_OFFSET, 0x00,
            SET_COM_PIN_CFG, 0x02 if self.height == 32 else 0x12,
            # timing and driving scheme
            SET_DISP_CLK_DIV, 0x80,
            SET_PRECHARGE, 0x22 if self.external_vcc else 0xf1,
            SET_VCOM_DESEL, 0x30, # 0.83*Vcc
            # display
            SET_CONTRAST, 0xff, # maximum
            SET_ENTIRE_ON, # output follows RAM contents
            SET_NORM_INV, # not inverted
            # charge pump
            SET_CHARGE_PUMP, 0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01): # on
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(SET_DISP | 0x00)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def show(self):
        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_framebuf()

    def fill(self, col):
        self.framebuf.fill(col)

    def pixel(self, x, y, col):
        self.framebuf.pixel(x, y, col)

    def scroll(self, dx, dy):
        self.framebuf.scroll(dx, dy)

    def text(self, string, x, y, col=1):
        self.framebuf.text(string, x, y, col)
    #行列式
    def text_16X16(self,ch_str, x_axis, y_axis): 
       offset_ = 0 
       for k in ch_str: 
           code = 0x00  # 转成16进制编码 
           data_code = k.encode("utf-8")
           code |= data_code[0]
           byte_data = font.fonts[code]
           for y in range(0, 16):
               a_ = bin(byte_data[y]).replace('0b', '')
               while len(a_) < 8:
                   a_ = '0'+ a_
               b_ = bin(byte_data[y+16]).replace('0b', '')
               while len(b_) < 8:
                   b_ = '0'+ b_
               for x in range(0, 8):
                   self.pixel(x_axis + offset_ + x,    y+y_axis, int(a_[x]))   
                   self.pixel(x_axis + offset_ + x +8, y+y_axis, int(b_[x]))   
           offset_ += 16    
    #列行式    
    def chinese(self,str_cn,x,y): #输入中文字符串和xy坐标
        seat = 0 #类似指针，指向汉字的位置。每写完一个字时，seat+16 指向下一个汉字的位置
        for i in str_cn : #每一个中文字符
            code = 0x00
            data_code = i.encode('utf-8') #转换成utf-8的编码
            code |= data_code[0] << 16
            code |= data_code[1] << 8
            code |= data_code[2]
            code_cn = font.font[code] #与font里面的字典值做对应
            for u in range(16): #每个汉字有16列 每一列里面分为上8行和下8行，8行为一页
                a = code_cn[u] #第一列的上8行
                a = bin(a).replace('0b', '') #把a 转换成二进制的8位数 且把字首的'0b'转换为空 例a =27 ，bin后为 0b11011， replac后为 11011 
                while len(a) < 8 :#如果a的长度不够8为则在前面补0
                    a = '0' + a 
                b = code_cn[u+16] #第一列的下8行
                b = bin(b).replace('0b', '') #转换成二进制的8位数 且把字首的'0b'转换为空 例b =27 ，bin后为 0b11011， replac后为 11011
                while len(b) < 8 :#如果长度不够8为则在前面补0
                    b = '0' + b
                    #在这个时候一个汉字的一列分别为 a b 写入屏幕
                for c in range(8):#循环写入个位
                    self.pixel(x+seat+u,y+c,int(a[c]))
                    self.pixel(x+seat+u,y+c+8,int(b[c]))
            seat = seat + 16
    def picture(self,pic=0):
        y = 0
        for i in range(8):
            code = Picture.picture[pic][128*i,128*i+127]
            for u in range(128):
                a = code[u]
                a = bin(a).replace('0b','')
                while len(a) < 8 :
                    a = '0'+a
                for b in range(8):
                    self.pixel(u,b+y,int(a))
            y = y + 8

class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3c, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        # Add an extra byte to the data buffer to hold an I2C data/command byte
        # to use hardware-compatible I2C transactions.  A memoryview of the
        # buffer is used to mask this byte from the framebuffer operations
        # (without a major memory hit as memoryview doesn't copy to a separate
        # buffer).
        self.buffer = bytearray(((height // 8) * width) + 1)
        self.buffer[0] = 0x40  # Set first byte of data buffer to Co=0, D/C=1
        self.framebuf = framebuf.FrameBuffer1(memoryview(self.buffer)[1:], width, height)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80 # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_framebuf(self):
        # Blast out the frame buffer using a single I2C transaction to support
        # hardware I2C interfaces.
        self.i2c.writeto(self.addr, self.buffer)

    def poweron(self):
        pass


class SSD1306_SPI(SSD1306):
    def __init__(self, width, height, spi, dc, res, cs, external_vcc=False):
        self.rate = 10 * 1024 * 1024
        dc.init(dc.OUT, value=0)
        res.init(res.OUT, value=0)
        cs.init(cs.OUT, value=1)
        self.spi = spi
        self.dc = dc
        self.res = res
        self.cs = cs
        self.buffer = bytearray((height // 8) * width)
        self.framebuf = framebuf.FrameBuffer1(self.buffer, width, height)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs.high()
        self.dc.low()
        self.cs.low()
        self.spi.write(bytearray([cmd]))
        self.cs.high()

    def write_framebuf(self):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs.high()
        self.dc.high()
        self.cs.low()
        self.spi.write(self.buffer)
        self.cs.high()

    def poweron(self):
        self.res.high()
        time.sleep_ms(1)
        self.res.low()
        time.sleep_ms(10)
        self.res.high()



import struct
import numpy as np
from PIL import Image  # PIL就是pillow库


def color565(r, g, b):
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3
'''
#打开一组图片转换
def main():
    img = Image.open("text.png")
    print(img.format, img.size, img.mode)
    img_data = np.array(img)  # 240行240列有3个 240x240x3

    with open("text_img.dat", "wb") as f:
        for line in img_data:
            for dot in line:
                f.write(struct.pack("H", color565(*dot))[::-1])

'''
#多组图片转换
def main():
    for i in range(1,14):
        img = Image.open("./images/img{}.jpg".format(i))
        print(img.format, img.size, img.mode)
        img_data = np.array(img)  # 240行240列有3个 240x240x3

        with open("./images/img{}.dat".format(i), "wb") as f:
            for line in img_data:
                for dot in line:
                    f.write(struct.pack("H", color565(dot[0],dot[1],dot[2]))[::-1])


if __name__ == '__main__':
    main()

# -*- coding: gbk -*-
import os
import datetime as dt
import time
import pandas as pd
import numpy as np
import datetime as dt
import shutil


from PIL import ImageGrab
# import pytesserocr
from PIL import Image
import pytesseract
import time


# 范围要上下左右各富裕一些，不然识别不出来
bbox = (704.5, 963.5, 772, 997)
im = ImageGrab.grab(bbox)


im.save('D:\code\zy.jpg')
time.sleep(3)

image=Image.open('D://code/zy.jpg')
#
# image = image.convert('L')
# threshold = 170
# table = []
# for i in range(256):
#     if i < threshold:
#         table.append(0)
#     else:
#         table.append(1)
# image = image.point(table,'1')
# image.show()
#
# result = pytesseract.image_to_string(image)
# print(result)

#
print (image)
print (pytesseract.image_to_string(image))
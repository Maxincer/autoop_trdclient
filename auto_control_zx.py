#! /usr/bin/env python
# encoding: utf-8
'''
@author: zxl
@file: QMacro.py
@time: 2020/3/10 10:54
'''

import os
import stat
import zipfile
import time
from PIL import ImageGrab
from PIL import Image
import pytesseract
from pymouse import PyMouse          # 引入鼠标监控器
from pykeyboard import PyKeyboard    # 引入键盘监控器


# 按键精灵自动化版本
class QMACRO:
    def __init__(self):
        self.path_file = r'C:\Users\dingqi\Desktop\data备份'
        self.m = PyMouse()
        self.k = PyKeyboard()
        self.x_len = 14
        self.y_len = 19

    """
    return:
    m.click(x,y,button,n)   –鼠标点击
    x,y                     –是坐标位置
    buttong                 –1表示左键，2表示点击右键
    n                       –点击次数，默认是1次，2表示双击
    m.move(x,y)             –鼠标移动到坐标(x,y)
    x_dim, y_dim = m.screen_size()  –获得屏幕尺寸
    """
    def control_mouse_size(self):
        self.x_dim,self.y_dim = self.m.screen_size()
        print('[+] 整体屏幕大小为：(%s,%s)' % (self.x_dim,self.y_dim))

    def control_mouse(self,x,y,y_n_click,error_x = -10,error_y = -10,buttong=1,n=1):
        # x,y 为以桌面图标为单位，几个单位的坐标
        xx = int(self.x_dim / self.x_len * x) + error_x
        yy = int(self.y_dim / self.y_len * y) + error_y
        self.m.move(xx,yy)
        if y_n_click in ['y','Y','Yes','YES']:
            self.m.click(xx,yy,buttong,n)

    """
    k.type_string(‘Hello, World!’)      –模拟键盘输入字符串
    k.press_key(‘H’)                    –模拟键盘按H键
    k.release_key(‘H’)                  –模拟键盘松开H键
    k.tap_key(“H”)                      –模拟点击H键
    k.tap_key(‘H’,n=2,interval=5)       –模拟点击H键，2次，每次间隔5秒
    k.tap_key(k.function_keys[5])         –点击功能键F5
    k.tap_key(k.numpad_keys[5],3)         –点击小键盘5,3次

    联合按键模拟
    例如同时按alt+tab键盘
    k.press_key(k.alt_key)          –按住alt键
    k.tap_key(k.tab_key)            –点击tab键
    k.release_key(k.alt_key)        –松开alt键
    :return:
    """
    # string 必须为字符串
    def keyboard_input(self,string):
        self.k.type_string(string)

    # 模拟键盘按某字母键
    def keyboard_press(self,string):
        self.k.press_key(string)

    # 模拟键盘松开某字幕键
    def keyboard_release(self,string):
        self.k.release_key(string)

    # 模拟键盘点击某字母键，几次， 每次间隔几秒
    def keyboard_tap(self,string,n=1,interval=1):
        self.k.tap_key(string,n,interval)

    # 点击功能键 如：F5
    def keyboard_tap_function(self,num):
        self.k.tap_key(self.k.function_keys[num])

    # 点击小键盘数字键 及 几次
    def keyboard_tap_numpad(self,num,times):
        self.k.tap_key(self.k.numpad_key[num],times)

    # 联合按键模拟
    """
    如同时按 alt + tab 键盘
    k.press_key(k.alt_key)   - 按住alt 键
    k.tap_key(k.tab_key)     - 按住tab 键
    k.release_key(k.alt_key) - 松开alt 键
    """

    def keyboard_double_press(self,key_1,key_2):
        self.k.press_key(eval('self.k.%s_key' % key_1))
        if len(key_2) != 1:
            self.k.tap_key(eval('self.k.%s_key' % key_2))
        else:
            self.k.tap_key(key_2)
        self.k.release_key(eval('self.k.%s_key' % key_1))

    # 压缩文件包
    def zip_file(self):
        zip_name = self.path_file + '.zip'
        z = zipfile.ZipFile(zip_name,'w',zipfile.ZIP_DEFLATED)
        for dirpath,dirnames,filenames in os.walk(self.path_file):
            fpath = dirpath.replace(self.path_file,"")
            fpath = fpath and fpath + os.sep or ""
            for filename in filenames:
                z.write(os.path.join(dirpath,filename),fpath+filename)
            print(fpath.replace('\\','') + " success to zip!!!")
        z.close()

if __name__ == '__main__':
    xx = QMACRO()
    xx.control_mouse_size()
    # 如果有对应压缩包，应该先删除！！！
    start_num = 0
    prod_id_dict = {'601hao':['106700272833','125127']}
    for key in list(prod_id_dict.keys())[start_num:]:
        time.sleep(3)
        # errorx 为正数是往右，errory为正是往下
        xx.control_mouse(x=13,y=9,y_n_click='Y',error_x = -22,error_y = 20,buttong=1,n=2)    # 点击 相应软件图标
        time.sleep(4)
        xx.control_mouse(x=6, y=9,y_n_click='Y',error_x = 15,error_y = 15, buttong=1, n=1)     # 输入账号按钮
        time.sleep(0.5)
        xx.keyboard_double_press('control','a')   # Ctrl + A
        time.sleep(0.5)
        xx.keyboard_input(prod_id_dict[key][0])
        xx.control_mouse(x=6, y=9, y_n_click='Y', error_x=15, error_y=40, buttong=1, n=1)  # 输入密码按钮
        time.sleep(0.5)
        xx.keyboard_double_press('control', 'a')  # Ctrl + A
        time.sleep(0.5)
        xx.keyboard_input(prod_id_dict[key][1])
        time.sleep(0.5)
        # xx.control_mouse(x=6, y=9, y_n_click='Y', error_x=0, error_y=42, buttong=1, n=1)  # 输入第二个密码
        # time.sleep(0.5)
        # xx.keyboard_double_press('control', 'a')  # Ctrl + A
        # time.sleep(0.5)
        # xx.keyboard_input(prod_id_dict[key][2])
        # time.sleep(0.5)


        xx.control_mouse(x=6, y=9, y_n_click='Y', error_x=113, error_y=68, buttong=1, n=1)  # 输入验证码
        bbox = (704.5, 964, 770, 995)
        im = ImageGrab.grab(bbox)
        im.save('D:\code\zy.jpg')
        time.sleep(2)
        imageObject = Image.open('D:\code\zy.jpg')
        imageObject = imageObject.convert("L")
        imageObject_two = imageObject.point(lambda x: 255 if x > 190 else 0)
        YZM = pytesseract.image_to_string(imageObject_two)
        YZM = YZM.replace('.','')
        print (YZM)
        xx.keyboard_input(YZM)
        time.sleep(0.5)
        xx.control_mouse(x=6, y=9, y_n_click='Y', error_x=15, error_y=95, buttong=1, n=1)  # 点击链接按钮
        time.sleep(3)
        xx.control_mouse(x=3, y=8, y_n_click='Y', error_x=-5, error_y=45, buttong=1, n=1)  # 点击资金股份
        time.sleep(2.5)
        xx.control_mouse(x=13, y=9, y_n_click='Y', error_x=-85, error_y=-95, buttong=1, n=1)  # 点击输出
        time.sleep(2)
        xx.control_mouse(x=8, y=4, y_n_click='Y', error_x=20, error_y=20, buttong=2, n=1)  # 点击右键按钮
        time.sleep(2)
        xx.control_mouse(x=9, y=5, y_n_click='Y', error_x=20, error_y=0, buttong=1, n=1)  # 点击输出按钮
        time.sleep(2)
        xx.control_mouse(x=11, y=5, y_n_click='Y', error_x=45, error_y=30, buttong=1, n=1)  # 点击输出到Excel表格
        time.sleep(2)
        xx.control_mouse(x=13, y=5, y_n_click='Y', error_x=45, error_y=30, buttong=1, n=1)  # 点击确认输出按钮
        time.sleep(2)
        xx.control_mouse(x=13, y=4, y_n_click='Y', error_x=15, error_y=20, buttong=1, n=2)  # 点击选择文件夹
        time.sleep(3)
        xx.keyboard_input(key)                                                              # 输入对应文件夹名称
        time.sleep(2)
        xx.control_mouse(x=12, y=5, y_n_click='Y', error_x=15, error_y=-20, buttong=1, n=2)  # 点击确认要替换文件按钮
        time.sleep(3)
        xx.control_mouse(x=13, y=5, y_n_click='Y', error_x=20, error_y=20, buttong=1, n=2)  # 点击确认输出按钮
        time.sleep(2)
        xx.control_mouse(x=14, y=6, y_n_click='Y', error_x=20, error_y=30, buttong=1, n=2)  # 点击
        time.sleep(2)
        xx.control_mouse(x=11, y=5, y_n_click='Y', error_x=20, error_y=30, buttong=1, n=2)  # 点击浏览
        time.sleep(2)
        xx.control_mouse(x=14, y=7, y_n_click='Y', error_x=-20, error_y=50, buttong=1, n=1)  # 点击浏览
        time.sleep(2)
        xx.control_mouse(x=19, y=1, y_n_click='Y', error_x=40, error_y=80, buttong=1, n=1)  # 点击浏览
        time.sleep(2)
        xx.control_mouse(x=20, y=2, y_n_click='Y', error_x=60, error_y=80, buttong=1, n=1)  # 点击浏览
        time.sleep(2)
        xx.control_mouse(x=12, y=5, y_n_click='Y', error_x=20, error_y=50, buttong=1, n=1)  # 点击浏览
        time.sleep(2)
        xx.control_mouse(x=24, y=0, y_n_click='Y', error_x=80, error_y=10, buttong=1, n=1)  # 点击浏览
        time.sleep(2)
        xx.control_mouse(x=10, y=5, y_n_click='Y', error_x=80, error_y=50, buttong=1, n=1)  # 点击浏览
        time.sleep(2)
        xx.control_mouse(x=13, y=5, y_n_click='Y', error_x=40, error_y=50, buttong=1, n=1)  # 点击浏览
        time.sleep(2)


# coding: utf-8
# version: python3.9
# Author: Maxincer
# CreateTime: 20211216T210000

"""
自动登录招商通达信-智远一户通
测试账号:  0978368090/456123
Assumption: 只打开一个客户端
"""
import time
import win32api
import win32con
import win32gui

from pymouse import PyMouse
from pykeyboard import PyKeyboard


app_title = '招商智远一户通'
app_path = r'C:\programfiles\trading_client\zhaos_zyyht\TdxW.exe'

ncard_id = '0978368090'
password = '456123'

class_login_window = '#32770'
caption_login_window = u'招商证券V7.15'

class_msg_window = None
caption_msg_window = 'Chrome Legacy Window'

def get_hwnd_opened_checked(class_, caption_):
    hwnd = 0
    i = 0
    while not hwnd:
        if i <= 20:
            hwnd = win32gui.FindWindow(class_, caption_)
            time.sleep(0.1)
        else:
            raise RuntimeError('start TdxW.exe while waiting too long, please check.')
    return hwnd


hwnd = win32gui.FindWindow(class_login_window, caption_login_window)
if hwnd:
    pass
else:
    win32api.ShellExecute(0, 'open', app_path, '', '', 1)  # 非阻塞方式打开软件
    print('opened command entered.')
    hwnd = get_hwnd_opened_checked(class_login_window, caption_login_window)
    # 等待启动后，置顶
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.SetForegroundWindow(hwnd)




# 打开一个客户端后
dict_coordinates = {'ncard_id': (750, 485), 'password': (750, 530), 'login': (750, 600)}


m = PyMouse()
k = PyKeyboard()

m.click(dict_coordinates['ncard_id'][0], dict_coordinates['ncard_id'][1])
time.sleep(1)
k.press_key(k.control_key)
k.tap_key('a')
k.release_key(k.control_key)
k.tap_key(k.delete_key)
k.type_string(ncard_id)

m.click(dict_coordinates['password'][0], dict_coordinates['password'][1])
time.sleep(1)
k.type_string(password)

m.click(dict_coordinates['login'][0], dict_coordinates['login'][1])
time.sleep(2)

# 进入客户端, 找到句柄
# hwnd = win32gui.FindWindow(None, 'Chrome Legacy Window')
# win32gui.CloseWindow(hwnd)

# win32gui.PostMessage(00080A70, win32con.WM_CLOSE, 0, 0)
print('done')




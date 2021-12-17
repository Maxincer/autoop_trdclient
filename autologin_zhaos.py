# coding: utf-8
# version: python3.9
# Author: Maxincer
# CreateTime: 20211216T210000

"""
自动登录招商通达信-智远一户通
测试账号:  0978368090/456123
"""
app_title='招商智远一户通'
app_path=r'C:\zhaos_zyyht\TdxW.exe'

account_id='0978368090'
password='456123'

import datetime
import re

import win32gui # Win 图形界面接口，主要负责操作窗口切换以及窗口中元素

import win32api # Win 开发接口模块，主要负责模拟键盘和鼠标操作

import win32con # 全面的库函数，提供Win32gui和Win32api需要的操作参数

from pywinauto import application

from pywinauto.keyboard import send_keys

import pywinauto.mouse

from pymouse import PyMouse

from pykeyboard import PyKeyboard

m = PyMouse()
k = PyKeyboard()

# 定义窗口检测函数
def find_win(title):
    ws=0
    for i in range(10):
        try:
            h=pywinauto.findwindows.find_window(title_re=title,found_index=0)
            ws=1
            break
        except:
            ws=0
    return ws

# 控件函数
def find_ocr(ocr_title, ocr_id, ocr_type, handle, index, method, note):
    lxy=(0,0,0,0)
    app_s1=0
    ocr_s1=0
    ocr_win=0
    ocr_state=''
    error_code='ok'
    # 检测app连接
    try:
        h1 = pywinauto.findwindows.find_window(title_re=app_title,found_index=0)
        app_s1=1
    except:
        error_code='Error(app)'
    # 检测ocr_win连接
    if app_s1==1:
        try:
            app=application.Application(backend='uia').connect(handle=h1)
            app.window(handle=h1).set_focus()
            if method=='printall':
                app.window(handle=h1).print_control_identifiers()
                ocr_win=app.window(handle=h1).child_window(title_re=ocr_title,auto_id=ocr_id,control_type=ocr_type,handle=handle,found_index=index)
                if ocr_win.exists()==True:
                    lstr=str(ocr_win.rectangle())
                    lstr_xy=re.findall("\d+",lstr)
                    lxy=(int(lstr_xy[0]),int(lstr_xy[1]),int(lstr_xy[2]),int(lstr_xy[3]))
                    ocr_s1=1
        except:
            error_code='Error(ocr)'

    # 响应事件
    if app_s1==1 and ocr_s1==1:
        try:
        if len(str(method))>0:

        if method=='click':

        if note=='auto':

        ocr_win.click()

        else:

        ocr_win.click_input()

    elif method=='focus':

    ocr_win.set_focus()

    elif method=='print':

    ocr_win.print_control_identifiers()

    elif method=='press':

    ocr_win.click_input()

    k.press_keys(str(note))

    elif method=='set':

    ocr_win.set_text(str(note))

    elif method=='send':

    ocr_win.click_input()

    send_keys(str(note))

    elif method=='move':

    m.move(int((lxy[0]+lxy[2])/2),int((lxy[1]+lxy[3])/2))

    elif method=='enabled':

    ocr_state=ocr_win.is_enabled()

    elif method=='get':

    ocr_state=ocr_win.get_properties()

    elif method=='texts':

    ocr_state=ocr_win.texts()

    except:

    error_code='Method Error'

    # 返回结果

    return app_s1,ocr_s1,ocr_win,ocr_state,error_code,lxy

def login(id, password, login_mode, trade_type):
    # (1) 行情
    if login_mode==2:
        login2 = find_ocr('','365','Pane',None,0,'focus','manul')
    # 按钮存在，点击进入
    if login2[1]==1:
        find_ocr('','365','Pane',None,0,'click','manul')
    # 按钮不存在
    elif login2[1]==0:
        # 如果 App 已经启动，不用再登录
        if login2[0]==1:
            return
        else:
            app = application.Application(backend='uia').start(app_path)
            app.top_window().set_focus()
            find_ocr('','365','Pane',None,0,'click','manul')
            return
    # (2) 独立交易
    if login_mode==3:
        login3=find_ocr('','366','Pane',None,0,'focus','manul')
        # 按钮存在，点击准备登录
        if login3[1]==1:
            find_ocr('','366','Pane',None,0,'click','manul')
        # 按钮不存在
        elif login3[1]==0:
        # 如果 App 已经启动，先退出再登录
            if login3[0]==1:
                app_exit()
                app=application.Application(backend='uia').start(app_path)
                app.top_window().set_focus()
                find_ocr('','366','Pane',None,0,'click','manul')
                select(trade_type)
    # (3) 行情 + 交易
    if login_mode==1:
        # 检验“登录模式”和“交易类型”控件
        login1=find_ocr('','364','Pane',None,0,'focus','manul')
        # 如果App未启动，先启动
        if login1[0]==0:
            app=application.Application(backend='uia').start(app_path)
            app.top_window().set_focus()
            # 点击登录页面
            find_ocr('','364','Pane',None,0,'click','manul')
            # 测试模式选择按钮
            seltype = select(trade_type)
            # 如果 App 已启动，但不存在登录界面，说明是热启动
            if seltype[0]==1 and seltype[1]==0:
                for i in range(5):
                # 如果交易已登录，且未锁定，无需登录，直接跳出
                    lock_ocr=find_ocr('锁定','','',None,0,'','auto')
                    if lock_ocr[1]==1:
                        return
                    # 如果交易锁定，直接解锁
                    find_ocr('交易密码','1130','Text',None,0,'focus','manul')
                    unlock_ocr=find_ocr('交易密码','1130','Text',None,0,'press',str(password))

                    if unlock_ocr[1]==1:
                        find_ocr('确定','442','Button',None,0,'click','auto')
                        return
                        # 如果交易隐藏，调出界面
                    if lock_ocr[1]==0 and unlock_ocr[1]==0:
                        # 隐藏弹窗
                        hide_ocr(0,None,'即时播报')
                        # 激活 K 线界面，调出（交易/登录/解锁）界面
                        find_ocr('','59648','Pane',None,0,'send','.8{VK_RETURN}')

            # 如果调出的是登录界面，则跳出循环准备登录
            seltype=select(trade_type)
            if seltype[1]==1:
                break
            find_ocr('','234','Pane',None,0,'press',str(password))
    # 后输入客户号
    find_ocr('','1001','Edit',None,0,'set',str(id))



# 控件(隐藏/显示)函数

def hide_ocr(mode,handle,title):

# 句柄优先，无句柄再找标题

if handle!=None:

handle=handle

else:

handle=win32gui.FindWindow(None,title)

# 进行隐藏/显示操作

if mode==0:

win32gui.PostMessage(handle,win32con.WM_CLOSE,0,0)

win32gui.ShowWindow(handle,win32con.WM_DESTROY)

elif mode==1:

win32gui.ShowWindow(handle,win32con.SW_SHOWNORMAL)

else:

return handle

# 关闭弹窗('今日不再提示'\'无此操作方式')
def close_note():

# 登录时可能的弹窗

s1=find_ocr('今日不再提示','508','CheckBox',None,0,'click','auto')

if s1[1]==1:

find_ocr('关闭','509','Button',None,0,'click','auto')

# 盘中可能的弹窗

s2=find_ocr('今日不再提示','1914','CheckBox',None,0,'click','auto')

if s2[1]==1:

find_ocr('关闭','2','Button',None,0,'click','auto')

# 盘中可能的弹窗

s3=('','1474','Edit',None,0,'','')

if s3[1]==1:

find_ocr('关闭','2','Button',None,0,'click','auto')

# 锁定交易

def lock_trade():

# 如果处于锁定界面

find_ocr('取消','443','Button',None,0,'click','auto')

# 如果处于交易界面

find_ocr('锁定','','',None,0,'click','auto')

# 退出app

def app_exit():

find_ocr('','9601','Pane',None,0,'click','manul')

find_ocr('退出','961','Button',None,0,'click','auto')

# 如果提示下载盘后日线数据

note=find_ocr('提示','','Pane',None,0,'','auto')

if note[1]==1:

find_ocr('确定','1','Button',None,0,'click','auto')

time.sleep(1)

# 定义登录函数

# ==============================================================

def select(trade_type):

z=(0,0,0)

if trade_type==1:

z=find_ocr('普通交易','2264','RadioButton',None,0,'click','auto')

elif trade_type==2:

z=find_ocr('信用交易','2265','RadioButton',None,0,'click','auto')

return z


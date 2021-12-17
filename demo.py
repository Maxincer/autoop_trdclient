# TDX_交易机器人（Python程序自动化）<2020.12.19开发> Update:2021.1.2

# ===================================================================

for TDX v2.8.1

# 开关

run_on_off = 1

# =================================================

app_title='中国银河证券海王星V2*'

app_path=r'C:\中国银河证券海王星\TdxW.exe'

# 账号/密码

#----------------

id='1025*******8'

password='******'

#----------------

# 工作时段( 0-不限制；1-限制 )

#-----------------------------

time_work = 1

time_start=80500

time_end =150200

#

# 下单时段( 0-不限制；1-限制 )

#-----------------------------

time_trade = 1

time1= 93000

time2=245700

#-----------------------------

#

# 下单方式(0-测试单；1-任意时间；2-固定时间；3-尾盘时间；4-最优时间)

#--------------------------------------------------------------------

Trade_mode = 1

#--------------------------------------------------------------------

# 短线交易开关

Short_mode = 1

#



# 配置和安装方法

# ======================================================================================

# 特别重要提示：新包安装后，请重新进入python才起作用。

#

# 1.定时器

# pip3 install schedule

# d:\python37\python.exe -m pip install --upgrade pip

# path d:\python37\scripts

#

# 2.Python自动化模块

# pip3 install pywinauto

# pip3 install pywin32 如果报错，采用下述方式：pip3 install pypiwin32

# （win32api，win32gui，win32con）

# pip3 install pymouse

# pip3 install pyUserInput

# 3.图像处理

# pip3 install PILLOW

# 图片处理

# pip3 install opencv-python

# 4.OCR 光学文字识别软件

# ======================================================================================

# pip3 install pytesseract

# pip3 install tesseract

# 下载安装 Tesseract-OCR 软件并设好路径：

# -----------------------------------------------------------------------------------

# Index of /tesseract

# 最新: tesseract-ocr-w64-setup-v5.0.0-alpha.20201127.exe

# CMD 中设置路径:path C:\Program Files\Tesseract-OCR

# 路径修改：python37\Lib\site-packages\pytesseract\pytesseract.py

# 改为: tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# -----------------------------------------------------------------------------------

# tesseract --list-langs 查看语言包

# 默认英文，中文语言包需要放到 C:\Program Files\Tesseract-OCR\tessdata

# tesseract --help-psm 查看psm 参数设置方法

# 参数设置：config='-l chi_sim --psm 7 -c tessedit_char_whitelist=0123456789'

# ======================================================================================

#

# 基础知识介绍

# ==========================================================================

# 数据分析: pandas, numpy

# 文本处理: re

# 爬虫: requests, pyQuery, Selenium, BeautifulSoup, Scrapy, pyspider, cola

# 网页应用: Django, flask, grab

# 办公自动化: 可以编辑excel的xlrd, openpyxl和编辑world的docx

# 金融: mplfinance,talib

# ==========================================================================

#



# 模块导入

# ---------------------------------

# 导入时间

import time

import datetime

# OS和Win32

import os

import win32gui # Win 图形界面接口，主要负责操作窗口切换以及窗口中元素

import win32api # Win 开发接口模块，主要负责模拟键盘和鼠标操作

import win32con # 全面的库函数，提供Win32gui和Win32api需要的操作参数

import win32ui

# 自动化

from pywinauto import application

from pywinauto.keyboard import send_keys

import pywinauto.mouse

# 键盘鼠标

from pymouse import PyMouse

from pykeyboard import PyKeyboard

# 定义键鼠

m = PyMouse()

k = PyKeyboard()

# 正则函数

import re

# OCR光学文字识别

import pytesseract

# 屏幕抓图

from PIL import Image,ImageGrab

# ---------------------------------

# 时间函数

def tm():

time_now = datetime.datetime.now()

hour = time_now.hour

minute = time_now.minute

second = time_now.second

timex=10000*hour+100*minute+second

# tm_format='%Y-%m-%d %H:%M:%S'

times=time_now.strftime('%H:%M:%S')

return time_now,hour,minute,second,timex,times



# 时间差

def d_tm(time_start):

time_end=datetime.datetime.now()

delta_ts=(time_end-time_start).seconds

delta_tm=int((time_end-time_start).seconds/60)

return delta_ts,delta_tm



# 图像识别

def scan_image(left,top,right,bottom,check_code,check_len,method,limit):

z=''

lenz=0

codez='0'

# 抓取屏幕图片

img = ImageGrab.grab(bbox=(left,top,right,bottom))

# 灰度转换

if check_code=='gray':

img = img.convert('L')

# 二值转换

if check_code=='binary':

img = img.convert('L')

threshold = 200

table = []

for i in range(256):

if i < threshold:

table.append(0)

else:

table.append(1)

img = img.point(table, '1')

# 测试图片

if method=='save':

img.save('test.png')

# 识别文本

if limit=='num':

# 仅限数字

z = pytesseract.image_to_string(img,config='--psm 7 -c tessedit_char_whitelist=0123456789').replace(' ','')

elif limit=='eng':

# 仅限字母和数字

z = pytesseract.image_to_string(img,config='--psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz').replace(' ','')

elif limit=='chi':

# 中文语言包

z = pytesseract.image_to_string(img,config='-l chi_sim --psm 7').replace(' ','')

else:

# 无限制

z = pytesseract.image_to_string(img,config='--psm 7').replace(' ','')

# 删除最后两位特殊字符

z = z[:-2]

# 生成扫描文本的长度和末位字符

if len(z)>0:

lenz=len(z)

codez=z[-1]

# 校验(未通过长度或末位字符校验，则初始化为'0')

if method=='check' and (check_len>0 or check_code!=''):

if check_len>0 and lenz==check_len and check_code=='':

pass

elif check_len==0 and check_code!='' and codez==check_code:

pass

elif check_len>0 and lenz==check_len and check_code!='' and codez==check_code:

pass

else:

j=1

z=''

if check_len>0:

j=check_len

elif lenz>0:

j=lenz

z=z.zfill(j)

# 返回值

return z



# 信标机扫描

def Scanner(left,top,right,bottom):

z = scan_image(left,top,right,bottom,'9',15,'check','num')

if z[14]!='9':

z=('扫','描','遮','盖','','','0','','0','0','0','','0','0','0')

stk_code=z[0]+z[1]+z[2]+z[3]+z[4]+z[5]

tradel=z[6]

tradeln=z[7]+z[8]+z[9]

trades=z[10]

tradesn=z[11]+z[12]+z[13]

check=z[14]

return (stk_code,tradel,tradeln,trades,tradesn,check)



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

def find_ocr(ocr_title,ocr_id,ocr_type,handle,index,method,note):

lxy=(0,0,0,0)

app_s1=0

ocr_s1=0

ocr_win=0

ocr_state=''

error_code='ok'

# 检测app连接

try:

h1=pywinauto.findwindows.find_window(title_re=app_title,found_index=0)

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

ocr_win=ocr_win=app.window(handle=h1).child_window(title_re=ocr_title,auto_id=ocr_id,control_type=ocr_type,handle=handle,found_index=index)

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

# 向通达信广播股票代码

def BroadCast(Message,Code):

if str(Message)=='Stock':

if str(Code)[0]=='6':

codex='7'+str(Code)

else:

codex='6'+str(Code)

else:

codex=int(Code)

UWM_STOCK = win32api.RegisterWindowMessage('Stock')

win32gui.PostMessage(win32con.HWND_BROADCAST,UWM_STOCK,int(codex),0)



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

def login(id,password,login_mode,trade_type):

# (1) 行情

if login_mode==2:

login2=find_ocr('','365','Pane',None,0,'focus','manul')

# 按钮存在，点击进入

if login2[1]==1:

find_ocr('','365','Pane',None,0,'click','manul')

# 按钮不存在

elif login2[1]==0:

# 如果 App 已经启动，不用再登录

if login2[0]==1:

return

else:

app=application.Application(backend='uia').start(app_path)

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

seltype=select(trade_type)

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

# 账号登录

#------------------------------

# 先输入密码

find_ocr('','234','Pane',None,0,'press',str(password))

# 后输入客户号

find_ocr('','1001','Edit',None,0,'set',str(id))

# 验证码识别

#------------------------------

# 安全框坐标

safe_win=find_ocr('主站测速','1896','ComboBox',None,0,'','auto')

# 验证码坐标

check_win=find_ocr('','235','Pane',None,0,'','manul')

x1=int(check_win[5][2]+1.5*(check_win[5][0]-safe_win[5][2]))

y1=check_win[5][1]

x2=int(check_win[5][2]+0.38*(check_win[5][2]-safe_win[5][0]))

y2=check_win[5][3]

# 尝试登录(不超过 20 次尝试...)

for j in range(1,20):

#-------------------------------------------------------------------

# 间隔时间，控制控件检测速度

time.sleep(0.1)

# 检验验证码输入框是否可用

check_ocr=find_ocr('','235','Pane',None,0,'enabled','auto')

# 如果可用，输入验证码登录

if check_ocr[3]==True and check_ocr[4]=='ok':

# 提取图片验证码

z=scan_image(x1,y1,x2,y2,'',4,'check','num')

# 输入验证码

check_ocr=find_ocr('','235','Pane',None,0,'press',str(z))

# 点击登录

find_ocr('','1','Pane',None,0,'click','manul')

time.sleep(0.1)

else:

break

#-------------------------------------------------------------------

# 关闭弹窗

close_note()



# 快速交易

# ==============================================================

def fast_trade(order,sk_code,num,ratio,on_off):

# 登录交易

login(id,password,1,1)

# 循环至快速交易界面

for j in range(5):

# 隐藏弹窗

hide_ocr(0,None,'即时播报')

# 向通达信广播股票代码消息

BroadCast('Stock',sk_code)

# 快速买入

if order==1 or order==2 or order==3 or order==4:

# 激活 K 线界面，调出(闪电买入)界面

find_ocr('','59648','Pane',None,0,'send','21{VK_RETURN}')

time.sleep(0.3)

# 检测买入界面控件

# ----------------------------------------------------------------------

if ratio==0:

fast_win=find_ocr('买入数量','12007','Edit',None,0,'set',str(num))

elif ratio==1:

fast_win=find_ocr('全部','1495','Button',None,0,'click','auto')

elif ratio==2:

fast_win=find_ocr('1/2','8909','RadioButton',None,0,'click','auto')

elif ratio==3:

fast_win=find_ocr('1/3','8910','RadioButton',None,0,'click','auto')

elif ratio==4:

fast_win=find_ocr('1/4','8911','RadioButton',None,0,'click','auto')

elif ratio==5:

fast_win=find_ocr('1/5','8913','RadioButton',None,0,'click','auto')

# ----------------------------------------------------------------------

# 快速卖出

elif order==5 or order==6 or order==7 or order==8:

# 激活 K 线界面，调出(闪电卖出)界面

find_ocr('','59648','Pane',None,0,'send','23{VK_RETURN}')

time.sleep(0.3)

# 检测卖出界面控件

# ----------------------------------------------------------------------

if ratio==0:

fast_win=find_ocr('卖出数量','12007','Edit',None,0,'set',str(num))

elif ratio==1:

fast_win=find_ocr('全部','1495','Button',None,0,'click','auto')

elif ratio==2:

fast_win=find_ocr('1/2','8903','RadioButton',None,0,'click','auto')

elif ratio==3:

fast_win=find_ocr('1/3','8905','RadioButton',None,0,'click','auto')

elif ratio==4:

fast_win=find_ocr('1/4','8907','RadioButton',None,0,'click','auto')

elif ratio==5:

fast_win=find_ocr('1/5','8913','RadioButton',None,0,'click','auto')

# ----------------------------------------------------------------------

# 检测到控件动作,跳出

if fast_win[1]==1:

break

# ------------------------

# 买单确认

if order==1 or order==2 or order==3 or order==4:

#-----------------------------------------------------------

find_ocr('买 入','1','Button',None,0,'click','auto')

# 数量有效性

#------------------------------------------------------------

note=find_ocr('提示','','Pane',None,0,'','auto')

if note[1]==1:

find_ocr('确认','7015','Button',None,0,'click','auto')

# 交易界面取消

find_ocr('取 消','2','Button',None,0,'click','auto')

#------------------------------------------------------------

# 交易开关

if on_off=='on':

# 买入确认

find_ocr('买入确认','7015','Button',None,0,'click','auto')

# 提示（成交结果）

note=find_ocr('提示','','Pane',None,0,'','auto')

if note[1]==1:

find_ocr('确认','7015','Button',None,0,'click','auto')

elif on_off=='off':

off=find_ocr('取消','7016','Button',None,0,'click','auto')

if off[1]==1:

# 交易界面取消

find_ocr('取 消','2','Button',None,0,'click','auto')

#-----------------------------------------------------------

# 卖单确认

elif order==5 or order==6 or order==7 or order==8:

#-----------------------------------------------------------

find_ocr('卖 出','1','Button',None,0,'click','auto')

# 数量有效性

#-----------------------------------------------------------

note=find_ocr('提示','','Pane',None,0,'','auto')

if note[1]==1:

find_ocr('确认','7015','Button',None,0,'click','auto')

# 交易界面取消

find_ocr('取 消','2','Button',None,0,'click','auto')

#-----------------------------------------------------------

# 交易开关

if on_off=='on':

# 卖出确认

find_ocr('卖出确认','7015','Button',None,0,'click','auto')

# 提示（成交结果）

note=find_ocr('提示','','Pane',None,0,'','auto')

if note[1]==1:

find_ocr('确认','7015','Button',None,0,'click','auto')

elif on_off=='off':

off=find_ocr('取消','7016','Button',None,0,'click','auto')

if off[1]==1:

# 交易界面取消

find_ocr('取 消','2','Button',None,0,'click','auto')

#-----------------------------------------------------------

#

# 查看持仓

find_ocr('持仓','','Button',None,0,'click','auto')

# 锁定交易

lock_trade()



# 欢迎函数

def welcome():

print('')

print('')

print(' # -----------------------------------------------------------------')

print('')

print(' TDX_交易机器人( Ver.2021.1.1 ) 启动！')

print('')

print(' TDX_机器人实盘，将在每天: ',time_end,' 退出！')

print('')

print(' 为方便观测，本窗口将保持开启！关闭本窗口将退出机器人看盘！ ')

print('')

print(' # -----------------------------------------------------------------')

print('')

print(' 交易时点（ 09:50, 11:00, 13:15, 14:50 ）,短线（09:30-15:00） ')

print('')

print('')

print(' 启动中 ... ')

print('')

print('')

print('')

print('')



# 分单计算器

def calc(total,r1,r2,r3,r4):

x1=total*r1

x2=(total-x1)*r2

x3=(total-x1-x2)*r3

x4=(total-x1-x2-x3)*r4

x=x1+x2+x3+x4

return int(x),int(x1),int(x2),int(x3),int(x4)



# ====================

# 主程序

# ====================

#

if run_on_off==1:

welcome()

login(id,password,1,1)

time.sleep(3)

#--------------



#--------------

wx_init=0

tm_init=tm()[0]

#--------------

t1=0

t2=0

t3=0

t4=0

buycount=0

selcount=0

#--------------

while (run_on_off==1):

# 接入 app

# -----------------------------------

wx=find_win(app_title)

if wx==1:

tm_start=tm_init

# 首次进入第 9 秒自检，此后每隔 7 分钟执行一次自检

if d_tm(tm_start)[1]>=7 or (wx_init==0 and d_tm(tm_start)[0])>=9:

print('')

print(' 状态自检......')

print('-------------------------------------------')

close_note()

lock_trade()

print('-------------------------------------------')

print(' 自检结束......')

print('')

wx_init=1

tm_init=tm()[0]

else:

time.sleep(3)

login(id,password,2,1)



# 间隔时间

time.sleep(3)

# 扫描区

# ---------------------------------------------

imgxy1=(12,112,142,142) # 1920x1080,100% 缩放

imgxy2=(20,205,260,255) # 3860x2160,175% 缩放

# ---------------------------------------------

# 自动选择

for i in range(2):

imgxy=locals()['imgxy'+str(i+1)]

# --------------

# 扫描信号

z=Scanner(imgxy[0],imgxy[1],imgxy[2],imgxy[3])

if z[5]=='9':

break

# 编码解析

# ---------------------------------------------------------------- 初始化

stk_code='000063'

tradel=0

tradel_num=0

trades=0

trades_num=0

# ---------------------------------------------------------------- 解 码

check=z[5] # 校验码 ('9'-正常，'0'-异常)

if check=='9':

stk_code=z[0] # 股票代码

tradel=int(z[1]) # 长线交易信号 ( [1—4] 买入，[5—8] 卖出 )

tradel_num=int(z[2])*100 # 长线交易数量 ( 1-代表100股，最大999*100股 )

trades=int(z[3]) # 短线交易信号 ( [1—4] 买入，[5—8] 卖出 )

trades_num=int(z[4])*100 # 短线交易数量 ( 1-代表100股，最大999*100股 )

# --------------------------------------------------------------------------



# 记录交易时间

# --------------------

zm = tm()

hour = zm[1]

minute = zm[2]

second = zm[3]

timex = zm[4]

time_str = zm[5]

# --------------------



# 下单策略

# --------------------------------------------------------参数区

Place_Order='no'

long_buy=(tradel==1 or tradel==2 or tradel==3 or tradel==4)

long_sel=(tradel==5 or tradel==6 or tradel==7 or tradel==8)

long_Trade=(long_buy or long_sel)

short_buy=(trades==1 or trades==2 or trades==3 or trades==4)

short_sel=(trades==5 or trades==6 or trades==7 or trades==8)

short_Trade=(short_buy or short_sel)

Time1=(hour== 9 and minute>=50 and minute<=60)

Time2=(hour==11 and minute>= 0 and minute<=10)

Time3=(hour==13 and minute>=15 and minute<=25)

Time4=(hour==14 and minute>=50 and minute<=60)

Trade_time=(timex>=time1 and timex<=time2) or time_trade==0

# ---------------------------------------------------------策略区

orderx=(0,'000063',0,0,'off')

# ---------------------------------------------------------

# 长线信号

# --------

# 测试下单

if Trade_mode==0 and long_Trade==True and t1==0:

Place_Order='yes'

orderx=(tradel,stk_code,tradel_num,0,'off')

t1=1

# 盘中下单

if Trade_mode==1 and Trade_time==True and long_Trade==True and t2==0:

Place_Order='yes'

orderx=(tradel,stk_code,tradel_num,1,'on')

t2=1

# 分批下单

if Trade_mode==2 and Trade_time==True and long_Trade==True and (t1==0 or t2==0 or t3==0 or t4==0):

# ---------------------------------------------------------------

if Time1==True and t1==0:

Place_Order='yes'

orderx=(tradel,stk_code,tradel_num,4,'on')

t1=1

if Time2==True and t2==0:

Place_Order='yes'

orderx=(tradel,stk_code,tradel_num,3,'on')

t2=1

if Time3==True and t3==0:

Place_Order='yes'

orderx=(tradel,stk_code,tradel_num,2,'on')

t3=1

if Time4==True and t4==0:

Place_Order='yes'

orderx=(tradel,stk_code,tradel_num,1,'on')

t4=1

# ---------------------------------------------------------------

# 最优下单

if Trade_mode==3 and Trade_time==True and long_Trade==True and t3==0:

# 出现最优信号，立即下单

if (long_buy==True and short_buy==True) or (long_sel==True and short_sel==True):

Place_Order='yes'

orderx=(tradel,stk_code,tradel_num,1,'on')

t3=1

# 若无最优信号，尾盘下单

elif Time4==True:

Place_Order='yes'

orderx=(tradel,stk_code,tradel_num,1,'on')

t3=1

# 尾盘下单

if Trade_mode==4 and Trade_time==True and long_Trade==True and t4==0 and Time4==True:

Place_Order='yes'

orderx=(tradel,stk_code,tradel_num,1,'on')

t4=1

# 短线信号

# ----------------------------------------------------------------------------------

# 盘中下单

if Short_mode==1 and Trade_time==True and short_buy==True and buycount==0:

Place_Order='yes'

if Trade_mode==0:

orderx=(trades,stk_code,tradel_num,4,'off')

else:

orderx=(trades,stk_code,tradel_num,4,'on')

buycount=1

if Short_mode==1 and Trade_time==True and short_sel==True and selcount==0:

Place_Order='yes'

if Trade_mode==0:

orderx=(trades,stk_code,tradel_num,4,'off')

else:

orderx=(trades,stk_code,tradel_num,4,'on')

selcount=1

# ----------------------------------------------------------------------------------



# 订单信息

# ----------------------------------------------------------------------

if Place_Order=='yes' and long_Trade == True and long_buy == True:

print(z,'买入',(t1,t2,t3,t4),(buycount,selcount),'时间:',time_str)

elif Place_Order=='yes' and long_Trade == True and long_sel == True:

print(z,'卖出',(t1,t2,t3,t4),(buycount,selcount),'时间:',time_str)

elif check!='9':

print(z,'异常',(t1,t2,t3,t4),(buycount,selcount),'时间:',time_str)

else:

print(z,'wait',(t1,t2,t3,t4),(buycount,selcount),'时间:',time_str)

# -----------------------------------------------------------------------

# 下单交易

if Place_Order=='yes':

print('')

print(' 准备交易......')

print('-------------------------------------------')

fast_trade(orderx[0],orderx[1],orderx[2],orderx[3],orderx[4])

print(' 已经下单：',orderx)

print('-------------------------------------------')

print(' 交易结束......')

print('')

# 定时退出

# ---------------------------------------------------------------------------

if (timex>=time_start and timex<time_end) or time_work==0:

pass

else:

print('')

print('')

print(' # -----------------------------------------------------------------')

print('')

print(' TDX_机器人已经下班！')

print('')

print(' TDX_机器人定时器可能仍在运行中！')

print('')

print(' 如果想明天 ',time_start,' 继续，请保持本窗口,不要关闭！ ')

print('')

print(' # -----------------------------------------------------------------')

print('')

print('')

app_exit()

break
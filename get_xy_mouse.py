import pymouse
print('点击回车查看当前鼠标的坐标')
while True:
    _ = input()  # input起到阻塞程序的作用
    print(pymouse.PyMouse().position())  # 获取当前鼠标指针的坐标




# -*- coding: utf-8 -*-
import ctypes
import tkinter
import tkinter.messagebox
from PIL import Image, ImageTk

from user_log_in_operation import *
from user_sign_up_operation import *


def user_sign_up_interface():
    # 触发用户操作界面窗口
    def create_user_interface():
        tkinter.messagebox.showinfo('提交成功')
        user_sign_up_win.destroy()

    # 鼠标左键按下时的事件处理函数
    def onLeftButtonDown(event):
        X.set(event.x)
        Y.set(event.y)
        canMove.set(1)

    # 鼠标移动时的事件处理函数
    def onLeftButtonMove(event):
        if canMove.get() == 0:
            return
        newX = user_sign_up_win.winfo_x() + (event.x - X.get())
        newY = user_sign_up_win.winfo_y() + (event.y - Y.get())
        user_sign_up_win.geometry('%dx%d+%d+%d' % (width, height, newX, newY))

    # 鼠标左键抬起时的事件处理函数
    def onLeftButtonUp(event):
        canMove.set(0)

    def press_submit_button():
        account = enter_account.get()
        password = enter_password.get()
        password_again = enter_password_again.get()
        name = enter_name.get()
        address = enter_address.get()
        tele = enter_tele.get()
        if account == '' or password == '' or password_again == '' or name == '' or address == '' or tele == '':
            tkinter.messagebox.showwarning('非法输入', message='输入不能为空！')
            return
        already_exist, message = CheckIfUserExist(account)
        if already_exist:
            tkinter.messagebox.showinfo(title='注册错误', message='账号已存在，请更换账户名！')
            return
        if not password.isalnum() or len(password) < 6 or len(password) > 10:
            tkinter.messagebox.showwarning(title='非法输入', message='密码为6-10位，仅允许数字和字母!')
            return
        if password != password_again:
            tkinter.messagebox.showinfo(title='注册错误', message='两次密码输入不一致，请检查！')
            return
        if len(tele) != 11 or (not tele.isdigit()):
            tkinter.messagebox.showwarning(title='非法输入', message='手机号码应为11位数字！')
            return
        Receive_Sign_Up_Require([account, password, name, address, tele])
        tkinter.messagebox.showinfo(title='注册申请成功', message='注册申请已提交，请等待管理员审核！')
        user_sign_up_win.destroy()

    user_sign_up_win = tkinter.Tk()
    # 调用api设置成由应用程序缩放
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # 调用api获得当前的缩放因子
    ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
    # 设置缩放因子
    user_sign_up_win.tk.call('tk', 'scaling', ScaleFactor/75)

    width = 600
    height = 800
    # 将窗口居中
    screenwidth = user_sign_up_win.winfo_screenwidth()
    screenheight = user_sign_up_win.winfo_screenheight()
    user_sign_up_win.geometry('%dx%d+%d+%d'%(width, height, screenwidth-width/2, screenheight/2))
    user_sign_up_win.title('新用户注册')

    canvas = tkinter.Canvas(user_sign_up_win, highlightthickness=0, width=width, height=height)
    canvas.place(x=0, y=0)
    image = Image.open('images/用户注册界面.png').resize((width, height))
    image = ImageTk.PhotoImage(image)
    canvas.create_image(width/2, height/2, image=image)
    # 不允许修改大小
    user_sign_up_win.resizable(False, False)
    # 不显示标题栏
    user_sign_up_win.overrideredirect(True)
    # 设置白色透明色，这样图片中所有白色区域都被认为是透明的了
    user_sign_up_win.wm_attributes('-transparentcolor', 'black')

    # 两个文字标签，账号和密码两个部分
    canvas.create_text(160, 205, text='账号', font=('FangSong', 12, 'bold'))
    enter_account = tkinter.Entry(user_sign_up_win, font=('Times New Romans', 10), bd=3)
    enter_account.place(x=205, y=190)

    canvas.create_text(160, 285, text='密码', font=('FangSong', 12, 'bold'))
    enter_password = tkinter.Entry(user_sign_up_win, font=('Times New Romans', 10), show='*', bd=3)
    canvas.create_text(315, 325, text='(密码为6-10位，仅允许数字和字母)', font=('HeiTi', 9))
    enter_password.place(x=205, y=270)

    canvas.create_text(130, 365, text='再次输入', font=('FangSong', 12, 'bold'))
    enter_password_again = tkinter.Entry(user_sign_up_win, font=('Times New Romans', 10), show='*', bd=3)
    enter_password_again.place(x=205, y=350)

    canvas.create_text(160, 445, text='姓名', font=('FangSong', 12, 'bold'))
    enter_name = tkinter.Entry(user_sign_up_win, font=('Times New Romans', 10), bd=3)
    enter_name.place(x=205, y=430)

    canvas.create_text(160, 525, text='住址', font=('FangSong', 12, 'bold'))
    enter_address = tkinter.Entry(user_sign_up_win, font=('Times New Romans', 10), bd=3)
    enter_address.place(x=205, y=510)

    canvas.create_text(160, 605, text='电话', font=('FangSong', 12, 'bold'))
    enter_tele = tkinter.Entry(user_sign_up_win, font=('Times New Romans', 10), bd=3)
    enter_tele.place(x=205, y=590)

    # 按钮部件
    submit_sign_up_require = Image.open('images/提交注册申请按钮.png').resize((178, 50))
    submit_sign_up_require = ImageTk.PhotoImage(submit_sign_up_require)
    submit_sign_up_button = tkinter.Button(user_sign_up_win, image=submit_sign_up_require, bd=0, cursor='hand2', command=press_submit_button)
    submit_sign_up_button.place(x=210, y=670)

    close_win_image = Image.open('images/关闭按钮.png').resize((25, 25))
    close_win_image = ImageTk.PhotoImage(close_win_image)
    close_win_button = tkinter.Button(user_sign_up_win, image=close_win_image, bd=0, cursor='hand2', command=user_sign_up_win.destroy)
    close_win_button.place(x=520, y=40)

    # 鼠标左键按下时设置为1表示可移动窗口，抬起后不可移动
    canMove = tkinter.IntVar(user_sign_up_win, value=0)
    # 记录鼠标左键按下的位置
    X = tkinter.IntVar(user_sign_up_win, value=0)
    Y = tkinter.IntVar(user_sign_up_win, value=0)

    user_sign_up_win.bind('<Button-1>', onLeftButtonDown)
    user_sign_up_win.bind('<B1-Motion>', onLeftButtonMove)
    user_sign_up_win.bind('<ButtonRelease-1>', onLeftButtonUp)

    user_sign_up_win.mainloop()


if __name__ == '__main__':
    user_sign_up_interface()

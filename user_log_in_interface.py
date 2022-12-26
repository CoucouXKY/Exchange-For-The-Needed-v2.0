# -*- coding: utf-8 -*-
import ctypes
import tkinter
import tkinter.messagebox
from PIL import Image, ImageTk

from user_log_in_operation import CheckUserIdentity
from admin_log_in_interface import administrator_log_in_interface
from user_sign_up_interface import user_sign_up_interface
from user_operation_interface import RegularUser


def user_log_in_interface():
    # 触发用户操作界面窗口
    def create_user_interface(user_account, user_password):
        tkinter.messagebox.showinfo(title='登录成功', message='欢迎使用你帮我助v2.0系统')
        user_log_in_win.destroy()
        regular_user = RegularUser(user_account, user_password)
        regular_user.user_operation_interface()

    # 点击“登录”按钮触发函数
    def press_log_in_button():
        user_account = enter_account.get()
        user_password = enter_password.get()
        if user_account == '' or user_password == '':
            tkinter.messagebox.showwarning(title='非法输入', message='输入不能为空！')
            return
        is_correct, message = CheckUserIdentity(user_account, user_password)
        if is_correct:
            create_user_interface(user_account, user_password)
        else:
            tkinter.messagebox.showinfo(title='登陆错误', message=message)

    # 鼠标左键按下时的事件处理函数
    def onLeftButtonDown(event):
        X.set(event.x)
        Y.set(event.y)
        canMove.set(1)

    # 鼠标移动时的事件处理函数
    def onLeftButtonMove(event):
        if canMove.get() == 0:
            return
        newX = user_log_in_win.winfo_x() + (event.x - X.get())
        newY = user_log_in_win.winfo_y() + (event.y - Y.get())
        user_log_in_win.geometry('%dx%d+%d+%d' % (width, height, newX, newY))

    # 鼠标左键抬起时的事件处理函数
    def onLeftButtonUp(event):
        canMove.set(0)

    def press_admin_log_in_button():
        user_log_in_win.destroy()
        administrator_log_in_interface()

    def press_user_sign_up():
        user_log_in_win.destroy()
        user_sign_up_interface()

    user_log_in_win = tkinter.Tk()
    # 调用api设置成由应用程序缩放
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # 调用api获得当前的缩放因子
    ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
    # 设置缩放因子
    user_log_in_win.tk.call('tk', 'scaling', ScaleFactor/75)

    width = 600
    height = 800
    # 将窗口居中
    screenwidth = user_log_in_win.winfo_screenwidth()
    screenheight = user_log_in_win.winfo_screenheight()
    user_log_in_win.geometry('%dx%d+%d+%d'%(width, height, screenwidth-width/2, screenheight/2))
    user_log_in_win.title('欢迎使用你帮我助v2.0')

    canvas = tkinter.Canvas(user_log_in_win, highlightthickness=0, width=width, height=height)
    canvas.place(x=0, y=0)
    image = Image.open('images/登录界面.png').resize((width, height))
    image = ImageTk.PhotoImage(image)
    canvas.create_image(width/2, height/2, image=image)
    # 不允许修改大小
    user_log_in_win.resizable(False, False)
    # 不显示标题栏
    user_log_in_win.overrideredirect(True)
    # 设置白色透明色，这样图片中所有白色区域都被认为是透明的了
    user_log_in_win.wm_attributes('-transparentcolor', 'black')

    # 两个文字标签，账号和密码两个部分
    canvas.create_text(130, 550, text='账号', font=('FangSong', 12, 'bold'))
    enter_account = tkinter.Entry(user_log_in_win, font=('Times New Romans', 10), bd=3)
    enter_account.place(x=175, y=535)
    canvas.create_text(130, 620, text='密码', font=('FangSong', 12, 'bold'))
    enter_password = tkinter.Entry(user_log_in_win, font=('Times New Romans', 10), show='*', bd=3)
    enter_password.place(x=175, y=605)

    # 按钮部件
    administrator_button_image = Image.open('images/管理员按钮.png').resize((150, 50))
    administrator_button_image = ImageTk.PhotoImage(administrator_button_image)
    administrator_button = tkinter.Button(user_log_in_win, image=administrator_button_image, bd=0, cursor='hand2', command=press_admin_log_in_button)
    administrator_button.place(x=80, y=680)

    login_in_button_image = Image.open('images/登录按钮.png').resize((120, 50))
    login_in_button_image = ImageTk.PhotoImage(login_in_button_image)
    log_in_button = tkinter.Button(user_log_in_win, image=login_in_button_image, bd=0, cursor='hand2', command=press_log_in_button)
    log_in_button.place(x=250, y=680)

    sign_up_button_image = Image.open('images/注册按钮.png').resize((120, 50))
    sign_up_button_image = ImageTk.PhotoImage(sign_up_button_image)
    sign_up_button = tkinter.Button(user_log_in_win, image=sign_up_button_image, bd=0, cursor='hand2', command=press_user_sign_up)
    sign_up_button.place(x=390, y=680)

    close_win_image = Image.open('images/关闭按钮.png').resize((25, 25))
    close_win_image = ImageTk.PhotoImage(close_win_image)
    close_win_button = tkinter.Button(user_log_in_win, image=close_win_image, bd=0, cursor='hand2', command=user_log_in_win.destroy)
    close_win_button.place(x=520, y=40)

    # 鼠标左键按下时设置为1表示可移动窗口，抬起后不可移动
    canMove = tkinter.IntVar(user_log_in_win, value=0)
    # 记录鼠标左键按下的位置
    X = tkinter.IntVar(user_log_in_win, value=0)
    Y = tkinter.IntVar(user_log_in_win, value=0)

    user_log_in_win.bind('<Button-1>', onLeftButtonDown)
    user_log_in_win.bind('<B1-Motion>', onLeftButtonMove)
    user_log_in_win.bind('<ButtonRelease-1>', onLeftButtonUp)

    user_log_in_win.mainloop()


if __name__ == '__main__':
    user_log_in_interface()

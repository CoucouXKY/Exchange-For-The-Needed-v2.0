# -*- coding: utf-8 -*-

import ctypes
import tkinter
import tkinter.messagebox
from PIL import Image, ImageTk

from admin_log_in_operation import CheckAdministraterIdentity
from admin_operation_interface import Admin


# 点击“管理员入口”触发管理员登录界面
def administrator_log_in_interface():
    # 触发用户操作界面窗口
    def create_admin_interface(admin_account, admin_password):
        tkinter.messagebox.showinfo(title='登录提示', message='登录成功!')
        admin_log_in_win.destroy()
        admin = Admin(admin_account, admin_password)
        admin.admin_operation_interface()

    # 点击“登录”按钮触发函数
    def press_log_in_button():
        admin_account = enter_account.get()
        admin_password = enter_password.get()
        if admin_account == '' or admin_password == '':
            tkinter.messagebox.showwarning(title='非法输入', message='输入不能为空！')
            return
        is_correct, message = CheckAdministraterIdentity(admin_account, admin_password)
        if is_correct:
            create_admin_interface(admin_account, admin_password)
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
        newX = admin_log_in_win.winfo_x() + (event.x - X.get())
        newY = admin_log_in_win.winfo_y() + (event.y - Y.get())
        admin_log_in_win.geometry('%dx%d+%d+%d' % (width, height, newX, newY))

    # 鼠标左键抬起时的事件处理函数
    def onLeftButtonUp(event):
        canMove.set(0)


    admin_log_in_win = tkinter.Tk()
    # 调用api设置成由应用程序缩放
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # 调用api获得当前的缩放因子
    ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    admin_log_in_win.tk.call('tk', 'scaling', ScaleFactor/75)

    width = 720
    height = 480

    # 将窗口居中
    screenwidth = admin_log_in_win.winfo_screenwidth()
    screenheight = admin_log_in_win.winfo_screenheight()
    admin_log_in_win.geometry('%dx%d+%d+%d' % (width, height, screenwidth - width / 2, (screenheight + 300) / 2))
    admin_log_in_win.title('管理员登录')

    canvas = tkinter.Canvas(admin_log_in_win, highlightthickness=0, width=width, height=height)
    canvas.place(x=0, y=0)
    img = Image.open('images/管理员登录.png').resize((width, height))
    img = ImageTk.PhotoImage(img)
    canvas.create_image(width / 2, height / 2, image=img)

    # 不允许修改大小
    admin_log_in_win.resizable(False, False)

    # 不显示标题栏
    admin_log_in_win.overrideredirect(True)

    # 设置白色透明色，这样图片中所有白色区域都被认为是透明的了
    admin_log_in_win.wm_attributes('-transparentcolor', 'black')

    # 两个文字标签，账号和密码两个部分
    canvas.create_text(320, 200, text='账号', font=('FangSong', 12, 'bold'))
    enter_account = tkinter.Entry(admin_log_in_win, font=('Times New Romans', 10), bd=3)
    enter_account.place(x=365, y=185)

    canvas.create_text(320, 270, text='密码', font=('FangSong', 12, 'bold'))
    enter_password = tkinter.Entry(admin_log_in_win, font=('Times New Romans', 10), show='*', bd=3)
    enter_password.place(x=365, y=255)

    # 按钮部件
    login_in_button_image = Image.open('images/登录按钮.png').resize((120, 50))
    login_in_button_image = ImageTk.PhotoImage(login_in_button_image)
    log_in_button = tkinter.Button(admin_log_in_win, image=login_in_button_image, bd=0, cursor='hand2', command=press_log_in_button)
    log_in_button.place(x=420, y=350)

    close_win_image = Image.open('images/关闭按钮.png').resize((25, 25))
    close_win_image = ImageTk.PhotoImage(close_win_image)
    close_win_button = tkinter.Button(admin_log_in_win, image=close_win_image, bd=0, cursor='hand2', command=admin_log_in_win.destroy)
    close_win_button.place(x=640, y=40)

    # 鼠标左键按下时设置为1表示可移动窗口，抬起后不可移动
    canMove = tkinter.IntVar(admin_log_in_win, value=0)
    # 记录鼠标左键按下的位置
    X = tkinter.IntVar(admin_log_in_win, value=0)
    Y = tkinter.IntVar(admin_log_in_win, value=0)

    admin_log_in_win.bind('<Button-1>', onLeftButtonDown)
    admin_log_in_win.bind('<B1-Motion>', onLeftButtonMove)
    admin_log_in_win.bind('<ButtonRelease-1>', onLeftButtonUp)

    admin_log_in_win.mainloop()


if __name__ == '__main__':
    administrator_log_in_interface()

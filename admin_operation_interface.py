# -*- coding: utf-8 -*-

import ctypes
import tkinter
from PIL import ImageTk, Image
from tkinter import simpledialog
import tkinter.messagebox
from tkinter.ttk import Treeview
from tkinter import ttk
import csv
import os

from basic_class import User

class Admin(User):
    """管理员类"""

    def __init__(self, account, password):
        super().__init__(account, password)

    # 载入管理员操作界面
    def admin_operation_interface(self):
        # 按下"添加物品类别"后调出相应控件
        def add_new_type():
            def add_attribute():
                attribute = simpledialog.askstring('新物品属性输入', '要添加的属性', initialvalue='数量')
                if attribute in list_box.get(0, tkinter.END):
                    tkinter.messagebox.showwarning(title='非法输入', message='属性已存在!')
                    return
                list_box.insert(tkinter.END, attribute)

            def delete_attribute():
                list_box.delete(list_box.curselection())

            def delete_all_attribute():
                list_box.delete(0, tkinter.END)

            def confirm_addition():
                type_name = enter_new_type_name.get()
                attributes = list_box.get(0, tkinter.END)
                if type_name == '' or len(attributes) == 0:
                    tkinter.messagebox.showwarning(title='非法输入', message='输入不能为空！')
                    return
                if self.CheckIfItemTypeExist(type_name):
                    tkinter.messagebox.showinfo(title='种类添加失败', message='物品种类已经存在！')
                    return
                self.AddNewItemType([type_name] + list(attributes))
                tkinter.messagebox.showinfo(title='添加成功', message='物品种类添加成功！')
                for widget in temp_frame.winfo_children():
                    if widget != frame_bg:
                        widget.destroy()

            # 删除temp_frame上的全部组件
            for widget in temp_frame.winfo_children():
                if widget != frame_bg:
                    widget.destroy()
            # 布局提示文本和输入框
            temp_text1 = tkinter.Label(temp_frame, text='添加物品种类', font=('FangSong', 14, 'bold'))
            temp_text1.place(relx=0.05, rely=0.1)
            enter_new_type_name = tkinter.Entry(temp_frame, font=('Times New Romans', 20), bd=3,
                                                highlightcolor='orange', highlightthickness=5, fg='orange')
            enter_new_type_name.place(relx=0.05, rely=0.15)
            temp_text2 = tkinter.Label(temp_frame, text='已添加的属性', font=('FangSong', 14, 'bold'))
            temp_text2.place(relx=0.05, rely=0.25)

            # 布局属性列表和滚动轴
            frame = tkinter.Frame(temp_frame, relief='groove', width=1040, height=550, bg='red')
            frame.place(relx=0.05, rely=0.3)
            list_box = tkinter.Listbox(temp_frame, bd=3, font=('Times New Romans', 20), fg='orange',
                                       highlightthickness=5, highlightcolor='orange', width=36)
            list_box.place(relx=0.05, rely=0.3)
            scr = tkinter.Scrollbar(frame, orient='vertical')
            scr.place(relwidth=0.05, relheight=1, relx=0.95, rely=0)
            list_box.configure(yscrollcommand=scr.set)
            scr.configure(command=list_box.yview)

            # 布局按钮
            add_button = tkinter.Button(temp_frame, text='添加属性', font=('FangSong', 10, 'bold'), bd=5,
                                        command=add_attribute, relief='groove', bg='orange', fg='white', activeforeground='orange')
            add_button.place(relx=0.3, rely=0.25)
            delete_button = tkinter.Button(temp_frame, text='删除属性', font=('FangSong', 10, 'bold'), bd=5,
                                        command=delete_attribute,
                                        relief='groove', bg='orange', fg='white', activeforeground='orange')
            delete_button.place(relx=0.42, rely=0.25)
            delete_all_button = tkinter.Button(temp_frame, text='清空列表', font=('FangSong', 10, 'bold'), bd=5,
                                           command=delete_all_attribute,
                                           relief='groove', bg='orange', fg='white', activeforeground='orange')
            delete_all_button.place(relx=0.54, rely=0.25)
            confirm_button = tkinter.Button(temp_frame, text='确认添加物品种类', font=('FangSong', 12, 'bold'), bd=5,
                                            command=confirm_addition, relief='groove', bg='orange', fg='white', activeforeground='orange')
            confirm_button.place(relx=0.28, rely=0.86)

        # 按下“修改物品类别”调出相应控件
        def change_type():
            def click_type_list(event):
                list_box_2.delete(0, tkinter.END)
                select_type = list_box_1.get(list_box_1.curselection())
                # 获取选中物品种类当前对应的属性
                attributes = self.GetSpecificTypeAttributes(select_type)
                for attribute in attributes:
                    list_box_2.insert(tkinter.END, attribute)

            def change_attribute():
                new_attribute = simpledialog.askstring('属性输入', '将属性修改为')
                if new_attribute == '':
                    tkinter.messagebox.showwarning(title='非法输入', message='输入不能为空！')
                    return
                try:
                    self.ChangeTypeAttribute(list_box_1.get(list_box_1.curselection()), list_box_2.get(list_box_2.curselection()),
                                        new_attribute)
                except:
                    tkinter.messagebox.showwarning(title='选择错误', message='请检查是否已选择物品种类及对应属性！')
                else:
                    tkinter.messagebox.showinfo(title='修改成功', message='物品属性修改成功！')
                    list_box_2.insert(list_box_2.curselection(), new_attribute)
                    list_box_2.delete(list_box_2.curselection()[0])

            def change_type_name():
                new_type_name = simpledialog.askstring('类型输入', '将物品类型修改为')
                if new_type_name == '':
                    tkinter.messagebox.showwarning(title='非法输入', message='输入不能为空！')
                    return
                try:
                    self.ChangeTypeName(list_box_1.get(list_box_1.curselection()), new_type_name)
                except:
                    tkinter.messagebox.showwarning(title='选择错误', message='请检查是否已选择要修改的物品种类！')
                else:
                    tkinter.messagebox.showinfo(title='修改成功', message='物品名称修改成功！')
                    list_box_1.insert(list_box_1.curselection(), new_type_name)
                    list_box_1.delete(list_box_1.curselection()[0])

            # 删除temp_frame上的全部组件
            for widget in temp_frame.winfo_children():
                if widget != frame_bg:
                    widget.destroy()
            # 选择修改物品类别的部分
            temp_text1 = tkinter.Label(temp_frame, text='选择物品种类', font=('FangSong', 14, 'bold'))
            temp_text1.place(relx=0.05, rely=0.1)
            frame_1 = tkinter.Frame(temp_frame, relief='groove', width=400, height=720, bg='red')
            frame_1.place(relx=0.05, rely=0.15)
            list_box_1 = tkinter.Listbox(temp_frame, bd=3, font=('Times New Romans', 16), fg='orange',
                                       highlightthickness=5, highlightcolor='orange', width=16, height=16, exportselection=False)
            list_box_1.place(relx=0.05, rely=0.15)
            scr_1 = tkinter.Scrollbar(frame_1, orient='vertical')
            scr_1.place(relwidth=0.1, relheight=1, relx=0.9, rely=0)
            list_box_1.configure(yscrollcommand=scr_1.set)
            scr_1.configure(command=list_box_1.yview)

            list_box_1.bind('<<ListboxSelect>>', click_type_list)
            type_list = self.GetItemTypeList()
            for item_type in type_list:
                list_box_1.insert(tkinter.END, item_type)

            # 选择修改物品属性的部分
            temp_text2 = tkinter.Label(temp_frame, text='当前属性', font=('FangSong', 14, 'bold'))
            temp_text2.place(relx=0.35, rely=0.25)
            frame_2 = tkinter.Frame(temp_frame, relief='groove', width=850, height=542, bg='red')
            frame_2.place(relx=0.35, rely=0.3)
            list_box_2 = tkinter.Listbox(temp_frame, bd=3, font=('Times New Romans', 16), fg='orange',
                                         highlightthickness=5, highlightcolor='orange', width=36, height=12, exportselection=False)
            list_box_2.place(relx=0.35, rely=0.3)
            scr_2 = tkinter.Scrollbar(frame_2, orient='vertical')
            scr_2.place(relwidth=0.05, relheight=1, relx=0.95, rely=0)
            list_box_2.configure(yscrollcommand=scr_2.set)
            scr_2.configure(command=list_box_2.yview)

            # 布局按钮
            change_attribute_button = tkinter.Button(temp_frame, text='修改物品属性', font=('FangSong', 12, 'bold'), bd=5,
                                            command=change_attribute, relief='groove', bg='orange', fg='white',
                                            activeforeground='orange')
            change_attribute_button.place(relx=0.76, rely=0.24)
            change_type_name_button = tkinter.Button(temp_frame, text='修改物品名称', font=('FangSong', 12, 'bold'), bd=5,
                                            command=change_type_name, relief='groove', bg='orange', fg='white',
                                            activeforeground='orange')
            change_type_name_button.place(relx=0.05, rely=0.82)

        # 点击“用户注册审批”调出相应控件
        def user_require_approval():
            # 点击复制到粘贴板
            def treeviewclick(event):
                approved_accounts = []
                delete_items = tree.selection()
                for selection in tree.selection():
                    approved_accounts.append(tree.item(selection, "values")[0])
                approve_button.configure(command=lambda : approve_request(approved_accounts, delete_items))
                refuse_button.configure(command=lambda : refuse_request(delete_items))

            def approve_request(approved_IDs, delete_items):
                # 将用户从注册名单中删除，加入正式用户名单
                self.TurnToFormalUser(approved_IDs)
                for delete_item in delete_items:
                    tree.delete(delete_item)

            def refuse_request(delete_items):
                # 将拒绝的用户从注册名单中删除
                for delete_item in delete_items:
                    tree.delete(delete_item)

            # 删除temp_frame上的全部组件
            for widget in temp_frame.winfo_children():
                if widget != frame_bg:
                    widget.destroy()

            # 创建提示文本
            temp_text = tkinter.Label(temp_frame, text='待处理的用户注册申请', font=('FangSong', 14, 'bold'))
            temp_text.place(relx=0.05, rely=0.1)

            # 布局表格和滚动条
            frame = tkinter.Frame(temp_frame, relief='groove', width=1002, height=596, bg='red')
            frame.place(relx=0.05, rely=0.2)
            cols = ("账号", "姓名", "住址", "电话")
            ybar = tkinter.Scrollbar(frame, orient='vertical')  # 竖直滚动条
            style_head = ttk.Style()
            style_head.configure("Treeview.Heading", font=('FangSong', 14), rowheight=50)
            style_head.configure("Treeview", font=('FangSong', 12), rowheight=40)
            tree = Treeview(temp_frame, show='headings', columns=cols, yscrollcommand=ybar.set, height=14)
            ybar['command'] = tree.yview
            # 表头设置
            for col in cols:
                tree.heading(col, text=col)  # 行标题
                tree.column(col, width=240, anchor='center')  # 每一行的宽度,'w'意思为靠右
            # 插入数据
            sign_up_info = self.GetSignUpInfo()
            for info in sign_up_info:
                tree.insert("", "end", values=(info[0], info[2], info[3], info[4]))

            tree.place(relx=0.05, rely=0.2)
            ybar.place(relwidth=0.04, relheight=1, relx=0.96, rely=0)
            tree.bind('<ButtonRelease-1>', treeviewclick)

            # 布局按钮
            approve_button = tkinter.Button(temp_frame, text='审核通过', font=('FangSong', 12, 'bold'), bd=5,
                                                     relief='groove', bg='orange', fg='white',
                                                     activeforeground='orange')
            approve_button.place(relx=0.75, rely=0.2)
            refuse_button = tkinter.Button(temp_frame, text='拒绝申请', font=('FangSong', 12, 'bold'), bd=5,
                                            relief='groove', bg='orange', fg='white',
                                            activeforeground='orange')
            refuse_button.place(relx=0.75, rely=0.3)

        admin_operate_win = tkinter.Tk()
        admin_operate_win.resizable(False, False)
        # 调用api设置成由应用程序缩放
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        # 调用api获得当前的缩放因子
        ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        admin_operate_win.tk.call('tk', 'scaling', ScaleFactor / 75)

        width = 1920
        height = 1080
        screenwidth = admin_operate_win.winfo_screenwidth()
        screenheight = admin_operate_win.winfo_screenheight()
        admin_operate_win.geometry('%dx%d+%d+%d' % (width, height, screenwidth - width / 2, screenheight - height / 2))
        admin_operate_win.title('管理员操作界面')

        # 背景
        canvas = tkinter.Canvas(admin_operate_win, width=width, height=height, bd=0, highlightthickness=0, bg='white')
        canvas.place(x=0, y=0)
        img = Image.open('images/界面壁纸半透明.png').resize((width, height))
        img = ImageTk.PhotoImage(img)
        canvas.create_image(width / 2, height / 2, image=img)

        # 按钮
        add_type_button_image = Image.open('images/添加物品种类按钮.png').resize((214, 60))
        add_type_button_image = ImageTk.PhotoImage(add_type_button_image)
        add_type_button = tkinter.Button(admin_operate_win, image=add_type_button_image, bd=0, cursor='hand2')
        add_type_button.configure(command=add_new_type)
        add_type_button.place(x=115, y=250)

        change_type_button_image = Image.open('images/修改物品种类按钮.png').resize((214, 60))
        change_type_button_image = ImageTk.PhotoImage(change_type_button_image)
        change_type_button = tkinter.Button(admin_operate_win, image=change_type_button_image, bd=0, cursor='hand2')
        change_type_button.configure(command=change_type)
        change_type_button.place(x=115, y=350)

        user_require_approval_button_image = Image.open('images/用户注册审批按钮.png').resize((214, 60))
        user_require_approval_button_image = ImageTk.PhotoImage(user_require_approval_button_image)
        user_require_approval_button = tkinter.Button(admin_operate_win, image=user_require_approval_button_image, bd=0,
                                                      cursor='hand2')
        user_require_approval_button.configure(command=user_require_approval)
        user_require_approval_button.place(x=115, y=450)

        # 一个框架，用作所有临时控件的父容器，便于删除临时控件
        temp_width = 1483
        temp_height = 1080
        temp_frame = tkinter.Frame(admin_operate_win, relief='flat', bg='white', width=temp_width, height=temp_height)
        temp_frame.place(x=437, y=0)
        frame_bg_img = Image.open('images/Frame背景.png').resize((temp_width, temp_height))
        frame_bg_img = ImageTk.PhotoImage(frame_bg_img)
        frame_bg = tkinter.Label(temp_frame, image=frame_bg_img)
        frame_bg.place(x=0, y=0)

        admin_operate_win.mainloop()

    # 检查要添加的产品种类是否已经存在
    def CheckIfItemTypeExist(self, item_type):
        with open("Type_Of_Goods.txt", "r", encoding='utf-8') as f:
            for line in f:
                if line.split(';')[0] == item_type:
                    print('Exist')
                    return True
            return False

    # 根据输入添加新的产品种类
    def AddNewItemType(self, item_info):
        with open("Type_Of_Goods.txt", "a", encoding='utf-8') as f:
            for element in item_info:
                f.write(element + ';')
            f.write('\n')
        with open(item_info[0] + '.csv', "w", newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['上传用户', '物品名称', '物品说明', '物品所在地址', '联系人手机', '邮箱'] + item_info[1:])

    # 返回某物品种类当前的属性列表
    def GetSpecificTypeAttributes(self, select_type):
        with open("Type_Of_Goods.txt", "r", encoding='utf-8') as f:
            for line in f:
                if line.split(';')[0] == select_type:
                    return line.split(';')[1:-1]

    def ChangeTypeAttribute(self, select_type, select_attribute, new_attribute):
        # 修改Type_Of_Goods.txt
        lines = []
        new_row = []
        with open("Type_Of_Goods.txt", "r", encoding='utf-8') as f:
            for line in f:
                if line.split(';')[0] == select_type:
                    new_row = line.split(';')
                    new_row[new_row.index(select_attribute)] = new_attribute
                    line = line.replace(select_attribute, new_attribute)
                lines.append(line)
        with open("Type_Of_Goods.txt", "w", encoding='utf-8') as f:
            for line in lines:
                f.write(line)

        # 修改对应的csv文件
        with open(select_type + '.csv', "r", newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            lines = list(reader)
        with open(select_type + '.csv', "w", newline='', encoding='utf-8') as csvfile:
            lines[0] = new_row[1:]
            writer = csv.writer(csvfile)
            writer.writerows(lines)

    def ChangeTypeName(self, old_name, new_name):
        lines = []
        with open("Type_Of_Goods.txt", "r", encoding='utf-8') as f:
            for line in f:
                if line.split(';')[0] == old_name:
                    line = line.replace(old_name, new_name)
                lines.append(line)
        with open("Type_Of_Goods.txt", "w", encoding='utf-8') as f:
            for line in lines:
                f.write(line)
        os.rename(old_name + '.csv', new_name + '.csv')

    def TurnToFormalUser(self, user_ids):
        with open('Sign_Up_Request.csv', "r") as csvfile:
            reader = csv.reader(csvfile)
            old_rows = list(reader)
            new_rows = [old_rows[0]]
            formal_user_info = []
            for sign_up_info in old_rows[1:]:
                if sign_up_info[0] in user_ids:
                    formal_user_info.append(sign_up_info)
                else:
                    new_rows.append(sign_up_info)
        with open('Sign_Up_Request.csv', "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(new_rows)
        with open('User_Account.csv', 'a', newline='') as csvfile:
            writer_object = csv.writer(csvfile)
            writer_object.writerows(formal_user_info)

    # 获取当前所有的注册申请信息
    def GetSignUpInfo(self):
        with open('Sign_Up_Request.csv', "r") as csvfile:
            reader = csv.reader(csvfile)
            info = list(reader)
            return info[1:]


if __name__ == '__main__':
    admin = Admin('abc', '123')
    admin.admin_operation_interface()

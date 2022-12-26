# -*- coding: utf-8 -*-

import ctypes
import tkinter
from PIL import ImageTk, Image
from tkinter import simpledialog
import tkinter.messagebox
from tkinter.ttk import Treeview
from tkinter import ttk
import csv
import pandas as pd
from operator import itemgetter

from basic_class import User


class RegularUser(User):
    """普通用户类"""

    def __init__(self, account, password):
        super().__init__(account, password)
        with open('User_Account.csv', "r") as csvfile:
            reader = csv.reader(csvfile)
            for sign_up_info in list(reader)[1:]:
                if sign_up_info[0] == account:
                    self.name = sign_up_info[2]
                    self.address = sign_up_info[3]
                    self.tele = sign_up_info[4]
                    break

    # 载入用户操作界面
    def user_operation_interface(self):
        def add_item():
            def click_add_type(event):
                items = tree.get_children()
                for item in items:
                    tree.delete(item)
                select_type = list_box.get(list_box.curselection())
                attributes = self.GetNeededAttributes(select_type)[1:]
                for attribute in attributes:
                    tree.insert("", "end", values=(attribute, ''))
                confirm_button.configure(command=lambda : confirm_addition(select_type))

            def treeviewclick(event):
                value = simpledialog.askstring(title='输入属性值', prompt=tree.item(tree.selection()[0], "values")[0])
                if value == '':
                    tkinter.messagebox.showwarning(title='非法输入', message='输入不能为空！')
                    return
                tree.set(tree.selection()[0], column='输入值', value=value)

            def confirm_addition(select_type):
                values = []
                item_ids = tree.get_children()
                for item_id in item_ids:
                    enter = tree.item(item_id)["values"][1]
                    if enter == '':
                        tkinter.messagebox.showwarning(title='非法输入', message='您还有未输入的属性值！')
                        return
                    values.append(enter)
                self.AddItemToCSV(select_type, values)
                tkinter.messagebox.showinfo(title='添加成功', message='物品添加成功！')
                for widget in temp_frame.winfo_children():
                    if widget != frame_bg:
                        widget.destroy()

            # 删除temp_frame上的全部组件
            for widget in temp_frame.winfo_children():
                if widget != frame_bg:
                    widget.destroy()
            # 选择修改物品类别的部分
            temp_text1 = tkinter.Label(temp_frame, text='选择要添加的产品种类', font=('FangSong', 14, 'bold'))
            temp_text1.place(relx=0.05, rely=0.1)
            frame_1 = tkinter.Frame(temp_frame, relief='groove', width=400, height=720, bg='red')
            frame_1.place(relx=0.05, rely=0.15)
            list_box = tkinter.Listbox(temp_frame, bd=3, font=('Times New Romans', 16), fg='orange',
                                         highlightthickness=5, highlightcolor='orange', width=16, height=16,
                                         exportselection=False)
            list_box.place(relx=0.05, rely=0.15)
            scr_1 = tkinter.Scrollbar(frame_1, orient='vertical')
            scr_1.place(relwidth=0.1, relheight=1, relx=0.9, rely=0)
            list_box.configure(yscrollcommand=scr_1.set)
            scr_1.configure(command=list_box.yview)

            list_box.bind('<<ListboxSelect>>', click_add_type)
            type_list = self.GetItemTypeList()
            for item_type in type_list:
                list_box.insert(tkinter.END, item_type)

            # 布局需要填入信息的表格
            temp_text2 = tkinter.Label(temp_frame, text='双击输入各个属性', font=('FangSong', 14, 'bold'))
            temp_text2.place(relx=0.4, rely=0.1)
            frame_2 = tkinter.Frame(temp_frame, relief='groove', width=640, height=598, bg='red')
            frame_2.place(relx=0.4, rely=0.15)
            cols = ("属性", "输入值")
            ybar = tkinter.Scrollbar(frame_2, orient='vertical')  # 竖直滚动条
            style_head = ttk.Style()
            style_head.configure("Treeview.Heading", font=('FangSong', 14), rowheight=50)
            style_head.configure("Treeview", font=('FangSong', 12), rowheight=40)
            tree = Treeview(temp_frame, show='headings', columns=cols, yscrollcommand=ybar.set, height=14,
                            selectmode='browse')
            ybar['command'] = tree.yview
            # 表头设置
            for col in cols:
                tree.heading(col, text=col)  # 行标题
                tree.column(col, width=300, anchor='center')  # 每一行的宽度,'w'意思为靠右

            tree.place(relx=0.4, rely=0.15)
            ybar.place(relwidth=0.06, relheight=1, relx=0.94, rely=0)
            tree.bind('<Double-Button-1>', treeviewclick)

            # 布局按钮
            confirm_button = tkinter.Button(temp_frame, text='确认添加', font=('FangSong', 12, 'bold'), bd=5,
                                                     relief='groove', bg='orange', fg='white',
                                                     activeforeground='orange')
            confirm_button.place(relx=0.4, rely=0.75)

        def delete_item():
            # 从所有物品清单文件中搜索当前操作用户拥有的物品，供用户选择删除
            def delete_possession():
                del_record = []
                del_indexes = []
                i = 0
                if len(list_box.curselection()) == 0:
                    tkinter.messagebox.showerror(title='删除出错', message='您在系统中登记的物品已清空!')
                    return
                for selection in list_box.curselection():
                    del_record.append((possession[selection][0], possession[selection][1]))
                    del_indexes.append(i)
                    i += 1
                del_indexes.reverse()
                for i in del_indexes:
                    list_box.delete(i)
                self.DelRecordsAccordingToFilenameAndRow(del_record)
                tkinter.messagebox.showinfo(title='删除成功', message='物品删除成功！')

            # 删除temp_frame上的全部组件
            for widget in temp_frame.winfo_children():
                if widget != frame_bg:
                    widget.destroy()

            # 布局属性列表和滚动轴
            temp_text = tkinter.Label(temp_frame, text='您当前在系统中登记的物品如下', font=('FangSong', 14, 'bold'))
            temp_text.place(relx=0.05, rely=0.1)
            frame = tkinter.Frame(temp_frame, relief='groove', width=1215, height=585, bg='red')
            frame.place(relx=0.05, rely=0.15)
            list_box = tkinter.Listbox(temp_frame, bd=3, font=('FangSong', 14), fg='orange', highlightthickness=5,
                                       highlightcolor='orange', width=60, height=15, selectmode=tkinter.EXTENDED)
            list_box.place(relx=0.05, rely=0.15)
            scr = tkinter.Scrollbar(frame, orient='vertical')
            scr.place(relwidth=0.05, relheight=1, relx=0.95, rely=0)
            list_box.configure(yscrollcommand=scr.set)
            scr.configure(command=list_box.yview)

            # 显示物品
            possession = self.SearchPossession()
            for p in possession:
                show_info = [p[0]] + p[3:]
                list_box.insert(tkinter.END, '  '.join(show_info))

            # 布局按钮
            confirm_button = tkinter.Button(temp_frame, text='删除本条记录', font=('FangSong', 12, 'bold'), bd=5,
                                            relief='groove', bg='orange', fg='white',
                                            activeforeground='orange')
            confirm_button.configure(command=delete_possession)
            confirm_button.place(relx=0.05, rely=0.72)

        def print_items():
            def click_type_list(event):
                # 获取选中物品种类的属性和值列表
                select_type = list_box.get(list_box.curselection())
                items = self.GetItems(select_type)
                # 布局物品属性表格
                temp_text2 = tkinter.Label(temp_frame, text='该类物品清单', font=('FangSong', 14, 'bold'))
                temp_text2.place(relx=0.32, rely=0.1)
                frame_2 = tkinter.Frame(temp_frame, relief='groove', width=900, height=715, bg='red')
                frame_2.place(relx=0.32, rely=0.15)
                cols = items[0]
                ybar = tkinter.Scrollbar(frame_2, orient='vertical')  # 竖直滚动条
                style_head = ttk.Style()
                style_head.configure("Treeview.Heading", font=('FangSong', 12), rowheight=50)
                style_head.configure("Treeview", font=('FangSong', 10), rowheight=40)
                tree = Treeview(temp_frame, show='headings', columns=cols, yscrollcommand=ybar.set, height=17,
                                selectmode='browse')
                ybar['command'] = tree.yview
                # 表头设置
                for col in cols:
                    tree.heading(col, text=col)  # 行标题
                    tree.column(col, width=int(860/len(cols)), anchor='center')  # 每一行的宽度,'w'意思为靠右

                tree.place(relx=0.32, rely=0.15)
                ybar.place(relwidth=0.05, relheight=1, relx=0.95, rely=0)
                for item in items[1:]:
                    tree.insert("", "end", values=item)

            # 删除temp_frame上的全部组件
            for widget in temp_frame.winfo_children():
                if widget != frame_bg:
                    widget.destroy()
            # 查看物品类别的部分
            temp_text1 = tkinter.Label(temp_frame, text='选择物品种类', font=('FangSong', 14, 'bold'))
            temp_text1.place(relx=0.02, rely=0.1)
            frame_1 = tkinter.Frame(temp_frame, relief='groove', width=400, height=720, bg='red')
            frame_1.place(relx=0.02, rely=0.15)
            list_box = tkinter.Listbox(temp_frame, bd=3, font=('Times New Romans', 16), fg='orange',
                                       highlightthickness=5, highlightcolor='orange', width=16, height=16, exportselection=False)
            list_box.place(relx=0.02, rely=0.15)
            scr = tkinter.Scrollbar(frame_1, orient='vertical')
            scr.place(relwidth=0.1, relheight=1, relx=0.9, rely=0)
            list_box.configure(yscrollcommand=scr.set)
            scr.configure(command=list_box.yview)

            list_box.bind('<<ListboxSelect>>', click_type_list)
            type_list = self.GetItemTypeList()
            for item_type in type_list:
                list_box.insert(tkinter.END, item_type)

        def search_item():
            def search_by_key():
                if len(list_box.curselection()) == 0:
                    tkinter.messagebox.showwarning(title='查询失败', message='您还没有选择物品种类！')
                    return
                select_type = list_box.get(list_box.curselection())
                key_word = keyword_entry.get()
                if key_word == '':
                    tkinter.messagebox.showwarning(title='查询失败', message='您还没有输入关键字！')

                is_successful, eligible_items = self.SearchByKeyword(select_type, key_word)
                if not is_successful:
                    tkinter.messagebox.showinfo(title='查找失败', message='未找到匹配项！')
                    return

                # 布局物品属性表格
                frame_2 = tkinter.Frame(temp_frame, relief='groove', width=900, height=635, bg='red')
                frame_2.place(relx=0.32, rely=0.23)
                cols = self.GetNeededAttributes(select_type)
                ybar = tkinter.Scrollbar(frame_2, orient='vertical')  # 竖直滚动条
                style_head = ttk.Style()
                style_head.configure("Treeview.Heading", font=('FangSong', 12), rowheight=50)
                style_head.configure("Treeview", font=('FangSong', 10), rowheight=40)
                tree = Treeview(temp_frame, show='headings', columns=cols, yscrollcommand=ybar.set, height=15,
                                selectmode='browse')
                ybar['command'] = tree.yview
                # 表头设置
                for col in cols:
                    tree.heading(col, text=col)  # 行标题
                    tree.column(col, width=int(860 / len(cols)), anchor='center')  # 每一行的宽度,'w'意思为靠右

                tree.place(relx=0.32, rely=0.23)
                ybar.place(relwidth=0.05, relheight=1, relx=0.95, rely=0)
                for item in eligible_items:
                    tree.insert("", "end", values=item)

            # 删除temp_frame上的全部组件
            for widget in temp_frame.winfo_children():
                if widget != frame_bg:
                    widget.destroy()
            # 选择物品类别的部分
            temp_text1 = tkinter.Label(temp_frame, text='选择物品种类', font=('FangSong', 14, 'bold'))
            temp_text1.place(relx=0.02, rely=0.1)
            frame_1 = tkinter.Frame(temp_frame, relief='groove', width=400, height=720, bg='red')
            frame_1.place(relx=0.02, rely=0.15)
            list_box = tkinter.Listbox(temp_frame, bd=3, font=('Times New Romans', 16), fg='orange',
                                       highlightthickness=5, highlightcolor='orange', width=16, height=16,
                                       exportselection=False)
            list_box.place(relx=0.02, rely=0.15)
            scr = tkinter.Scrollbar(frame_1, orient='vertical')
            scr.place(relwidth=0.1, relheight=1, relx=0.9, rely=0)
            list_box.configure(yscrollcommand=scr.set)
            scr.configure(command=list_box.yview)
            type_list = self.GetItemTypeList()
            for item_type in type_list:
                list_box.insert(tkinter.END, item_type)

            # 输入关键字部分
            temp_text2 = tkinter.Label(temp_frame, text='关键字', font=('FangSong', 14, 'bold'))
            temp_text2.place(relx=0.32, rely=0.1)
            keyword_entry = tkinter.Entry(temp_frame, font=('Times New Romans', 16), bd=3,
                                                highlightcolor='orange', highlightthickness=5, fg='orange')
            keyword_entry.place(relx=0.32, rely=0.15)
            keyword_search_button = tkinter.Button(temp_frame, text='查找', font=('FangSong', 10, 'bold'), bd=5,
                                        relief='groove', bg='orange', fg='white', activeforeground='orange')
            keyword_search_button.place(relx=0.64, rely=0.156)
            keyword_search_button.configure(command=search_by_key)

        user_operate_win = tkinter.Tk()
        user_operate_win.resizable(False, False)
        # 调用api设置成由应用程序缩放
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        # 调用api获得当前的缩放因子
        ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        user_operate_win.tk.call('tk', 'scaling', ScaleFactor / 75)

        width = 1920
        height = 1080
        screenwidth = user_operate_win.winfo_screenwidth()
        screenheight = user_operate_win.winfo_screenheight()
        user_operate_win.geometry('%dx%d+%d+%d' % (width, height, screenwidth - width / 2, screenheight - height / 2))
        user_operate_win.title('用户操作界面')

        # 背景
        canvas = tkinter.Canvas(user_operate_win, width=width, height=height, bd=0, highlightthickness=0, bg='white')
        canvas.place(x=0, y=0)
        img = Image.open('images/界面壁纸半透明.png').resize((width, height))
        img = ImageTk.PhotoImage(img)
        canvas.create_image(width / 2, height / 2, image=img)

        # 按钮
        add_button_image = Image.open('images/添加物品信息按钮.png').resize((214, 60))
        add_button_image = ImageTk.PhotoImage(add_button_image)
        add_button = tkinter.Button(user_operate_win, image=add_button_image, bd=0, cursor='hand2')
        add_button.configure(command=add_item)
        add_button.place(x=115, y=250)

        delete_button_image = Image.open('images/删除物品信息按钮.png').resize((214, 60))
        delete_button_image = ImageTk.PhotoImage(delete_button_image)
        delete_button = tkinter.Button(user_operate_win, image=delete_button_image, bd=0, cursor='hand2')
        delete_button.configure(command=delete_item)
        delete_button.place(x=115, y=350)

        print_list_button_image = Image.open('images/显示物品列表按钮.png').resize((214, 60))
        print_list_button_image = ImageTk.PhotoImage(print_list_button_image)
        print_list_button = tkinter.Button(user_operate_win, image=print_list_button_image, bd=0,
                                                      cursor='hand2')
        print_list_button.configure(command=print_items)
        print_list_button.place(x=115, y=450)

        search_button_image = Image.open('images/查找物品信息按钮.png').resize((214, 60))
        search_button_image = ImageTk.PhotoImage(search_button_image)
        search_button = tkinter.Button(user_operate_win, image=search_button_image, bd=0, cursor='hand2')
        search_button.configure(command=search_item)
        search_button.place(x=115, y=550)

        # 一个框架，用作所有临时控件的父容器，便于删除临时控件
        temp_width = 1483
        temp_height = 1080
        temp_frame = tkinter.Frame(user_operate_win, relief='flat', bg='white', width=temp_width, height=temp_height)
        temp_frame.place(x=437, y=0)
        frame_bg_img = Image.open('images/Frame背景.png').resize((temp_width, temp_height))
        frame_bg_img = ImageTk.PhotoImage(frame_bg_img)
        frame_bg = tkinter.Label(temp_frame, image=frame_bg_img)
        frame_bg.place(x=0, y=0)

        user_operate_win.mainloop()

    def GetNeededAttributes(self, type_name):
        with open(type_name + '.csv', "r", encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            lines = list(reader)
            return lines[0]

    def AddItemToCSV(self, type_name, values):
        with open(type_name + '.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([self.account] + values)

    def SearchPossession(self):
        type_list = []
        with open("Type_Of_Goods.txt", "r", encoding='utf-8') as f:
            for line in f:
                type_list.append(line.split(';')[0])
        possession = []
        for tp in type_list:
            with open(tp + '.csv', "r", encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                lines = list(reader)
                line_count = 0
                for line in lines[1:]:
                    if line[0] == self.account:
                        possession.append([tp, line_count] + line)
                    line_count += 1
        return possession

    def DelRecordsAccordingToFilenameAndRow(self, del_records):
        del_records.sort(key=itemgetter(1), reverse=True)
        for del_record in del_records:
            filename = del_record[0] + '.csv'
            row = del_record[1]
            data = pd.read_csv(filename, encoding='utf-8')
            data_after_del = data.drop(row)
            data_after_del.to_csv(filename, encoding='utf-8', index=False)

    def GetItems(self, select_type):
        with open(select_type + '.csv', "r", newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            lines = list(reader)
        return lines

    def SearchByKeyword(self, select_type, keyword):
        data = pd.read_csv(select_type + '.csv', encoding='utf-8', index_col=None)
        df = pd.DataFrame(data)
        eligible_items = df[df['上传用户'].str.contains(keyword) | df['物品说明'].str.contains(keyword)]
        if eligible_items.empty:
            return False, None
        return True, eligible_items.values.tolist()


if __name__ == '__main__':
    regular_user = RegularUser('zhangming', '123')
    regular_user.user_operation_interface()
    # print(regular_user.address)
    # print(regular_user.name)
    # print(regular_user.tele)

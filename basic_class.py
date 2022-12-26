# -*- coding: utf-8 -*-
import csv


class User():
    """定义一个用户的基类，是普通用户和管理员共有的部分"""
    def __init__(self, account, password):
        self.account = account
        self.password = password

    # 返回现有物品种类的列表
    def GetItemTypeList(self):
        with open("Type_Of_Goods.txt", "r", encoding='utf-8') as f:
            item_type_list = []
            for line in f:
                item_type_list.append(line.split(';')[0])
            return item_type_list


if __name__ == '__main__':
    print(item_f.GetNeededAttributes())

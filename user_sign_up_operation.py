# -*- coding: utf-8 -*-

import pandas as pd
from csv import writer

def CheckIfUserExist(user_account):
    """检查账户是否存在，用户注册"时使用"""
    account_info = pd.read_csv('User_Account.csv', encoding='gb2312')
    accounts = account_info['账号'].values.tolist()
    requires = pd.read_csv('Sign_Up_Request.csv', encoding='gb2312')
    required_accounts = requires['账号'].values.tolist()
    if user_account in accounts:
        return True, '账号已存在,请更换账户名！'
    if user_account in required_accounts:
        return True, '账号已被注册，请更换账户名！'
    return False, None

# 接受用户的注册请求
def Receive_Sign_Up_Require(user_info):
    with open('Sign_Up_Request.csv', 'a', newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(user_info)
        f_object.close()
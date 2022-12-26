# -*- coding: utf-8 -*-

import pandas as pd


def CheckUserIdentity(user_account, user_password):
    """检查传入的管理员账号和密码，并返回对应的信息"""
    account_info = pd.read_csv('User_Account.csv', encoding='gb2312')
    accounts = account_info['账号'].values.tolist()
    if user_account not in accounts:
        message = '账号不存在，请检查!'
        return False, message
    else:
        i = accounts.index(user_account)
        if account_info.iloc[i, 1] == user_password:
            message = '登录成功!'
            return True, message
        else:
            message = '密码错误，请检查!'
            return False, message
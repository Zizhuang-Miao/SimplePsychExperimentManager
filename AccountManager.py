# 对用户的账户进行管理
# 可进行的操作包括: 新建账户, 删除账户, 修改密码, 增加实验, 改变用户权限, 删除用户等
# 就某一实验而言, 被试的状态为0/1/2, 分别代表: 无权限做该实验/有权限做但仍未做该实验/已经完成该实验
# 作者: 汪肇兴, 1700017741
# 2020-05-08

import pandas as pd
import os
import easygui

# 打开'用户信息.csv', 将数据写入dataframe, 返回该dataframe
def Read():
    df = pd.read_csv('用户信息.csv')
    return df

# 将含有新的用户信息的dataframe写入'用户信息.csv'
def Write(df):
    df.to_csv('用户信息.csv', index=False)

# 将被试信息读取出来
def ReadParticipants():
    df = pd.read_csv('用户信息.csv')
    df = df[df['用户属性'] == '被试']
    return df

# 将仅被试信息的dataframe写入'用户信息.csv'
def WriteParticipants(df_p):
    df = pd.read_csv('用户信息.csv')
    df = df[df['用户属性'] == '主试']
    df = df.append(df_p)
    df.to_csv('用户信息.csv', index=False)

# 用于确认用户名存在, 否则抛出异常
def AssertUserExist(df, user_name):
    if user_name not in df['用户名'].values:
        raise ValueError(str('您输入的用户名 ' + user_name + ' 不存在'))

# 用于确认用户名不存在, 否则抛出异常
def AssertUserNotExist(df, user_name):
    if user_name in df['用户名'].values:
        raise ValueError(str('您输入的用户名 ' + user_name + ' 已存在'))

# 用于确认实验名存在, 否则抛出异常
def AssertExperimentExist(df, experiment_name):
    if experiment_name == '用户名' or experiment_name == '密码' or experiment_name == '用户属性':
        raise ValueError(str('您输入的实验名 ' + experiment_name + '不合法'))
    if experiment_name not in df.columns:
        raise ValueError(str('您输入的实验 ' + experiment_name + ' 不存在'))

# 用于确认实验名不存在, 否则抛出异常
def AssertExperimenNotExist(df, experiment_name):
    if experiment_name == '用户名' or experiment_name == '密码' or experiment_name == '用户属性':
        raise ValueError(str('您输入的实验名 ' + experiment_name + '不合法'))
    if experiment_name in df.columns:
        raise ValueError(str('您输入的实验 ' + experiment_name + ' 已存在'))

# 用于确认实验文件是否存在于Experiment文件夹中
def isExpExist(expname):
    curdir = os.getcwd()
    os.chdir(curdir+'\\Experiments')
    if expname not in os.listdir():  
        easygui.msgbox('请先将同名实验文件放入Experiments文件夹', title='错误', ok_button='确认')
        os.chdir(curdir)
        return 0
    os.chdir(curdir)
    return 1

# 创建新的主试账号
def NewExperimenterAccount(user_name, password):
    df = Read()
    AssertUserNotExist(df, user_name)
    temp_list = [user_name, password, '主试']
    for i in range(len(df.columns)-3):
        temp_list.append(0)
    s = pd.Series(temp_list, index=df.columns)
    df = df.append(s, ignore_index=True)
    Write(df)

# 创建新的被试账号
def NewParticipantAccount(user_name, password):
    df = Read()
    AssertUserNotExist(df, user_name)
    temp_list = [user_name, password, '被试']
    for i in range(len(df.columns)-3):
        temp_list.append(0)
    s = pd.Series(temp_list, index=df.columns)
    df = df.append(s, ignore_index=True)
    Write(df)

# 改变已有账号的密码
def ChangeAccountDetails(user_name, new_user_name, original_password, new_password):
    df = Read()
    AssertUserExist(df, user_name)
    if original_password != df.loc[df['用户名'] == user_name, '密码'].item():
        raise ValueError(str('您输入的原密码有误'))
    df.loc[df['用户名'] == user_name, ['密码']] = new_password
    df.loc[df['用户名'] == user_name, ['用户名']] = new_user_name
    Write(df)

# 删除已有的账号
def DeleteAccount(user_name):
    df = Read()
    AssertUserExist(df, user_name)
    df = df[df['用户名'] != user_name]
    Write(df)

# 检查用户输入的用户名是否存在
def CheckUserName(user_name):
    df = Read()
    if user_name in df['用户名'].values:
        return True
    return False

# 检查用户输入的密码是否与用户名匹配
def CheckPassword(user_name, password):
    df = Read()
    AssertUserExist(df, user_name)
    if password == df.loc[df['用户名'] == user_name, '密码'].item():
        return True
    return False

# 检查用户属性, 如果为主试, 返回True, 否则返回False
def CheckRole(user_name):
    df = Read()
    AssertUserExist(df, user_name)
    if df.loc[df['用户名'] == user_name, '用户属性'].item() == '主试':
        return True
    elif df.loc[df['用户名'] == user_name, '用户属性'].item() == '被试':
        return False

# 在列表中增加实验
def NewExperiment(experiment_name):
    df = Read()
    AssertExperimenNotExist(df, experiment_name)
    df[experiment_name] = '0'
    Write(df)

# 在列表中删除原有实验
def DeleteExperiment(experiment_name):
    df = Read()
    AssertExperimentExist(df, experiment_name)
    df = df.drop(columns=[experiment_name])
    Write(df)

# 将某个被试对某一个实验的权限, 由无权限(0)改为有权限但仍未完成该实验(1)
def AddParticipantToExperiment(experiment_name, user_name):
    df = ReadParticipants()
    AssertUserExist(df, user_name)
    AssertExperimentExist(df, experiment_name)
    if df.loc[df['用户名'] == user_name, experiment_name].item() != 0:
        raise ValueError(str('已对用户 ' + user_name + ' 开放实验 ' + experiment_name + ' 的权限'))
    df.loc[df['用户名'] == user_name, experiment_name] = 1
    WriteParticipants(df)

# 将某个被试对某个实验的权限, 由有权限但仍未完成该实验(1)改为无权限(0)
def RemoveParticipantFromExperiment(experiment_name, user_name):
    df = ReadParticipants()
    AssertUserExist(df, user_name)
    AssertExperimentExist(df, experiment_name)
    if df.loc[df['用户名'] == user_name, experiment_name].item() == 0:
        raise ValueError(str('用户 ' + user_name + ' 对实验 ' + experiment_name + ' 无权限'))
    if df.loc[df['用户名'] == user_name, experiment_name].item() == 2:
        raise ValueError(str('用户 ' + user_name + ' 已完成实验 ' + experiment_name))
    df.loc[df['用户名'] == user_name, experiment_name] = 0
    WriteParticipants(df)



if __name__ == '__main__':
    NewParticipantAccount('beishi1', 'abc123')
    NewParticipantAccount('beishi2', 'abc123')
    NewParticipantAccount('beishi3', 'abc123')
    NewParticipantAccount('beishi4', 'abc123')
    NewParticipantAccount('beishi5', 'abc123')
    NewParticipantAccount('beishi6', 'abc123')
    NewParticipantAccount('beishi7', 'abc123')

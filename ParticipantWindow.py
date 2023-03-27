# 被试的窗口，主界面是被试有权限做但还没有做的实验，可对查看实验说明、运行实验
# 可以通过菜单栏按钮修改自己账户的信息
# 可以通过菜单栏按钮返回登陆界面或退出程序
# 作者: 汪肇兴, 1700017741
# 2020-05-08
# 作者：苗子壮，1700017787
# 2020-05-23
# 后期调整：张天炜,1800017745
# 2020-06-01

import tkinter as tk
import easygui
import pandas as pd
import AccountManager as AM
import csv
import ScrollableFrame as sc

# 导入现有的所有实验模块
ExpInfo = pd.read_csv('实验信息.csv')
ExpClass = {}  #保存实验名称及其中的类
for each in ExpInfo['实验名称'].values:
    class_dict = {}
    exec("from Experiments."+each+" import class_dict")  #class_dict变量保存了每个实验中定义的类
    ExpClass[each] = list(class_dict.keys())
    for i in ExpClass[each]:
        exec("from Experiments."+each+" import "+i)

# 被试界面的函数
def PW(user_name, assembles, root):
    
    def ClearPage():
        if len(assembles) > 1:
            for j in range(1, len(assembles)):
                for a in assembles[j]:
                    a.grid_remove()
                assembles[j] = []

    # 呈现默认的主界面, 暂时没有内容
    def BackToMain():
        ClearPage()
        while len(assembles) < 2:
            assembles.append([])
        Welcome = tk.Label(root, text='欢迎登陆简单心理实验系统！', font=('黑体', 20),justify='center')
        Welcome.grid(row=0, columnspan=5, pady=10)
        assembles[1].append(Welcome)

        # 检查实验是否存在
        def CheckExp(expname):
            if expname not in ExpInfo['实验名称'].values:
                easygui.msgbox(msg='该实验不存在或名称有误，请检查！')
                return 0
            else: return 1

        #运行实验
        def runexp():
            global ExpInfo, ExpClass
            nam = ExpList.get(tk.ACTIVE)
            if CheckExp(nam) and AM.isExpExist(nam+'.py'):
                execstr = 'x='+ExpClass[nam][-1]+'('
                rowdf = ExpInfo[ExpInfo['实验名称']==nam]
                para = ''
                for i in range(1,5):
                    col = '参数'+str(i)
                    if not pd.isnull(rowdf[col]).values[0]:  #该参数不为空
                        para = para+str(float(rowdf[col]))+','
                    else: break
                execstr = execstr + para + ')'
                # 记录用户信息和实验信息
                filename = nam+'实验结果.csv'
                csvfile = open(filename,'a',newline='')
                writer=csv.writer(csvfile, delimiter=',')
                writer.writerow([user_name, para])
                csvfile.close()
                # 更改权限，并将列表中的实验删除
                df = AM.Read()
                df.loc[df['用户名'] == user_name, nam] = '2'
                AM.Write(df)
                ExpList.delete(tk.ACTIVE)
                # 开始实验
                exec(execstr)
                
        ExpListName = tk.Label(root, text='实验列表：', font=('黑体', 12), justify='left')
        ExpListName.grid(row=1, column=0, pady=10)
        assembles[1].append(ExpListName)

        # 带滚动条的frame，用于显示实验列表
        ListFrame = sc.ScrollableFrame(root)
        ListFrame.grid(row=2, rowspan=10, columnspan=4)
        # 实验列表
        ExpList = tk.Listbox(ListFrame.scrollable_frame, height=20, width=60)
        df = AM.Read()
        for each in ExpInfo['实验名称'].values:
            if df.loc[df['用户名'] == user_name, each].item() == 1:
                ExpList.insert(tk.END, each)
        ExpList.grid(row=0, column=0)
        assembles[1].append(ListFrame)
        assembles[1].append(ExpList)

        #运行实验按钮
        RunExpButton = tk.Button(root, text='开始实验', width=15, command=runexp)
        RunExpButton.grid(row=4, column=4)
        assembles[1].append(RunExpButton)
        #退出
        exitButton = tk.Button(root, text='退出程序', width=15, command=Exit)
        exitButton.grid(row=9, column=4)
        assembles[1].append(exitButton)

    # 被试仅能修改本账户的密码
    def ChangeAccountDetails():

        # 检查用户输入, 若用户输入有效, 更新本账户的信息
        def UpdateDetails():

            # 当用户输入有误时, 清空用户输入
            def ClearEntries():
                v3.set('')
                v4.set('')
                v5.set('')

            old_password = e3.get()
            new_password = e4.get()
            new_password2 = e5.get()
            if AM.CheckPassword(user_name, old_password) == False:
                easygui.msgbox('当前密码错误, 请重新输入', title='错误', ok_button='确认')
                ClearEntries()
            elif len(new_password) < 6:
                easygui.msgbox('新密码长度至少为6位, 请重新输入', title='错误', ok_button='确认')
                ClearEntries()
            elif new_password != new_password2:
                easygui.msgbox('新密码输入不一致, 请重新输入', title='错误', ok_button='确认')
                ClearEntries()
            else:
                AM.ChangeAccountDetails(user_name, user_name, old_password, new_password)
                easygui.msgbox('账户信息已更新', title='提示', ok_button='确认')
                ClearPage()
                ChangeAccountDetails()


        # 若当前界面右侧有组件, 清空界面右边的组件
        ClearPage()

        # 当前用户名的显示栏
        l1 = tk.Label(root, text="当前用户名为 "+user_name)
        l1.grid(row=1, column=1, columnspan=2)
        if len(assembles) < 2:
            assembles.append([])
        (assembles[1]).append(l1)

        # 当前密码的输入栏
        l3 = tk.Label(root, text='输入当前密码:')
        l3.grid(row=2, column=1)
        (assembles[1]).append(l3)
        v3 = tk.StringVar()
        e3 = tk.Entry(root, textvariable=v3, show='*')
        e3.grid(row=2, column=2, padx=20, pady=20)
        (assembles[1]).append(e3)

        # 新密码的输入栏
        l4 = tk.Label(root, text='输入新密码:')
        l4.grid(row=3, column=1)
        (assembles[1]).append(l4)
        v4 = tk.StringVar()
        e4 = tk.Entry(root, textvariable=v4, show='*')
        e4.grid(row=3, column=2, padx=20, pady=20)
        (assembles[1]).append(e4)

        # 新密码的确认栏
        l5 = tk.Label(root, text='确认新密码:')
        l5.grid(row=4, column=1)
        (assembles[1]).append(l5)
        v5 = tk.StringVar()
        e5 = tk.Entry(root, textvariable=v5, show='*')
        e5.grid(row=4, column=2, padx=20, pady=20)
        (assembles[1]).append(e5)

        # '确认'按钮
        confirm_button = tk.Button(root, text='确认', command=UpdateDetails)
        confirm_button.grid(row=5, column=1, padx=20, pady=20)
        (assembles[1]).append(confirm_button)

        # '返回主界面'按钮
        back_to_main_button = tk.Button(root, text='返回主界面', command=BackToMain)
        back_to_main_button.grid(row=5, column=2, padx=20, pady=20)
        (assembles[1]).append(back_to_main_button)

    # 返回登录界面
    def BackToSignIn():
        from MainProgram import SignIn
        emptyMenu = tk.Menu(root)
        root.config(menu=emptyMenu)
        if easygui.boolbox('是否确认返回登录界面?', '返回登录界面', ['是', '否']) == True:
            ClearPage()
            for i in assembles[0]:
                i.grid_remove()
            SignIn(root)

    # 退出程序
    def Exit():
        if easygui.boolbox('是否确认退出程序?', '退出程序', ['是', '否']) == True:
            root.destroy()

    # 界面大小设置
    root.geometry('520x410+400+100')
    assembles = []  # 组件的列表, 用于显示和删除组件
    assembles.append([])
    BackToMain()

    # 下拉菜单'编辑账户信息'
    # 其中包括选项 '修改本账户信息'/'修改被试账户实验权限'/'增加/删除被试账户'
    MenuBar = tk.Menu(root)
    EditAccount = tk.Menu(MenuBar, tearoff=False)
    EditAccount.add_command(label='修改本账户信息', command=ChangeAccountDetails)
    MenuBar.add_cascade(label='编辑账户信息', menu=EditAccount)

    # 下拉菜单'返回/退出'
    # 其中包括选项 '返回登录界面'/'退出程序'
    BackOrExit = tk.Menu(MenuBar, tearoff=False)
    BackOrExit.add_command(label='返回登录界面', command=BackToSignIn)
    BackOrExit.add_command(label='退出程序', command=Exit)
    MenuBar.add_cascade(label='返回/退出', menu=BackOrExit)
    root.config(menu=MenuBar)
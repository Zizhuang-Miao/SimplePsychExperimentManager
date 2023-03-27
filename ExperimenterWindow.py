# 主试的窗口，主界面是现有实验列表，可对实验进行查看说明、设置参数、添加、删除、运行的操作
# 可以通过菜单栏按钮修改自己账户的信息、管理被试账户的信息、设置被试的实验权限
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

# 调用的实验者界面主函数
def EW(user_name, assembles, root):
    
    # 清空界面右侧的组件, 用于刷新界面
    def ClearPage():
        if len(assembles) > 1:
            for j in range(1, len(assembles)):
                for a in assembles[j]:
                    a.grid_remove()
                assembles[j] = []
    
    # 呈现主界面
    def BackToMain():
        ClearPage()
        root.geometry('520x410+200+100')
        while len(assembles) < 2:
            assembles.append([])
        Welcome = tk.Label(root, text='欢迎登陆简单心理实验系统！', font=('黑体', 20), justify='center')
        Welcome.grid(row=0, columnspan=5, pady=10)
        assembles[1].append(Welcome)

        # 检查实验是否存在
        def CheckExp(expname):
            if expname not in ExpInfo['实验名称'].values:
                easygui.msgbox(msg='该实验不存在或名称有误，请检查！')
                return 0
            else: return 1

        # 与按钮配对的函数
        # 显示实验说明函数
        def note():
            global ExpInfo
            if CheckExp(ExpList.get(tk.ACTIVE)):
                a = ExpInfo[ExpInfo['实验名称']==ExpList.get(tk.ACTIVE)].values
                tp = tk.Toplevel()
                tp.title('实验说明')
                tk.Message(tp, text=a[0][5]).pack()
            else: pass
        
        #设置参数
        def setpara():
            global ExpInfo
            nam = ExpList.get(tk.ACTIVE)
            if not AM.isExpExist(nam+'.py'): #检查实验文件夹中是否存在这个实验，不存在则跳出提醒、函数结束
                return
            a = ExpInfo['实验名称']==nam
            msg = '请给出您想更改的参数\n'+ExpInfo[a].values[0][5]
            title = '修改实验参数：'+nam
            fieldNames = ['参数1', '参数2', '参数3', '参数4']
            fieldValues = easygui.multenterbox(msg, title, fieldNames)
            if fieldValues != None:
                for i in range(1,len(fieldValues)+1):
                    para = '参数'+str(i)
                    ExpInfo.loc[a, para] = fieldValues[i-1]
                ExpInfo.to_csv('实验信息.csv', index=False)
                easygui.msgbox('修改成功！', title='提示', ok_button='确认')
        
        #添加实验
        # 添加的实验必须满足：实验可以通过生成一个类的实例化而运行，且实验类是文件中定义的所有类中的最后一个
        def addexp():
            global ExpInfo
            msg = '请给出您想添加的实验的信息'
            title = '新实验'
            fieldNames = ['实验名称', '参数1', '参数2', '参数3', '参数4', '实验说明']
            fieldValues = easygui.multenterbox(msg, title, fieldNames)
            if AM.isExpExist(fieldValues[0]+'.py'):
                new_exp = pd.DataFrame([fieldValues], columns=fieldNames)
                ExpInfo = pd.concat([ExpInfo, new_exp], ignore_index=True)
                ExpInfo.to_csv('实验信息.csv', index=False)
                AM.NewExperiment(fieldValues[0])
                ExpList.insert(tk.END, fieldValues[0])
        
        #删除实验
        def delexp():
            global ExpInfo
            nam = ExpList.get(tk.ACTIVE)
            if nam in ('阶梯法测量亮度绝对阈限', '平均误差法测量差别阈限', '速度知觉实验'):
                easygui.msgbox(msg='此实验为系统自带，不可以从列表中删除！')
                return
            if CheckExp(nam) and AM.isExpExist(nam+'.py'):
                if easygui.boolbox('您确定要从列表中删除该实验？', '删除实验', ['是', '否']) == True:
                    ExpInfo = ExpInfo[ExpInfo['实验名称'] != nam]
                    ExpInfo.to_csv('实验信息.csv', index=False)
                    AM.DeleteExperiment(nam)
                    ExpList.delete(tk.ACTIVE)
        
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
                # 记录用户信息
                filename = nam+'实验结果.csv'
                csvfile = open(filename,'a',newline='')
                writer=csv.writer(csvfile, delimiter=',')
                writer.writerow([user_name, para])
                csvfile.close()
                # 开始实验
                exec(execstr)
        
        #查看当前实验参数
        def viewexp():
            global ExpInfo
            a = ExpInfo['实验名称']==ExpList.get(tk.ACTIVE)
            v = ExpInfo[a].values[0]
            msg = ExpList.get(tk.ACTIVE)+'\n'+str(v[5])+'\n当前设置的参数为：'\
                +str(v[1])+', '+str(v[2])+', '+str(v[3])+', '+str(v[4])
            tp = tk.Toplevel()
            tp.title('实验参数')
            tk.Message(tp, text=msg).pack()


        ExpListName = tk.Label(root, text='现有实验列表：', font=('黑体', 12), justify='left')
        ExpListName.grid(row=1, column=0, pady=10)
        assembles[1].append(ExpListName)

        # 带滚动条的frame，用于显示实验列表
        ListFrame = sc.ScrollableFrame(root)
        ListFrame.grid(row=2, rowspan=12, columnspan=4)
        # 实验列表
        ExpList = tk.Listbox(ListFrame.scrollable_frame, height=20, width=60)
        for each in ExpInfo['实验名称'].values:
            ExpList.insert(tk.END, each)
        ExpList.grid(row=0, column=0)
        assembles[1].append(ListFrame)
        assembles[1].append(ExpList)

        # 对实验进行各种操作的按钮
        # 实验说明
        NoteButton = tk.Button(root, text='实验说明', width=15, command=note)
        NoteButton.grid(row=2, column=4)
        assembles[1].append(NoteButton)
        # 设置参数
        SetParaButton = tk.Button(root, text='设置参数', width=15, command=setpara)
        SetParaButton.grid(row=4, column=4)
        assembles[1].append(SetParaButton)
        #添加实验
        AddExpButton = tk.Button(root, text='添加实验', width=15, command=addexp)
        AddExpButton.grid(row=6, column=4)
        assembles[1].append(AddExpButton)
        #删除实验
        DelExpButton = tk.Button(root, text='删除实验', width=15, command=delexp)
        DelExpButton.grid(row=8, column=4)
        assembles[1].append(DelExpButton)
        #运行实验
        RunExpButton = tk.Button(root, text='运行实验', width=15, command=runexp)
        RunExpButton.grid(row=10, column=4)
        assembles[1].append(RunExpButton)
        #查看参数
        ViewExpButton = tk.Button(root, text='查看参数', width=15, command=viewexp)
        ViewExpButton.grid(row=12, column=4)
        assembles[1].append(ViewExpButton)

    # 修改本账户的用户名/密码
    def ChangeAccountDetails():
        # 检查用户输入, 若用户输入有效, 更新本账户的信息
        def UpdateDetails():

            # 当用户输入有误时, 清空用户输入
            def ClearEntries():
                v2.set(user_name)
                v3.set('')
                v4.set('')
                v5.set('')

            new_user_name = e2.get()
            old_password = e3.get()
            new_password = e4.get()
            new_password2 = e5.get()
            if new_user_name != user_name and AM.CheckUserName(new_user_name):
                easygui.msgbox('新用户名已存在', title='错误', ok_button='确认')
                ClearEntries()
            elif len(new_user_name) == 0:
                easygui.msgbox('输入用户名长度为0', title='错误', ok_button='确认')
                ClearEntries()
            elif AM.CheckPassword(user_name, old_password) == False:
                easygui.msgbox('当前密码错误, 请重新输入', title='错误', ok_button='确认')
                ClearEntries()
            elif len(new_password) < 6:
                easygui.msgbox('新密码长度至少为6位, 请重新输入', title='错误', ok_button='确认')
                ClearEntries()
            elif new_password != new_password2:
                easygui.msgbox('新密码输入不一致, 请重新输入', title='错误', ok_button='确认')
                ClearEntries()
            else:
                AM.ChangeAccountDetails(user_name, new_user_name, old_password, new_password)
                easygui.msgbox('账户信息已更新', title='提示', ok_button='确认')
                ClearPage()
                for i in assembles[0]:
                    i.grid_remove()
                EW(new_user_name, assembles, root)


        # 清空当前页面
        ClearPage()

        # 当前用户名的显示栏
        l1 = tk.Label(root, text="当前用户名为 "+user_name)
        l1.grid(row=1, column=1, columnspan=2)
        while len(assembles) < 2:
            assembles.append([])
        (assembles[1]).append(l1)

        # 新用户名的编辑栏
        l2 = tk.Label(root, text="输入新用户名:")
        l2.grid(row=2, column=1)
        (assembles[1]).append(l2)
        v2 = tk.StringVar(value=user_name)
        e2 = tk.Entry(root, textvariable=v2)
        e2.grid(row=2, column=2, padx=20, pady=20)
        (assembles[1]).append(e2)

        # 当前密码的输入栏
        l3 = tk.Label(root, text='输入当前密码:')
        l3.grid(row=3, column=1)
        (assembles[1]).append(l3)
        v3 = tk.StringVar()
        e3 = tk.Entry(root, textvariable=v3, show='*')
        e3.grid(row=3, column=2, padx=20, pady=20)
        (assembles[1]).append(e3)

        # 新密码的输入栏
        l4 = tk.Label(root, text='输入新密码:')
        l4.grid(row=4, column=1)
        (assembles[1]).append(l4)
        v4 = tk.StringVar()
        e4 = tk.Entry(root, textvariable=v4, show='*')
        e4.grid(row=4, column=2, padx=20, pady=20)
        (assembles[1]).append(e4)

        # 新密码的确认栏
        l5 = tk.Label(root, text='确认新密码:')
        l5.grid(row=5, column=1)
        (assembles[1]).append(l5)
        v5 = tk.StringVar()
        e5 = tk.Entry(root, textvariable=v5, show='*')
        e5.grid(row=5, column=2, padx=20, pady=20)
        (assembles[1]).append(e5)

        # '确认'按钮
        confirm_button = tk.Button(root, text='确认', command=UpdateDetails)
        confirm_button.grid(row=6, column=1, padx=20, pady=20)
        (assembles[1]).append(confirm_button)

        # '返回主界面'按钮
        back_to_main_button = tk.Button(root, text='返回主界面', command=BackToMain)
        back_to_main_button.grid(row=6, column=2, padx=20, pady=20)
        (assembles[1]).append(back_to_main_button)

    # 显示被试账户信息的编辑界面
    # 可以改变被试对实验的权限
    def EditParticipantAccounts():

        # 对所有未完成该实验的被试开放某个实验的权限
        def SelectAll(experiment_number):
            def ReturnFunction():
                if SelectAllTextVar[experiment_number-1].get() == '全部勾选':
                    for i in range(row_len):
                        if par_info_array[i][experiment_number] != 2 and (par_info_IntVar[i][experiment_number]).get() == 0:
                            (par_info_IntVar[i][experiment_number]).set(1)
                    SelectAllTextVar[experiment_number-1].set('取消全选')
                elif SelectAllTextVar[experiment_number-1].get() == '取消全选':
                    for i in range(row_len):
                        if par_info_array[i][experiment_number] != 2 and (par_info_IntVar[i][experiment_number]).get() == 1:
                            (par_info_IntVar[i][experiment_number]).set(0)
                    SelectAllTextVar[experiment_number-1].set('全部勾选')
            return ReturnFunction

        # 将更新后的用户信息存入'用户信息.csv', 将在用户按下'保存'按钮后触发
        def SaveInfo():
            for row in range(row_len):
                for col in range(col_len):
                    if col != 0 and par_info_array[row][col] != 2:
                        par_info_array[row][col] = par_info_IntVar[row][col].get()
                    elif col != 0 and par_info_array[row][col] == 2:
                        if par_info_IntVar[row][col].get() == 1:
                            par_info_array[row][col] = 1
            updated_par = pd.DataFrame(par_info_array, columns=par_info.columns)
            updated_par.insert(1, '密码', participants['密码'].values)
            updated_par.insert(2, '用户属性', participants['用户属性'].values)
            AM.WriteParticipants(updated_par)
            easygui.msgbox('已更新被试权限', title='提示', ok_button='确认')

            # 刷新界面
            ClearPage()
            EditParticipantAccounts()

        # 首先清空界面右侧组件
        ClearPage()

        # 将被试数据导入, 隐去密码和用户属性
        participants = AM.ReadParticipants()
        par_info = participants.drop(columns=['密码', '用户属性'])
        par_info_array = par_info.values

        # 显示首行标签(用户名+各个实验名称), 显示为TextLabel
        counter1 = 0
        header_text = []  # 首行标签的组件的列表
        if len(assembles) < 2:
            assembles.append([])
        for i in par_info.columns:
            header_text.append(tk.Label(root, text=i))
            (header_text[counter1]).grid(row=0, column=counter1 + 1)
            (assembles[1]).append(header_text[counter1])
            counter1 += 1

        # 显示用户信息, 若为用户名, 显示为TextLabel
        # 若为实验权限, 0/1显示为CheckButton, 2显示为'已完成实验'的TextLabel
        row_len = len(par_info_array)
        col_len = len(par_info_array[0])
        info_assembles = [[None] * col_len for _ in range(row_len)]  # 用户信息的组件的二维列表
        par_info_IntVar = [[None] * col_len for _ in range(row_len)]  # 用户实验权限勾选与否的二维列表
        for row in range(row_len):
            for col in range(col_len):

                # col == 0, 内容为用户名, 在窗口中显示为TextLabel
                if col == 0:
                    info_assembles[row][col] = tk.Label(root, text=par_info_array[row][col])
                    (info_assembles[row][col]).grid(row=row + 1, column=col + 1)
                    (assembles[1]).append(info_assembles[row][col])

                # 当前内容为2, 说明用户已完成实验, 显示为checkbutton, 并提供"再次赋权"选项
                elif par_info_array[row][col] == 2:
                    x = 0
                    par_info_IntVar[row][col] = tk.IntVar()
                    (par_info_IntVar[row][col]).set(x)
                    info_assembles[row][col] = tk.Checkbutton(root, text='已完成, 可再次授权', variable=par_info_IntVar[row][col])
                    (info_assembles[row][col]).grid(row=row + 1, column=col + 1)
                    (assembles[1]).append(info_assembles[row][col])

                # 当前内容为1/0, 说明用户仍未完成实验或无权限完成实验, 显示为CheckButton
                elif par_info_array[row][col] == 0 or par_info_array[row][col] == 1:
                    x = par_info_array[row][col]
                    par_info_IntVar[row][col] = tk.IntVar()
                    (par_info_IntVar[row][col]).set(x)
                    info_assembles[row][col] = tk.Checkbutton(root, text='授权', variable=par_info_IntVar[row][col])
                    (info_assembles[row][col]).grid(row=row + 1, column=col + 1)
                    (assembles[1]).append(info_assembles[row][col])

                # 用户信息中出现了异常
                else:
                    raise ValueError('用户信息有异常')

        # 一键全选按钮
        SelectAllButtons = [None] * (col_len-1)
        SelectAllTextVar = [None] * (col_len-1)
        for col in range(1,col_len):
            SelectAllTextVar[col-1] = tk.StringVar()
            flag = 0
            for i in range(row_len):
                if isinstance(par_info_IntVar[i][col], tk.IntVar) and par_info_IntVar[i][col].get() == 0:
                    flag = 1
            if flag == 1:
                SelectAllTextVar[col-1].set('全部勾选')
            else:
                SelectAllTextVar[col - 1].set('取消全选')
            SelectAllButtons[col-1] = tk.Button(root, textvariable=SelectAllTextVar[col-1], command=SelectAll(col))
            SelectAllButtons[col-1].grid(row=row_len+1, column=col+1)
            (assembles[1]).append(SelectAllButtons[col-1])


        # '保存'按钮, 按下后将更新的信息写入'用户信息.csv'
        savebtn = tk.Button(root, text='保存信息', command=SaveInfo)
        savebtn.grid(row=row_len+2, column=1, padx=20, pady=20)
        (assembles[1]).append(savebtn)

        # '返回主界面'按钮, 按下后清空当前界面右侧的编辑界面
        backtomainbtn = tk.Button(root, text='返回主界面', command=BackToMain)
        backtomainbtn.grid(row=row_len+2, column=2, padx=20, pady=20)
        (assembles[1]).append(backtomainbtn)


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

    # 显示增加新被试账户/删除现有被试账户的界面
    def AddOrDeleteParticipantAccounts():
        # 删除被试用户账号
        def DeleteParticipants():
            # 删除账号
            for i in range(len(par_username)):
                if ParCheckButtonIntVar[i].get() == 1:
                    AM.DeleteAccount(par_username[i])
            # 刷新界面
            BackToMain()
            AddOrDeleteParticipantAccounts()

        # 跳出弹窗, 让用户确认删除所选被试账号
        def ConfirmDeletion():
            if easygui.boolbox('是否确认删除所选被试账号?', '删除被试账号', ['是', '否']) == True:
                DeleteParticipants()

        # 添加新用户
        def AddNewParticipant():

            # 检查输入的用户名/密码是否合法, 若合法, 添加新用户
            if AM.CheckUserName(v2.get()):
                easygui.msgbox('新用户名已存在', title='错误', ok_button='确认')
                ClearPage()
                AddOrDeleteParticipantAccounts()
            elif len(v2.get()) == 0:
                easygui.msgbox('输入用户名长度为0', title='错误', ok_button='确认')
                ClearPage()
                AddOrDeleteParticipantAccounts()
            elif len(v3.get()) < 6:
                easygui.msgbox('新密码长度至少为6位, 请重新输入', title='错误', ok_button='确认')
                ClearPage()
                AddOrDeleteParticipantAccounts()
            else:
                AM.NewParticipantAccount(v2.get(), v3.get())
                easygui.msgbox('已添加新被试账户', title='提示', ok_button='确认')
                ClearPage()
                AddOrDeleteParticipantAccounts()

        # 若当前界面右侧有组件, 清空界面右边的组件
        ClearPage()
        root.geometry('600x550+200+50')

        # 显示所有被试用户名, 每个被试用户配一个checkbutton, 用于选择
        if len(assembles) == 1:
            assembles.append([])
        Title = tk.Label(root, text='被试名单')
        Title.grid(row=0, column=3, padx=20, pady=20)
        assembles[1].append(Title)
        participants = AM.ReadParticipants()
        par_info_array = participants.values
        par_username = []
        for i in par_info_array:
            par_username.append(i[0])
        ParCheckButtons = [None] * len(par_username)
        ParCheckButtonIntVar = [None] * len(par_username)
        for i in range(len(par_username)):
            ParCheckButtonIntVar[i] = tk.IntVar()
            ParCheckButtonIntVar[i].set(0)
            ParCheckButtons[i] = tk.Checkbutton(root, text=par_username[i], variable=ParCheckButtonIntVar[i])
            ParCheckButtons[i].grid(row=(i//5)+1, column=(i%5)+1, padx=20, pady=20)
            assembles[1].append(ParCheckButtons[i])

        # '删除' 按钮, 点击后被勾选的账户将被删除
        temp_row = ((len(par_username)-1)//5+1)
        DeleteParButton = tk.Button(root, text='删除被试账号', command=ConfirmDeletion)
        DeleteParButton.grid(row=temp_row+1, column=3, padx=20, pady=20)
        assembles[1].append(DeleteParButton)

        # 新用户名的编辑栏
        l2 = tk.Label(root, text="新被试用户名:")
        l2.grid(row=temp_row+2, column=1,columnspan=2, padx=20, pady=20)
        assembles[1].append(l2)
        v2 = tk.StringVar()
        e2 = tk.Entry(root, textvariable=v2)
        e2.grid(row=temp_row+2, column=3, columnspan=3, padx=20, pady=20)
        assembles[1].append(e2)

        # 当前密码的输入栏
        l3 = tk.Label(root, text='输入新被试用户密码:')
        l3.grid(row=temp_row+3, column=1,columnspan=2, padx=20, pady=20)
        assembles[1].append(l3)
        v3 = tk.StringVar(value='abc123')
        e3 = tk.Entry(root, textvariable=v3)
        e3.grid(row=temp_row+3, column=3, columnspan=3, padx=20, pady=20)
        assembles[1].append(e3)

        # '添加新用户'按钮, 点击后将添加新用户
        AddNewParButton = tk.Button(root, text='添加新被试账户', command=AddNewParticipant)
        AddNewParButton.grid(row=temp_row+4, column=2, columnspan=3, padx=20, pady=20)
        assembles[1].append(AddNewParButton)

        # '返回主界面'按钮, 按下后清空当前界面右侧的编辑界面
        backtomainbtn = tk.Button(root, text='返回主界面', command=BackToMain)
        backtomainbtn.grid(row=temp_row+5, column=2, columnspan=3, padx=20, pady=20)
        assembles[1].append(backtomainbtn)

    # 界面大小设置
    root.geometry('520x410+400+100')
    assembles = [] # 组件的列表, 用于显示和删除组件
    assembles.append([])
    BackToMain()

    # 下拉菜单'编辑账户信息'
    # 其中包括选项 '修改本账户信息'/'修改被试账户实验权限'/'增加/删除被试账户'
    MenuBar = tk.Menu(root)
    EditAccount = tk.Menu(MenuBar, tearoff=False)
    EditAccount.add_command(label='修改本账户信息', command=ChangeAccountDetails)
    EditAccount.add_command(label='修改被试账户实验权限', command=EditParticipantAccounts)
    EditAccount.add_command(label='增加/删除被试账户', command=AddOrDeleteParticipantAccounts)
    MenuBar.add_cascade(label='编辑账户信息', menu=EditAccount)

    # 下拉菜单'返回/退出'
    # 其中包括选项 '返回登录界面'/'退出程序'
    BackOrExit = tk.Menu(MenuBar, tearoff=False)
    BackOrExit.add_command(label='返回登录界面', command=BackToSignIn)
    BackOrExit.add_command(label='退出程序', command=Exit)
    MenuBar.add_cascade(label='返回/退出', menu=BackOrExit)
    root.config(menu=MenuBar)
# 主程序，包含登陆界面，通过模块调用被试和主试的窗口
# 运用tkinter等模块输出窗口
# 作者: 汪肇兴, 1700017741
# 2020-05-08
# 作者：苗子壮，1700017787
# 2020-05-23

import AccountManager as AM
import tkinter as tk
import easygui
import ExperimenterWindow
import ParticipantWindow

# 登录界面, 将在主程序中调用
def SignIn(root):

    # 当用户点击'登录'按钮后, 触发LogOn函数,
    # 检验输入是否有效, 用户名/密码是否匹配, 若匹配, 进入主试/被试界面
    def LogOn():
        user_name = e1.get()
        password = e2.get()
        if user_name == '':
            easygui.msgbox('用户名不可为空', title='错误', ok_button='确认')
        elif AM.CheckUserName(user_name):
            if AM.CheckPassword(user_name, password):
                for a in assembles[0]:  # 清空上一步的组件
                    a.grid_remove()
                if AM.CheckRole(user_name):
                    ExperimenterWindow.EW(user_name, assembles, root) # 调用主试界面的函数
                else:
                    ParticipantWindow.PW(user_name, assembles, root) # 调用被试界面的函数
            else:
                easygui.msgbox('密码错误, 请重新输入', title='错误', ok_button='确认')
                e2.delete(0,tk.END)
        else:
            easygui.msgbox('用户名不存在, 请再次尝试', title='错误', ok_button='确认')

    # 退出程序
    def Exit():
        root.destroy()

    root.title("心理实验程序")
    root.geometry('260x200')
    assembles = [] # 组件的列表, 用于显示和删除组件

    # 用户名的输入栏
    l1 = tk.Label(root, text="用户名:")
    l1.grid(row=1,column=0)
    assembles.append([l1])
    v1 = tk.StringVar()
    e1 = tk.Entry(root, textvariable=v1)
    e1.grid(row=1, column=1, padx=20, pady=20)
    assembles[0].append(e1)

    # 密码的输入栏
    l2 = tk.Label(root, text='密码:')
    l2.grid(row=2, column=0)
    assembles[0].append(l2)
    v2 = tk.StringVar()
    e2 = tk.Entry(root, textvariable=v2, show='*')
    e2.grid(row=2, column=1, padx=20, pady=20)
    assembles[0].append(e2)

    # 登录按钮
    b1 = tk.Button(root, text='登录', command=LogOn)
    b1.grid(row=3, column=0, padx=20, pady=20)
    assembles[0].append(b1)

    # 退出按钮
    b2 = tk.Button(root, text='退出程序', command=Exit)
    b2.grid(row=3, column=1, padx=20, pady=20)
    assembles[0].append(b2)

if __name__ == '__main__':
    root = tk.Tk()
    SignIn(root)
    root.mainloop()
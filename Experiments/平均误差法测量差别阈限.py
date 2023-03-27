#张天炜 2020-04

import tkinter as tk
import random as rd
import csv

class AveErr:
    #trial-试次数，hf_std标准刺激大小，由于窗口大小有限，因而相对固定
    def __init__(self,trials=30,hf_std=75):
        #input correction 1
        if trials<10 or trials%2==1:
            raise TypeError('Trials should be a positive even int(>=10)')
        self.trials=int(trials)
        #input correction 2
        if hf_std>100 or hf_std<50 :
            raise TypeError('half standard should be an int between 50 and 100')
        self.hf_std=int(hf_std)

        self.temphfsize=0   #调整中的方形大小
        self.counter=0      #计数器，记trial
        self.reslist=[]     #结果数据
        self.start()


    def start(self):
        self.root=tk.Tk()
        self.root.title('Experiment of JND')
        self.win=tk.Canvas(self.root,width=1440,height=810,background='black')
        self.lmx=360        #左侧中心横坐标
        self.my=405         #中纵坐标
        self.win.bind("<KeyPress-Return>",self.gen_trial)
        self.win.bind("<KeyPress-Down>",self.contr)
        self.win.bind("<KeyPress-Up>",self.expand)
        self.win.focus_set()
        self.win.create_text(720,50,text="Now you are to use Up/Down Arrow Key to adjust the size of a certain square",fill="white",font=('Times New Roman',20))#指导语
        self.win.create_text(720,100,text="until you think the size of both are equal.",fill="white",font=('Times New Roman',20))
        self.win.create_text(720,200,text="Up/Down helps you expand/contract the square respectively.",fill="white",font=('Times New Roman',20))
        self.win.create_text(720,300,text="And you are supposed to finish this task while fixing at the central point.",fill="white",font=('Times New Roman',20))
        self.win.create_text(720,400,text="If you've finished your adjustment,Press Enter to run the next trial.",fill="white",font=('Times New Roman',20))
        self.win.create_text(720,500,text="If you understand the instructions above,Press Enter to start.",fill="white",font=('Times New Roman',20))
        self.win.pack()
        
        tk.mainloop()

    def draw(self,hfsize,is_right=0,color="grey"):
        self.win.create_rectangle(0+720*is_right,0,720+720*is_right,810,fill="black")
        self.win.create_oval(715,400,725,410,fill="red")
        self.win.create_rectangle(self.lmx-hfsize+720*is_right,self.my-hfsize,self.lmx+hfsize+720*is_right,self.my+hfsize,fill=color)
        
    def gen_trial(self,event):
        temp=[self.temphfsize,self.hf_std]
        self.reslist.append(temp)
        self.counter+=1
        self.win.delete("all")#删除已有的画布对象以防卡顿
        if self.counter>self.trials:#如果试次达成，即跳出
            # 数据保存
            self.reslist = self.reslist[1:]
            csvfile = open('平均误差法测量差别阈限实验结果.csv', 'a', newline='')
            writer = csv.writer(csvfile, delimiter=',')
            for i in range(len(self.reslist)):
                writer.writerow(self.reslist[i])
            csvfile.close()
            self.root.quit()
            self.root.destroy()
        else:
            if rd.randint(1,2)==1:#比较刺激初始大小随机更大/小
                self.temphfsize=self.hf_std+rd.randint(20,50)
            else:
                self.temphfsize=self.hf_std-rd.randint(20,50)
            self.templr=rd.randint(0,1)
            if self.templr==0:#左右随机,如果结果为0，则把比较刺激画在左侧
                self.draw(self.temphfsize,0)
                self.draw(self.hf_std,1)
            else:
                self.draw(self.temphfsize,1)
                self.draw(self.hf_std,0)
        
    def contr(self,event):#比较刺激缩小
        if self.temphfsize>0:
            self.temphfsize-=1
        self.draw(self.temphfsize,self.templr)

    def expand(self,event):#比较刺激增大
        if self.temphfsize<150:
            self.temphfsize+=1
        self.draw(self.temphfsize,self.templr)

class_dict = {key: var for key, var in locals().items() if isinstance(var, type)}

if __name__=='__main__':
    x=AveErr()
    

        

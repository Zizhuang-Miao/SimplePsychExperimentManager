#张天炜 2020-04
#本实验具有一定的局限性，屏幕大小固定，速度类型限定为2，计时器有待优化
import tkinter as tk
import random as rd
import time
import datetime as dt
import csv

class MyTimer:
    def __init__(self):
        self.running=0
    #开始函数
    def start(self):
        self.bgtime=time.time()
        self.running=1

    #结束函数
    def stop(self):
        if self.running==1:
            self.edtime=time.time()
            self.running=0
            return self.edtime-self.bgtime
        else:
            print("haven't started yet")

    def check(self):
        if self.running==1:
            self.edtime=time.time()
            return self.edtime-self.bgtime
        else:
            print('error')


class SpeedPerception:
    #trial-试次数，应为12的倍数(上下左右里外x两速度)，sp1速度1，sp2速度2,percent运行起始遮挡百分比
    def __init__(self,trials=48,spd1=40,spd2=80,percent=0.5):
        #input correction
        if trials<8 or trials%8!=0:
            raise TypeError('Trials should be a positive even int(>=8) and dividable by 8')
        self.trials=int(trials)
        self.spd=[int(spd1),int(spd2)]
        if not isinstance(percent,float) or percent<0.2 or percent>0.8:
            raise TypeError('Percent should be a float between .2 and .8')
        self.percent=percent
        self.spdtype=2
        
        #generate random trials
        self.rest_trial=[]
        for i in range(8):
            self.rest_trial.append(self.trials//8)
        self.trial_list=[]
        for i in range(self.trials):
            temp=rd.randint(0,7)
            while self.rest_trial[temp]==0:
                temp=rd.randint(0,7)
            self.trial_list.append(temp)
            self.rest_trial[temp]-=1        #最终获得self.trial_list作为随机试次表
        #(self.trial_list)
        
        #other initialization
        self.counter=0      #计数器，记trial
        self.stop=0
        self.reslist=[]     #结果数据
        self.t=MyTimer()
        self.start()

    def start(self):
        self.root=tk.Tk()
        self.root.title('Experiment of SpeedPerception')
        self.win=tk.Canvas(self.root,width=1440,height=810,background='white')
        self.win.bind("<KeyPress-Return>",self.turn_trial)
        self.win.focus_set()
        self.win.create_text(720,100,text="Now there'll be two rectangles and a square moving between them at a constant speed.",fill="black",font=('Times New Roman',15))#指导语
        self.win.create_text(720,200,text="While moving from one side to the other,the square will disappear at a certain timepoint.",fill="black",font=('Times New Roman',15))
        self.win.create_text(720,300,text="But it is still moving at the same speed,and you need to guess when it arrives at the other side.",fill="black",font=('Times New Roman',15))
        self.win.create_text(720,400,text="If you think it arrives now,Press the Enter immediately.",fill="black",font=('Times New Roman',15))
        self.win.create_text(720,500,text="And you'll get 2 feedbacks,one is the square's current position,the other is how early(-)/late(+) your guess is.",fill="black",font=('Times New Roman',15))
        self.win.create_text(720,600,text="If you understand the instructions above,Press Enter to start.",fill="black",font=('Times New Roman',15))
        self.win.pack()
        tk.mainloop()


    def turn_trial(self,event):#试次切换，如试次数满，终止；否则显示当前方块位置、相对时间差、开始下一试次
        if self.counter!=0:
            self.stop=1#如还在运行中，终止
            self.get_position(self.trial_list[self.counter-1])
            self.feedback='%.3f' % (self.t.check()-580/self.tempspd)
            self.reslist.append([self.trial_list[self.counter-1]//self.spdtype,self.trial_list[self.counter-1]%self.spdtype,float(self.feedback)/(580/self.tempspd)])
            #记录当前运动方式代号，速度代号，和偏差时占实际到达时百分比
            self.win.create_rectangle(self.tempx1,self.tempy1,self.tempx2,self.tempy2,fill="red")#上试次运动位置反馈
            self.win.update()
            time.sleep(0.5)
            self.win.delete("all")
            self.win.create_text(720,405,text=self.feedback+'秒',fill="black",font=('Times New Roman',30))#上试次时间反馈
            self.win.update()
            time.sleep(1.5)
            self.stop=0
        self.counter+=1
        self.win.delete("all")#清屏

        if self.counter>self.trials:#如果试次数达成，即跳出
            #数据保存
            csvfile = open('速度知觉实验实验结果.csv', 'a', newline='')
            writer = csv.writer(csvfile, delimiter=',')
            for i in range(len(self.reslist)):
                writer.writerow(self.reslist[i])
            csvfile.close()
            self.win.destroy()
            self.root.quit()
            self.root.destroy()
        else:
            self.run(self.trial_list[self.counter-1])

    def get_position(self,typenum):#调整运动位置反馈的最终坐标
        if typenum//self.spdtype==0:
            self.tempx1+=self.t.check()*self.tempspd
            self.tempx2+=self.t.check()*self.tempspd
        elif typenum//self.spdtype==1:
            self.tempx1-=self.t.check()*self.tempspd
            self.tempx2-=self.t.check()*self.tempspd
        elif typenum//self.spdtype==2:
            self.tempy1+=self.t.check()*self.tempspd
            self.tempy2+=self.t.check()*self.tempspd
        elif typenum//self.spdtype==3:
            self.tempy1-=self.t.check()*self.tempspd
            self.tempy2-=self.t.check()*self.tempspd

    def delete_sft(self):#由于按键时刻是不确定的，因而中途切断的循环的后续步骤可能报错，但对程序运行没有影响
        try:            #借这三个函数来运行循环内的删除/绘图/更新，这三个函数只用于while循环(运动过程)中
            self.win.delete('sft')
        except:
            pass

    def cr_rec_sft(self,x1,y1,x2,y2):
        try:
            self.win.create_rectangle(x1,y1,x2,y2,fill="red",tag='sft')
        except:
            pass

    def update_sft(self):
        try:
            self.win.update()
        except:
            pass

    def run(self,typenum):#四类试次
        self.t.start()
        if typenum//self.spdtype==0:#(一般spdtype==2)即typenum = 0 or 1——代表由左向右，0和1分别代表速度self.spd[0],[1]
            self.win.create_rectangle(400,255,420,555,fill="black")#左右板
            self.win.create_rectangle(1020,255,1040,555,fill="black")
            self.tempx1=420;self.tempy1=395;self.tempx2=440;self.tempy2=415;self.tempspd=self.spd[typenum%self.spdtype]#滑块位置速度设定
            self.win.create_rectangle(self.tempx1,self.tempy1,self.tempx2,self.tempy2,fill="red",tag='sft')#滑块
            self.win.update()
            while self.t.check()<580*self.percent/self.tempspd:#移动法=
                self.update_sft()
                time.sleep(0.025)
                self.delete_sft()
                self.cr_rec_sft(self.tempx1+self.t.check()*self.tempspd,self.tempy1,self.tempx2+self.t.check()*self.tempspd,self.tempy2)
                if self.stop:
                    break
            self.delete_sft()
            
        elif typenum//self.spdtype==1:#typenum = 2 or 3,——右左代表速度同上
            self.win.create_rectangle(400,255,420,555,fill="black")
            self.win.create_rectangle(1020,255,1040,555,fill="black")
            self.tempx1=1000;self.tempy1=395;self.tempx2=1020;self.tempy2=415;self.tempspd=self.spd[typenum%self.spdtype]
            self.win.create_rectangle(self.tempx1,self.tempy1,self.tempx2,self.tempy2,fill="red",tag='sft')#滑块
            self.win.update()
            while self.t.check()<580*self.percent/self.tempspd:
                self.update_sft()
                time.sleep(0.025)
                self.delete_sft()
                self.cr_rec_sft(self.tempx1-self.t.check()*self.tempspd,self.tempy1,self.tempx2-self.t.check()*self.tempspd,self.tempy2)#向左运行，x坐标运算改为减法
                if self.stop:
                    break
            self.delete_sft()

        elif typenum//self.spdtype==2:#typenum = 4 or 5——上下
            self.win.create_rectangle(570,85,870,105,fill="black")#底顶板
            self.win.create_rectangle(570,705,870,725,fill="black")
            self.tempx1=710;self.tempy1=105;self.tempx2=730;self.tempy2=125;self.tempspd=self.spd[typenum%self.spdtype]
            self.win.create_rectangle(self.tempx1,self.tempy1,self.tempx2,self.tempy2,fill="red",tag='sft')
            self.win.update()
            while self.t.check()<580*self.percent/self.tempspd:#移动法
                self.update_sft()
                time.sleep(0.025)
                self.delete_sft()
                self.cr_rec_sft(self.tempx1,self.tempy1+self.t.check()*self.tempspd,self.tempx2,self.tempy2+self.t.check()*self.tempspd)
                if self.stop:
                    break
            self.delete_sft()

        elif typenum//self.spdtype==3:#typenum = 6 or 7——下上
            self.win.create_rectangle(570,85,870,105,fill="black")#底顶板
            self.win.create_rectangle(570,705,870,725,fill="black")
            self.tempx1=710;self.tempy1=685;self.tempx2=730;self.tempy2=705;self.tempspd=self.spd[typenum%self.spdtype]
            self.win.create_rectangle(self.tempx1,self.tempy1,self.tempx2,self.tempy2,fill="red",tag='sft')
            self.win.update()
            while self.t.check()<580*self.percent/self.tempspd:#移动法
                self.update_sft()
                time.sleep(0.025)
                self.delete_sft()
                self.cr_rec_sft(self.tempx1,self.tempy1-self.t.check()*self.tempspd,self.tempx2,self.tempy2-self.t.check()*self.tempspd)
                if self.stop:
                    break
            self.delete_sft()

class_dict = {key: var for key, var in locals().items() if isinstance(var, type)}

if __name__=='__main__':
    x=SpeedPerception()
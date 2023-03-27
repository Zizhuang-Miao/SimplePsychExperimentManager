# 苗子壮，2020-05

import matplotlib.pyplot as plt
import numpy as np
import csv

class Staircase:
    def __init__(self, startpoint=98, requisite=3, endrequisite=20):
        '''startpoint参数表示初始灰度，是[0, 255]内的整数，默认为98
        requisite参数表示阶梯法的下降条件，一般为2或3，默认为3，也可以是其它正整数
        endrequisite是实验结束需要的转折点数量，默认为20个'''
        self.startpoint = int(startpoint)
        #用一个9*9*3对角矩阵表示刺激，只有中央是非黑色的（即被试需要探查的方块）
        rgb_array = [[0,0,0] for i in range(9*9)]
        rgb_array[40] = [np.int32(startpoint)]*3
        self.stimu = np.array(rgb_array).reshape((9,9,3))

        self.requisite = int(requisite)
        self.endrequisite = int(endrequisite)
        self.fig, self.ax = plt.subplots(figsize=(4.8, 4.8))  #创建图像界面
        self.ax.text(0.5, 0.5, 
        '''Now you will see a square at the center of the canvas
        Press F if you can detect it, otherwise press J
        There is no right or wrong, 
        just make your judgement based on your own sense
        If you understand your task, press your mouse to start''', 
        ha='center', va='center', fontsize=9)  #指导语
        self.ax.set_axis_off()
        
        self.flag = 0                #记录是否有“看不到”的判断
        self.vis = 0                 #记录已经判断“能看到”的次数
        self.turn_count = 0          #记录已出现的转折点数，达到endrequisite时实验结束
        self.turn_point = []         #记录每个转折点的灰度值
        self.res = 0                 #记录结果

        def start(event):            #点击鼠标开始实验
            plt.cla()
            self.ax.imshow(self.stimu, aspect='equal', interpolation='nearest')
            self.ax.set_axis_off()
            plt.pause(0.05)

        def key_press(event):        #被试作出按键反应后的刺激亮度改变
            if self.turn_count < self.endrequisite:
                if event.key == 'f':     #被试报告看到了
                    if self.flag == 0 or self.vis==requisite-1:    
                        plt.cla()        #之前每一个刺激都看到了或连续看到的次数达到要求，调整亮度
                        if self.vis==requisite-1:
                            self.vis = 0
                            self.turn_count += 1
                            self.turn_point.append(self.stimu[4][4][0])
                        self.stimu[4][4] -= np.int32(5) if self.flag==0 else np.int32(3)
                                     #如果之前出现了没看到的情况，就将灰度减3，否则减5
                        self.ax.imshow(self.stimu, aspect='equal', interpolation='nearest')
                        self.ax.set_axis_off()
                        plt.pause(0.05)
                    else:                #之前连续看到的次数不足要求，只计数不调整亮度
                        self.vis += 1
                elif event.key=='j':     #被试报告未看到，调整亮度并重新计数
                    self.turn_point.append(self.stimu[4][4][0])
                    self.stimu[4][4] += np.int32(5) if self.flag==0 else np.int32(3)
                    if self.flag == 0: self.flag = 1
                    plt.cla()
                    self.vis = 0         
                    self.turn_count += 1
                    self.ax.imshow(self.stimu, aspect='equal', interpolation='nearest')
                    self.ax.set_axis_off()
                    plt.pause(0.05)
                if self.turn_count == self.endrequisite:    #实验结束
                    plt.cla()
                    self.res = np.mean(np.array(self.turn_point[self.endrequisite-4:self.endrequisite]))
                    self.result = self.turn_point + [float(self.res)]
                    #保存结果到一个csv文件中
                    csvfile = open('阶梯法测量亮度绝对阈限实验结果.csv','a',newline='')
                    writer=csv.writer(csvfile, delimiter=',')
                    writer.writerow(self.result)
                    csvfile.close()
                    info = ('Finish!\n Your threshold is about {:.2f} at acc of {:.4f}\n'
                    + 'Please press any key to exit\n Thank you!').format(float(self.res), 0.5**(1/self.requisite))
                    self.ax.text(0.5, 0.5, info, ha='center', va='center', fontsize=9)
                    self.ax.set_axis_off()
                    plt.pause(0.005)
            else:
                plt.close()
            
        self.fig.canvas.mpl_disconnect(self.fig.canvas.manager.key_press_handler_id)    #取消默认快捷键
        self.fig.canvas.mpl_connect('button_release_event', start)
        self.fig.canvas.mpl_connect('key_release_event', key_press)
        plt.show()

class_dict = {key: var for key, var in locals().items() if isinstance(var, type)}

if __name__ == '__main__':
    a = Staircase(255,3,10)
# -*- coding:utf-8 -*-
from tkinter import *
import tkinter as tk
import linecache
import codecs
import tkinter.messagebox as box
from src.TerminalMain import s_main


class Init:
    """初始化"""
    def __init__(self, root_frame):
        self.root_frame = root_frame
        self.root_frame.geometry('650x400')
        self.init = tk.Frame(self.root_frame, width=650, height=400)
        self.init.pack()
        self.max_exp_num = 0
        self.mode = 0
        label = tk.Label(self.init, text="四则运算生成器", font=('宋体', 30, 'bold'), fg='darkblue')
        label.place(x=180, y=50)

        label = tk.Label(self.init, text="请输入1000以内需要的题目数量:", font=('宋体', 10))
        label.place(x=40, y=150)
        label2 = tk.Label(self.init, text="请输入生成题目的类型编号:", font=('宋体', 10))
        label2.place(x=40, y=200)
        label3 = tk.Label(self.init, text="(1.整数四则运算 2.分数四则运算 3.分数带乘方运算)", font=('宋体', 9))
        label3.place(x=320, y=200)

        self.num_temp = tk.Entry(self.init, width=10, bd=3)
        self.num_temp.place(x=240, y=150)
        self.num_temp2 = tk.Entry(self.init, width=10, bd=3)
        self.num_temp2.place(x=240, y=200)
        button = tk.Button(self.init, text=u'开始答题', activebackground='blue', command=self.start_test, bd=10,
                           font=('宋体', 15, 'bold'))
        button.place(x=240, y=250)

    def start_test(self):
        """答题开始"""
        self.max_exp_num = eval(self.num_temp.get())
        self.mode = eval(self.num_temp2.get())
        if self.max_exp_num <= 0 or self.max_exp_num > 1000 or self.mode not in [1, 2, 3]:
            box.showerror(None, "输入错误，请重新输入!")
            self.init.destroy()
            Init(self.root_frame)
            return
        s_main(self.max_exp_num, self.mode)
        self.init.destroy()
        StartTest(self.root_frame)


class StartTest:
    """题目显示框架"""
    def __init__(self, root_frame):
        self.root_frame = root_frame
        self.current_num = 1
        self.correct_num = 0
        self.question_frame = tk.Frame(self.root_frame, width=650, height=400)
        self.question_frame.pack()
        self.ans_text = ''
        # fh = codecs.open('/res/expressions.txt', 'r', "GBK")
        # content = fh.read()
        # codecs.open('/res/expressions.txt', 'w', "UTF-8").write(content)

        q_text = linecache.getline('../res/expressions.txt', self.current_num)
        label = tk.Label(self.question_frame, text=q_text, font=('宋体', 20))
        label.place(x=100, y=100)
        self.ans = tk.Entry(self.question_frame, width=20, bd=5)
        self.ans.place(x=250, y=150)
        submit_button = tk.Button(self.question_frame, text=u'提交', font=('宋体', 10), bd=5, command=self.submit)
        submit_button.place(x=150, y=200)
        next_pro_button = tk.Button(self.question_frame, text=u'下一题', font=('宋体', 10), bd=5, command=self.next_problem)
        next_pro_button.place(x=270, y=200)
        quit_button = tk.Button(self.question_frame, text=u'退出并显示', font=('宋体', 10), bd=5, command=self.show_point)
        quit_button.place(x=390, y=200)

    def next_problem(self):
        """下一题界面"""
        self.question_frame.destroy()
        self.current_num += 1
        self.question_frame = tk.Frame(self.root_frame, width=650, height=400)
        self.question_frame.pack()
        q_text = linecache.getline('../res/expressions.txt', self.current_num)
        if q_text == '':
            self.current_num -= 1
            self.show_point()
        label = tk.Label(self.question_frame, text=q_text, font=('宋体', 20))
        label.place(x=100, y=100)
        self.ans = tk.Entry(self.question_frame, width=20, bd=5)
        self.ans.place(x=250, y=150)
        submit_button = tk.Button(self.question_frame, text=u'提交', font=('宋体', 10), bd=5, command=self.submit)
        submit_button.place(x=150, y=200)
        next_pro_button = tk.Button(self.question_frame, text=u'下一题', font=('宋体', 10), bd=5, command=self.next_problem)
        next_pro_button.place(x=270, y=200)
        quit_button = tk.Button(self.question_frame, text=u'退出并显示', font=('宋体', 10), bd=5, command=self.show_point)
        quit_button.place(x=390, y=200)

    def submit(self):
        """提交并提示答案对错"""
        self.ans_text = self.ans.get()
        right_ans = linecache.getline('../res/answer.txt', self.current_num).split(' ')[1].split('\n')[0]
        if right_ans == self.ans_text:
            box.showinfo(None, '回答正确')
            self.correct_num += 1
        else:
            box.showerror(None, '回答错误')
        self.ans.selection_clear()

    def show_point(self):
        """结束并显示答题数目及对错数目等"""
        box.showinfo(None, '总共答了{}道题，答对了{}道'.format(self.current_num, self.correct_num))
        self.root_frame.destroy()


def main():
    root_frame = tk.Tk(className='四则运算生成器')
    Init(root_frame)
    root_frame.mainloop()


if __name__ == '__main__':
    main()

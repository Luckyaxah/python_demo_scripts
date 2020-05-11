"""
计时器GUI
"""


# -*- coding: utf-8 -*

from tkinter import *
import sys
import time
from DBcm import UseDatabase1 as UseDatabase
from DBconfig import dbconfig
import datetime


class new_Button:
    def __init__(self, text):
        self.ButtonText = text
        self.ButtonBody = Button(None, text=self.ButtonText, relief=RIDGE, command=lambda: (record(
            self.ButtonText, "正在进行:"+self.ButtonText) or text_show(self.ButtonText) or count_duration()), **Button_WandH)


def text_show(x):
    widget_text.delete('1.0', '1.11')
    widget_text.insert('1.0', '正在进行:'+x)


def initiate(*Flag):
    if not Flag:
        widget_text.delete('1.0', '1.11')
        print('已结束')
    else:
        print('开始吧')
    widget_text.insert('1.0', '开始吧')


def record(x, y):

    with UseDatabase(dbconfig) as cursor:
        _SQL = """insert into time_log(title, summary)values(%s,%s)
		"""
        cursor.execute(_SQL, (x, y))
    print(x, y)


def count_duration():
    with UseDatabase(dbconfig) as cursor:
        # _SQL = """select * from time_log """
        _SQL = """select add_time from time_log where id = (select t.* from (select max(id) from time_log)t)
		"""
        _SQL_last = """select add_time from time_log where id = (select t.* from (select max(id)-1 from time_log)t)
		"""
        cursor.execute(_SQL)
        res = cursor.fetchall()
        cursor.execute(_SQL_last)
        res_last = cursor.fetchall()

    print(res)
    print(res_last)
    # print(type(res[0][0]-res_last[0][0]))
    duration = str(res[0][0]-res_last[0][0])
    # print(str(duration))
    with UseDatabase(dbconfig) as cursor:
        _SQL = """update time_log set duration =%s where id = (select t.* from (select max(id)-1 from time_log)t)
		"""
        cursor.execute(_SQL, (duration,))

    print(duration)
    # print(datetime.datetime.now());


def add_comment(z):
    z_text = z.get()
    print(type(z_text))
    print(z_text)
    with UseDatabase(dbconfig) as cursor:
        _SQL = """update time_log set comment = %s
		 where id = (select t.* from (select max(id) from time_log)t )"""
        cursor.execute(_SQL, (z_text,))  # 有意思，传入的一定是一个元组
    pass


if __name__ == '__main__':

    root = Tk()
    root.title('计时器')
    root.geometry('400x400')
    # widget = Label(root)
    # widget.config(text='Timer')
    # widget.pack(side = TOP, fill = X)

    Button_WandH = {'height': 4, 'width': 8}

    # widget_button_exit = Button(None, text = '关闭', command = sys.exit)
    # widget_button_exit.pack( side= RIGHT )

    text_row1 = ['用例', '测试', '读代码', '会议', '编程', '学习', '文档', '休息', '其他']
    # widget_button_Func=[]
    # i = 0

    widget_button_Func = []
    i = 0

    for var_string in text_row1:
        # widget_button_Func.append(
        # 	Button(None , text = var_string,relief = RIDGE ,command = lambda : record(var_string) or test(var_string); , **Button_WandH) )
        widget_button_Func.append(new_Button(var_string))
        widget_button_Func[i].ButtonBody.place(
            x=100 + i % 3 * 100, y=100 + i//3 * 90)
        i += 1

    widget_text_comment = Entry(None, text='再这里输入备注信息')
    # widget_text_comment.insert("1.0","在这里输入备注信息")
    widget_text_comment.place(x=40, y=40)

    widget_insertcomment_btn = Button(
        None, text="添加", relief=RIDGE, command=lambda: add_comment(widget_text_comment))
    widget_insertcomment_btn.place(x=35, y=80)

    widget_button_close = Button(None, text='结束', relief=RIDGE, command=lambda: (
        initiate() or record("结束", "已结束")or count_duration()or sys.exit()), height=3, width=6)
    # widget_button_Fuc1.pack(ipadx =10 ,ipady =10 )
    widget_button_close.place(x=250, y=30)

    # widget_button_Fuc2 = Button(None, text = '测试', command = test ,**Button_WandH)
    # # widget_button_Fuc2.pack(ipadx =10 ,ipady =10 )
    # widget_button_Fuc2.place(x=200,y=100)

    # widget_button_Fuc3 = Button(None, text = '测试', command = test ,**Button_WandH)
    # # widget_button_Fuc2.pack(ipadx =10 ,ipady =10 )
    # widget_button_Fuc3.place(x=300,y=100)

    widget_text = Text(None, height=1, width=15)
    initiate(0)
    widget_text.place(x=10, y=10)
    # # widget_text.pack(side = TOP)
    # widget_text.grid(row = 0, column = 0)

    # count_duration()

    root.mainloop()

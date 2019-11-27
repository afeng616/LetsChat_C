#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Afeng
# Time: 2019/11/21 17:11
# Description: LetsChat客户端UI

from module.process import *
from tkinter.messagebox import *

# LetsChat主窗体
class UI(object):
    def __init__(self, title, version, width, height):
        self.width = width
        self.height = height
        self.title = title
        self.version = version
        self.mymessage_color = 'green'
        self.tag = 'my_message'

        self.window = Tk()
        self.frm_l = Frame(self.window)  # 左窗口
        self.frm_r = Frame(self.window)  # 右窗口
        self.text_history = Text(self.frm_l, width=65)  # 消息展示框
        self.input = Entry(self.frm_l, width=60)  # 信息键入框
        self.button_send = Button(self.frm_l, text='发送')  # 发送按钮
        self.list_persons = Listbox(self.frm_r, height=18)  # 成员列表
        self.menu = Menu(self.frm_r, tearoff=0)  # 双击菜单

        self.process = UDPProcess(self.text_history)

    def show(self):
        # 主窗口配置
        WIDTH = self.window.winfo_screenwidth()
        HEIGHT = self.window.winfo_screenheight()
        self.window.title(self.title + self.version)
        self.window.resizable(0, 0)
        self.window.geometry('{}x{}+{}+{}'.format(self.width, self.height,
                                                  (WIDTH - self.width) // 2, (HEIGHT - self.height) // 2))

        self.frm_l.pack(side='left')
        # 消息展示框设置
        scrol = Scrollbar(self.frm_l)
        scrol.pack(side='right', fill=Y)
        self.text_history.config(state=DISABLED, yscrollcommand=scrol.set)
        self.text_history.pack()
        scrol.config(command=self.text_history.yview)
        # 输入框设置
        self.input.bind('<Return>', self.submit)
        self.input.pack(side='left', padx=15)
        # 发送按钮设置
        self.button_send.config(command=self.send_message)
        self.button_send.pack(side='right')

        self.frm_r.pack(side='right')
        # 成员列表设置
        label = Label(self.frm_r, text="成员列表")
        label.pack()
        sb = Scrollbar(self.frm_r)
        sb.pack(side='right', fill=Y)
        for i in range(20):
            self.list_persons.insert(END, str(i) + '-JoJo')
        self.list_persons.config(yscrollcommand=sb.set)
        self.list_persons.bind('<Double-Button-1>', self.do_popup)
        self.list_persons.pack(padx=5)
        sb.config(command=self.list_persons.yview)
        # 双击菜单设置
        self.menu.add_command(label='item', state=DISABLED)
        self.menu.add_separator()
        self.menu.add_command(label='私聊')
        self.menu.add_command(label='查看信息')

        self.window.mainloop()

    # 发送消息并展示
    def send_message(self):
        var = self.input.get().strip(' ')
        if var:
            self.text_history.config(state=NORMAL)
            self.text_history.tag_config(self.tag, foreground=self.mymessage_color)
            self.text_history.insert('end', get_time() + '  我(' + get_ip() + ')：\n    '
                                     + var + '\n', self.tag)
            self.text_history.config(state=DISABLED)
            self.text_history.see(END)
            self.input.delete(0, 'end')

            self.process.send(var)

    # 回车发送消息
    def submit(self, e):
        self.send_message()

    # 弹出菜单
    def do_popup(self, event):
        self.menu.entryconfigure(0, label=self.list_persons.get(self.list_persons.curselection()))
        self.menu.tk_popup(event.x_root, event.y_root + 20, 0)


# 登录/注册窗体
class PreUI(object):
    def __init__(self, title, version):
        self.title = title
        self.version = version

        self.process = SQLProcess()
        self.window = Tk()
        self.label_register = Label(self.window, text='去注册>>', fg='blue', font='microsoftyahei 10 italic')
        self.input_account = Entry(self.window)
        self.input_password = Entry(self.window)
        self.button_login = Button(self.window, text='登录', width=8)

    def show(self):
        width = 400
        height = 240
        WIDTH = self.window.winfo_screenwidth()
        HEIGHT = self.window.winfo_screenheight()
        self.window.title(self.title + self.version)
        self.window.resizable(0, 0)
        self.window.geometry('{}x{}+{}+{}'.format(width, height,
                                                  (WIDTH - width) // 2, (HEIGHT - height) // 2))

        Label(self.window, text='LetsChat Login', font='Helvetica 15 bold italic').pack(side='top', pady='20')
        Label(self.window, text='账号：', font='Helvetica 12 bold').place(relx='.2', rely='.3')
        self.label_register.place(relx='.2', rely='.4')
        self.input_account.place(relx='.4', rely='.3')
        self.input_account.bind("<Return>", self.submit)
        Label(self.window, text='密码：', font='Helvetica 12 bold').place(relx='.2', rely='.5')
        self.input_password.place(relx='.4', rely='.5')
        self.input_password.bind("<Return>", self.submit)
        self.button_login.place(x=170, y=180)
        self.button_login.config(command=self.login)

        self.window.mainloop()

    # 回车事件
    def submit(self, e):
        self.login()

    # 登录
    def login(self):
        account = self.input_account.get()
        password = self.input_password.get()
        if account and password:
            if self.process.login(account, password):
                logging.info('登录成功')
                self.window.destroy()
                UI('LetsChat_C ', 'V0.1-local', 600, 380).show()
            else:
                # TODO: 登录失败提示
                logging.error('登录失败')
                showinfo("Tip", "账号或密码输入错误！")


if __name__ == '__main__':
    # UI('LetsChat_C ', 'V0.1-local', 600, 380).show()
    PreUI('LetsChat_C ', 'V0.1-local').show()

#
# # 项目名称、版本
# TITLE = "LetsChat_C "
# VERSION = "V0.1-local"
#
# # 窗口大小
# WIDTH = 600
# HEIGHT = 380
#
# window = Tk()
# window.title(TITLE + VERSION)
#
# # 屏幕大小
# width = window.winfo_screenwidth()
# height = window.winfo_screenheight()
# window.resizable(0, 0)
# window.geometry('{}x{}+{}+{}'.format(WIDTH, HEIGHT, (width - WIDTH) // 2, (height - HEIGHT) // 2))
#
# # 左窗口
# frm_l = Frame(window)
# frm_l.pack(side='left')
#
# # 历史记录
# text_history = Text(frm_l, width='70')
# text_history.config(state=DISABLED)
# text_history.pack()
# TAG_NAME = 'message_color'
# MESSAGE_COLOR = 'green'
#
#
# # 末尾插入输入框数据
# def insert_end():
#     var = e.get().strip(' ')
#     if var != '':
#         text_history.config(state=NORMAL)
#         text_history.tag_config(TAG_NAME, foreground=MESSAGE_COLOR)
#         text_history.insert('end', get_time() +
#                             '  我(' + get_ip() + ')：\n    ' + var + '\n',
#                             TAG_NAME)
#         text_history.config(state=DISABLED)
#         e.delete(0, 'end')
#
#
# # 回车提交
# def submit(event):
#     insert_end()
#
#
# # 输入框
# e = Entry(frm_l, width='60')
# e.bind('<Return>', submit)
# e.pack(side='left', padx='15')
#
# # 发送
# button_send = Button(frm_l, text='发送', command=insert_end)
# button_send.pack(side='right')
# # Button(frm_l, text='others', command=lambda: (
# #     text_history.config(state=NORMAL),
# #     text_history.insert('end', '\n' + 'others message here'),
# #     text_history.config(state=DISABLED)
# # )).pack()
#
# # 右窗口
# frm_r = Frame(window)
# frm_r.pack(side='right')
#
# # 人员列表
# label = Label(frm_r, text="人员列表")
# label.pack()
# sb = Scrollbar(frm_r)
# sb.pack(side='right', fill=Y)
# listbox_persons = Listbox(frm_r, height='18', yscrollcommand=sb.set)
# for i in range(20):
#     listbox_persons.insert(END, str(i) + '-jojo')
# listbox_persons.pack(padx='5')
# sb.config(command=listbox_persons.yview)
#
# # 双击菜单
# popup = Menu(frm_r, tearoff=0)
# popup.add_command(label='item', state=DISABLED)
# popup.add_separator()
# popup.add_command(label='私聊')
# popup.add_command(label='查看信息')
#
#
# def do_pupup(event):
#     popup.entryconfigure(0, label=listbox_persons.get(listbox_persons.curselection()), state=DISABLED)
#     popup.tk_popup(event.x_root, event.y_root, 0)
#
#
# listbox_persons.bind('<Double-Button-1>', do_pupup)
#
# # 窗口显示
# window.mainloop()

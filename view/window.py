#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Afeng
# Time: 2019/11/21 17:11
# Description: LetsChat客户端UI

from module.process import *
from tkinter.messagebox import *


# LetsChat主窗体
class UI(object):
    def __init__(self, title, version, width, height, account):
        self.width = width
        self.height = height
        self.title = title
        self.version = version
        self.id = account
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

        self.process_udp = UDPProcess(self.text_history, self.list_persons, account)
        self.process_sql = SQLProcess()
        self.process_udp.members = self.process_sql.members()
        self.process_udp.init_users_status()
        self.ip = self.process_udp.ip

    # 界面展示
    def show(self):
        # 群聊权限检测
        def check():
            if self.process_sql.join(self.id):
                logging.info('进入群聊')
                to_chat.destroy()
                self.chat()
            else:
                logging.info('申请群聊权限')
                showinfo('Tip', '已向管理员发送群聊申请，请耐心等待。')
                self.process_sql.join_apply(self.id)

        # 主窗口配置
        WIDTH = self.window.winfo_screenwidth()
        HEIGHT = self.window.winfo_screenheight()
        self.window.title(self.title + self.version)
        self.window.resizable(0, 0)
        self.window.geometry('{}x{}+{}+{}'.format(self.width, self.height,
                                                  (WIDTH - self.width) // 2, (HEIGHT - self.height) // 2))

        to_chat = Button(self.window, text='进入群聊', command=check, font='Helvetica 15 bold')
        to_chat.place(x=240, y=160)

    def chat(self):
        self.process_udp.start()

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
            self.text_history.insert('end', get_time() + '  我(' + self.ip + ')：\n    '
                                     + var + '\n', self.tag)
            self.text_history.config(state=DISABLED)
            self.text_history.see(END)
            self.input.delete(0, 'end')

            self.process_udp.send(var)

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
        self.WIDTH = self.window.winfo_screenwidth()
        self.HEIGHT = self.window.winfo_screenheight()
        self.label_register = Label(self.window, text='去注册>>', fg='blue', font='microsoftyahei 10 italic')
        self.input_account = Entry(self.window, font='microsoftyahei 12')
        self.input_password = Entry(self.window, font='microsoftyahei 12', show='*')
        self.button_login = Button(self.window, text='登录', width=8)

    def show(self):
        width = 400
        height = 240
        self.window.title(self.title + self.version)
        self.window.resizable(0, 0)
        self.window.geometry('{}x{}+{}+{}'.format(width, height,
                                                  (self.WIDTH - width) // 2, (self.HEIGHT - height) // 2))

        # LetsChat Login大标签
        Label(self.window, text='LetsChat Login', font='Helvetica 15 bold italic').pack(side='top', pady='20')
        # 登录
        Label(self.window, text='账号：', font='Helvetica 12 bold').place(relx='.2', rely='.3')
        self.input_account.place(relx='.4', rely='.3')
        self.input_account.bind("<Return>", self.submit)
        # 密码
        Label(self.window, text='密码：', font='Helvetica 12 bold').place(relx='.2', rely='.5')
        self.input_password.place(relx='.4', rely='.5')
        self.input_password.bind("<Return>", self.submit)
        # 注册
        self.label_register.place(relx='.2', rely='.4')
        self.label_register.bind('<Button-1>', self.register_ui)
        # 登录按钮
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
                logging.info(str(account) + '-登录成功')
                self.window.destroy()
                UI(NAME, VERSION, 600, 380, account).show()
            else:
                showinfo("Tip", "账号或密码输入错误！")

    # 注册窗口
    def register_ui(self, e):
        logging.info("去注册")
        width = 350
        height = 370
        window_register = Toplevel(self.window)
        window_register.title(self.title + '注册')
        window_register.resizable(0, 0)
        window_register.geometry('{}x{}+{}+{}'.format(width, height,
                                                      (self.WIDTH - width) // 2, (self.HEIGHT - height) // 2))
        window_register.grab_set()  # 模态控制

        # 注册操作
        def register_do():
            if input_nickname.get() and input_account.get() and input_password and input_resure:
                if input_resure.get() == input_password.get():
                    if self.process.register():
                        window_register.destroy()
                        self.window.destroy()
                        UI(NAME, VERSION, 600, 380, input_account.get()).show()
                        logging.info(input_account.get() + '-注册成功，登录完毕')
                    else:
                        showinfo('Tip', '注册失败，请稍后再试')
                        window_register.destroy()
                        logging.error('注册失败')
                else:
                    showinfo("Tip", "两次密码输入不同")

        def register_d(e):
            register_do()

        # 输入长度限制
        def length_limit(entry, length):
            if len(entry.get()) > length:
                entry.set(entry.get()[:-1])

        # LetsChat Register大标签
        Label(window_register, text='LetsChat Register', font='Helvetica 15 bold italic').pack(side='top', pady=40)
        # 昵称
        Label(window_register, text='昵称：', font='Helvetica 12 bold').place(x=55, y=100)
        nickname = StringVar()
        nickname.trace('w', lambda *args: length_limit(nickname, 8))
        input_nickname = Entry(window_register, textvariable=nickname, font='microsoftyahei 12')
        input_nickname.bind('<Return>', register_d)
        input_nickname.place(x=120, y=102)
        # 账号
        Label(window_register, text='账号：', font='Helvetica 12 bold').place(x=55, y=140)
        account = StringVar()
        account.trace('w', lambda *args: length_limit(account, 12))
        input_account = Entry(window_register, textvariable=account, font='microsoftyahei 12')
        input_account.bind('<Return>', register_d)
        input_account.place(x=120, y=142)
        # 密码
        Label(window_register, text='密码：', font='Helvetica 12 bold').place(x=55, y=180)
        password = StringVar()
        password.trace('w', lambda *args: length_limit(password, 18))
        input_password = Entry(window_register, textvariable=password, show='*', font='microsoftyahei 12')
        input_password.bind('<Return>', register_d)
        input_password.place(x=120, y=182)
        # 确认密码
        Label(window_register, text='确认密码：', font='Helvetica 12 bold').place(x=24, y=220)
        resure = StringVar()
        input_resure = Entry(window_register, textvariable=resure, show='*', font='microsoftyahei 12')
        input_resure.bind('<Return>', register_d)
        input_resure.place(x=120, y=222)
        # 注册按钮
        button_register = Button(window_register, text='确认注册', command=register_do)
        button_register.place(x=155, y=280)


if __name__ == '__main__':
    # UI('LetsChat_C ', 'V0.1-local', 600, 380).show()
    PreUI(NAME, VERSION).show()

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

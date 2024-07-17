import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json

class GUI3:

    def start(self):
        #global mainWindow
        self.root = tk.Toplevel()
        self.root.title('原声大碟关键词与音频对照表')
        self.root.geometry("500x350")
        self.interface1()

    def interface1(self):
        # (1)创建 Treeview 控件, 设置高度为10行
        self.tree = ttk.Treeview(self.root, height=10)
        self.tree.grid(rowspan=10, columnspan=10, padx=30)
        # (2)定义列名
        self.tree["columns"] = ("Name", "Age")
        # (3)设置列的标题名称
        self.tree.heading("#0", text="序号", anchor="w")
        self.tree.heading("Name", text="关键词")
        self.tree.heading("Age", text="音频")
        # (4)设置列宽度(像素)
        self.tree.column("#0", width=50)
        self.tree.column("Name", width=100, anchor="center")
        self.tree.column("Age", width=90, anchor="center")
        # (5)插入数据
        configFile = open(".\settings.json", encoding="utf8")
        self.settings = json.load(configFile)
        self.keywordDir = open(self.settings["ysddTableFile"], encoding="utf8")
        i = 1
        for keyword in json.load(self.keywordDir).items():
            self.tree.insert("", tk.END, text=i, values=(keyword))
            i = i+1
        # 创建按钮
        self.Button0 = tk.Button(self.root, text="添加", command=self.add_page)
        self.Button0.grid(row=11, column=1, ipadx=10)
        self.Button1 = tk.Button(self.root, text="编辑", command=self.edit_page)
        self.Button1.grid(row=11, column=3, ipadx=10)
        self.Button2 = tk.Button(self.root, text="删除", command=self.delete_item)
        self.Button2.grid(row=11, column=5, ipadx=10)
        self.Button3 = tk.Button(self.root, text="保存", command=self.save_data)
        self.Button3.grid(row=11, column=2, ipadx=10)

    def add_page(self):
        self.Label0 = tk.Label(self.root, text="关键词")
        self.Label0.grid(row=0, column=11)

        self.entry00 = tk.StringVar()
        self.entry0 = tk.Entry(self.root, textvariable=self.entry00, width=15)
        self.entry0.grid(row=1, column=11)

        self.Label1 = tk.Label(self.root, text="音频")
        self.Label1.grid(row=2, column=11)

        self.entry01 = tk.StringVar()
        self.entry1 = tk.Entry(self.root, textvariable=self.entry01, width=15)
        self.entry1.grid(row=3, column=11)

        self.Button_1 = tk.Button(self.root, text="确定", command=self.add_item)
        self.Button_1.grid(row=6, column=11, ipadx=10)

    def add_item(self):
        '''添加数据'''
        rows = self.tree.get_children()  # 获取所有的行ID
        name = self.entry00.get()
        age = self.entry01.get()
        if name and age:
            self.tree.insert("", tk.END, text=len(rows)+1, values=(name, age))
        else:
            self.Button_1.bind("<Button-1>", self.window("输入框不可以为空"))

    def edit_page(self):
        selected_items = self.tree.selection()
        if selected_items:
            for item in selected_items:
                row_data = self.tree.item(item)['values']

                self.Label0 = tk.Label(self.root, text="关键词")
                self.Label0.grid(row=0, column=11)

                self.entry00 = tk.StringVar()
                self.entry00.set(row_data[0])
                self.entry0 = tk.Entry(self.root, textvariable=self.entry00, width=15)
                self.entry0.grid(row=1, column=11)

                self.Label1 = tk.Label(self.root, text="音频")
                self.Label1.grid(row=2, column=11)

                self.entry01 = tk.StringVar()
                self.entry01.set(row_data[1])
                self.entry1 = tk.Entry(self.root, textvariable=self.entry01, width=15)
                self.entry1.grid(row=3, column=11)


                self.Button_1 = tk.Button(self.root, text="确定", command=self.edit_item)
                self.Button_1.grid(row=6, column=11, ipadx=10)
        else:
            self.Button1.bind("<Button-1>", self.window("未选中数据"))

    def edit_item(self):
        #编辑数据
        selected_item = self.tree.selection()
        name = self.entry00.get()
        age = self.entry01.get()
        if name and age :
            self.tree.item(selected_item, values=(name, age))
        else:
            self.Button_1.bind("<Button-1>", self.window("输入框不可以为空"))

    def delete_item(self):
        '''删除数据'''
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
        else:
            self.Button2.bind("<Button-1>", self.window("未选中数据"))

    def window(e, text):
        '''创建弹窗'''
        messagebox.showinfo("提示", text)

    def save_data(self):
        #保存数据
        datasheet = {}
        dict1 = {}
        rows = self.tree.get_children()  # 获取所有的行ID
        # 遍历每一行
        for row in rows:
            # 获取该行的数据
            list1 = self.tree.item(row)['values']
            #print(list1)
            dict1 = {list1[0]: list1[1]}
            datasheet.update(dict1)
        #保存
        filepath = open(self.settings["ysddTableFile"], "w", encoding="utf8")
        json.dump(datasheet, filepath, ensure_ascii=False, indent="\t")
        messagebox.showinfo("保存原声大碟关键词与音频对照表", "保存成功")
        self.root.destroy()

class GUI2:

    def start(self):
        #global mainWindow
        self.root = tk.Toplevel()
        self.root.title('非中文字符读法字典')
        self.root.geometry("500x350")
        self.interface1()

    def interface1(self):
        # (1)创建 Treeview 控件, 设置高度为10行
        self.tree = ttk.Treeview(self.root, height=10)
        self.tree.grid(rowspan=10, columnspan=10, padx=30)
        # (2)定义列名
        self.tree["columns"] = ("Name", "Age")
        # (3)设置列的标题名称
        self.tree.heading("#0", text="序号", anchor="w")
        self.tree.heading("Name", text="字符")
        self.tree.heading("Age", text="读法")
        # (4)设置列宽度(像素)
        self.tree.column("#0", width=50)
        self.tree.column("Name", width=100, anchor="center")
        self.tree.column("Age", width=90, anchor="center")
        # (5)插入数据
        configFile = open(".\settings.json", encoding="utf8")
        self.settings = json.load(configFile)
        self.keywordDir = open(self.settings["dictFile"], encoding="utf8")
        i = 1
        for keyword in json.load(self.keywordDir).items():
            self.tree.insert("", tk.END, text=i, values=(keyword))
            i = i+1
        # 创建按钮
        self.Button0 = tk.Button(self.root, text="添加", command=self.add_page)
        self.Button0.grid(row=11, column=1, ipadx=10)
        self.Button1 = tk.Button(self.root, text="编辑", command=self.edit_page)
        self.Button1.grid(row=11, column=3, ipadx=10)
        self.Button2 = tk.Button(self.root, text="删除", command=self.delete_item)
        self.Button2.grid(row=11, column=5, ipadx=10)
        self.Button3 = tk.Button(self.root, text="保存", command=self.save_data)
        self.Button3.grid(row=11, column=2, ipadx=10)

    def add_page(self):
        self.Label0 = tk.Label(self.root, text="字符")
        self.Label0.grid(row=0, column=11)

        self.entry00 = tk.StringVar()
        self.entry0 = tk.Entry(self.root, textvariable=self.entry00, width=15)
        self.entry0.grid(row=1, column=11)

        self.Label1 = tk.Label(self.root, text="读法")
        self.Label1.grid(row=2, column=11)

        self.entry01 = tk.StringVar()
        self.entry1 = tk.Entry(self.root, textvariable=self.entry01, width=15)
        self.entry1.grid(row=3, column=11)

        self.Button_1 = tk.Button(self.root, text="确定", command=self.add_item)
        self.Button_1.grid(row=6, column=11, ipadx=10)

    def add_item(self):
        '''添加数据'''
        rows = self.tree.get_children()  # 获取所有的行ID
        name = self.entry00.get()
        age = self.entry01.get()
        if name and age:
            self.tree.insert("", tk.END, text=len(rows)+1, values=(name, age))
        else:
            self.Button_1.bind("<Button-1>", self.window("输入框不可以为空"))

    def edit_page(self):
        selected_items = self.tree.selection()
        if selected_items:
            for item in selected_items:
                row_data = self.tree.item(item)['values']

                self.Label0 = tk.Label(self.root, text="字符")
                self.Label0.grid(row=0, column=11)

                self.entry00 = tk.StringVar()
                self.entry00.set(row_data[0])
                self.entry0 = tk.Entry(self.root, textvariable=self.entry00, width=15)
                self.entry0.grid(row=1, column=11)

                self.Label1 = tk.Label(self.root, text="读法")
                self.Label1.grid(row=2, column=11)

                self.entry01 = tk.StringVar()
                self.entry01.set(row_data[1])
                self.entry1 = tk.Entry(self.root, textvariable=self.entry01, width=15)
                self.entry1.grid(row=3, column=11)


                self.Button_1 = tk.Button(self.root, text="确定", command=self.edit_item)
                self.Button_1.grid(row=6, column=11, ipadx=10)
        else:
            self.Button1.bind("<Button-1>", self.window("未选中数据"))

    def edit_item(self):
        #编辑数据
        selected_item = self.tree.selection()
        name = self.entry00.get()
        age = self.entry01.get()
        if name and age :
            self.tree.item(selected_item, values=(name, age))
        else:
            self.Button_1.bind("<Button-1>", self.window("输入框不可以为空"))

    def delete_item(self):
        '''删除数据'''
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
        else:
            self.Button2.bind("<Button-1>", self.window("未选中数据"))

    def window(e, text):
        '''创建弹窗'''
        messagebox.showinfo("提示", text)

    def save_data(self):
        #保存数据
        datasheet = {}
        dict1 = {}
        rows = self.tree.get_children()  # 获取所有的行ID
        # 遍历每一行
        for row in rows:
            # 获取该行的数据
            list1 = self.tree.item(row)['values']
            #print(list1)
            dict1 = {list1[0]: list1[1]}
            datasheet.update(dict1)
        #保存
        filepath = open(self.settings["dictFile"], "w", encoding="utf8")
        json.dump(datasheet, filepath, ensure_ascii=False, indent="\t")
        messagebox.showinfo("保存非中文字符读法字典", "保存成功")
        self.root.destroy()

class GUI1:

    def start(self):
        #global mainWindow
        self.root = tk.Toplevel()
        self.root.title('敏感词词库')
        self.root.geometry("500x350")
        self.interface1()

    def interface1(self):
        # (1)创建 Treeview 控件, 设置高度为10行
        self.tree = ttk.Treeview(self.root, height=10)
        self.tree.grid(rowspan=10, columnspan=10, padx=30)
        # (2)定义列名
        self.tree["columns"] = ("Name", "Age")
        # (3)设置列的标题名称
        self.tree.heading("#0", text="序号", anchor="w")
        self.tree.heading("Name", text="敏感词")
        self.tree.heading("Age", text="备注")
        # (4)设置列宽度(像素)
        self.tree.column("#0", width=50)
        self.tree.column("Name", width=100, anchor="center")
        self.tree.column("Age", width=90, anchor="center")
        # (5)插入数据
        configFile = open(".\settings.json", encoding="utf8")
        self.settings = json.load(configFile)
        self.keywordDir = open(self.settings["keywordDir"], encoding="utf8")
        i = 1
        for keyword in json.load(self.keywordDir).items():
            self.tree.insert("", tk.END, text=i, values=(keyword))
            i = i+1
        # 创建按钮
        self.Button0 = tk.Button(self.root, text="添加", command=self.add_page)
        self.Button0.grid(row=11, column=1, ipadx=10)
        self.Button1 = tk.Button(self.root, text="编辑", command=self.edit_page)
        self.Button1.grid(row=11, column=3, ipadx=10)
        self.Button2 = tk.Button(self.root, text="删除", command=self.delete_item)
        self.Button2.grid(row=11, column=5, ipadx=10)
        self.Button3 = tk.Button(self.root, text="保存", command=self.save_data)
        self.Button3.grid(row=11, column=2, ipadx=10)

    def add_page(self):
        self.Label0 = tk.Label(self.root, text="敏感词")
        self.Label0.grid(row=0, column=11)

        self.entry00 = tk.StringVar()
        self.entry0 = tk.Entry(self.root, textvariable=self.entry00, width=15)
        self.entry0.grid(row=1, column=11)

        self.Label1 = tk.Label(self.root, text="备注")
        self.Label1.grid(row=2, column=11)

        self.entry01 = tk.StringVar()
        self.entry1 = tk.Entry(self.root, textvariable=self.entry01, width=15)
        self.entry1.grid(row=3, column=11)

        self.Button_1 = tk.Button(self.root, text="确定", command=self.add_item)
        self.Button_1.grid(row=6, column=11, ipadx=10)

    def add_item(self):
        '''添加数据'''
        rows = self.tree.get_children()  # 获取所有的行ID
        name = self.entry00.get()
        age = self.entry01.get()
        if name:
            self.tree.insert("", tk.END, text=len(rows)+1, values=(name, age))
        else:
            self.Button_1.bind("<Button-1>", self.window("输入框不可以为空"))

    def edit_page(self):
        selected_items = self.tree.selection()
        if selected_items:
            for item in selected_items:
                row_data = self.tree.item(item)['values']

                self.Label0 = tk.Label(self.root, text="敏感词")
                self.Label0.grid(row=0, column=11)

                self.entry00 = tk.StringVar()
                self.entry00.set(row_data[0])
                self.entry0 = tk.Entry(self.root, textvariable=self.entry00, width=15)
                self.entry0.grid(row=1, column=11)

                self.Label1 = tk.Label(self.root, text="备注")
                self.Label1.grid(row=2, column=11)

                self.entry01 = tk.StringVar()
                self.entry01.set(row_data[1])
                self.entry1 = tk.Entry(self.root, textvariable=self.entry01, width=15)
                self.entry1.grid(row=3, column=11)


                self.Button_1 = tk.Button(self.root, text="确定", command=self.edit_item)
                self.Button_1.grid(row=6, column=11, ipadx=10)
        else:
            self.Button1.bind("<Button-1>", self.window("未选中数据"))

    def edit_item(self):
        #编辑数据
        selected_item = self.tree.selection()
        name = self.entry00.get()
        age = self.entry01.get()
        if name:
            self.tree.item(selected_item, values=(name, age))
        else:
            self.Button_1.bind("<Button-1>", self.window("输入框不可以为空"))

    def delete_item(self):
        '''删除数据'''
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
        else:
            self.Button2.bind("<Button-1>", self.window("未选中数据"))

    def window(e, text):
        '''创建弹窗'''
        messagebox.showinfo("提示", text)

    def save_data(self):
        #保存数据
        datasheet = {}
        dict1 = {}
        rows = self.tree.get_children()  # 获取所有的行ID
        # 遍历每一行
        for row in rows:
            # 获取该行的数据
            list1 = self.tree.item(row)['values']
            #print(list1)
            dict1 = {list1[0]: list1[1]}
            datasheet.update(dict1)
        #保存
        filepath = open(self.settings["keywordDir"], "w", encoding="utf8")
        json.dump(datasheet, filepath, ensure_ascii=False, indent="\t")
        messagebox.showinfo("保存敏感词词库", "保存成功")
        self.root.destroy()

def runjsonloader(mode):
    if (mode==1):#敏感词设置
        a = GUI1()
    if (mode==2):#字符设置
        a = GUI2()
    if (mode==3):#原声大碟设置
        a = GUI3()
    a.start()
    
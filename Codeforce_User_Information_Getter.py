#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# @Author : xkk1
import datetime # 时间
import json # 解析 json 数据
import os # 系统
import os.path # 文件判断
import sys # 系统
import time # 时间
import tkinter as tk # 图像界面
import tkinter.filedialog # 图形界面-选择文件
import tkinter.font # 图形界面-字体
import tkinter.messagebox # 对话框
import tkinter.scrolledtext # 图形界面-滚动文本框
from tkinter import ttk # 用于显示信息的 Treeview 控件
from traceback import format_exc #用于精准的获取错误异常
from typing import List, Dict, Tuple, Any # 类型标注
import urllib.error # 请求获取网络信息错误
import urllib.request # 请求获取网络信息
import webbrowser # 打开浏览器

import xlwt # 导出 excel


PROGRAM: str = "Codeforce User Information Getter"
VERSION: Tuple[int, int, int, int] = (0, 0, 1, 4)
VERSION_STR: str = "%d.%d.%d.%d" % VERSION
# API https://codeforces.com/apiHelp/methods
API_user_info: str = "https://codeforces.com/api/user.info?handles="
handles_file_name: str = "handles.txt"


def get_bytes_coding(b: bytes) -> str:
    """
    获取字符编码类型
    """
    # win10:ANSI、UTF-16 LE、UTF-16 BE、UTF-8、带有 BOM 的 UTF-8
    # win7:ANSI、Unicode、 Unicode big endian、UTF-8
    # 说明：UTF兼容ISO8859-1和ASCII,GB18030兼容GBK,GBK兼容GB2312,GB2312兼容ASCIl
    CODES: List[str, str, str, str] = ['UTF-8', "GB18030", "BIG5", "UTF-16"]
    # UTF-8 BOM前缀字节
    UTF_8_BOM: bytes = b"\xef\xbb\xbf"
    for code in CODES:
        try:
            b.decode(encoding=code)
            if "UTF-8" == code and b.startswith(UTF_8_BOM):
                return "UTF-8-SIG"
            else:
                return code
        except Exception:
            continue
    return "未知字符编码类型"

def get_file_coding(file_path: str) -> str:
    """
    获取文件编码类型
    """
    coding: str = "UTF-8"
    with open(file_path, "rb") as f:
        coding = get_bytes_coding(f.read())
    # print(f"文件“{file_path}”编码“{coding}”")
    return coding

def get_json(url: str, encoding: str = "utf-8") -> Any:
    print(url)
    """使用 get 方法获取 json"""
    # 防反爬，设置 User-Agent
    headers: Dict[str, str] = {"User-Agent" : "Mozilla/5.0 (Linux; U; Android 12; zh-Hans-CN; XT2201-2 Build/S1SC32.52-69-24) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Quark/5.9.3.228 Mobile Safari/537.36"}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    json_data: str = response.read().decode(encoding)
    data = json.loads(json_data)
    return data

class SetRightClickMenu:
    """创建一个右键弹出菜单"""
    def __init__(self, text: str, undo: bool=True):
        menu = tk.Menu(text, tearoff=False)

        menu.add_command(label="剪切", command=lambda:text.event_generate('<<Cut>>'))
        menu.add_command(label="复制", command=lambda:text.event_generate('<<Copy>>'))
        menu.add_command(label="粘贴", command=lambda:text.event_generate('<<Paste>>'))
        menu.add_command(label="删除", command=lambda:text.event_generate('<<Clear>>'))
        if undo:
            menu.add_command(label="撤销", command=lambda:text.event_generate('<<Undo>>'))
            menu.add_command(label="重做", command=lambda:text.event_generate('<<Redo>>'))
        menu.add_separator()
        menu.add_command(label="代码仓库", command=lambda:webbrowser.open("https://github.com/xkk1/Codeforce_User_Information_Getter"))
        menu.add_command(label="个人网站", command=lambda:webbrowser.open("https://xkk1.github.io/"))
        menu.add_command(label="GitHub", command=lambda:webbrowser.open("https://github.com/xkk1"))
        menu.add_command(label="Gitee", command=lambda:webbrowser.open("https://gitee.com/xkk2"))
        menu.add_command(label="CSDN", command=lambda:webbrowser.open("https://blog.csdn.net/qq_55207049"))
        menu.add_command(label="哔哩哔哩", command=lambda:webbrowser.open("https://space.bilibili.com/513689605"))

        def popup(event):
            menu.post(event.x_root, event.y_root)   # post 在指定的位置显示弹出菜单

        text.bind("<Button-3>", popup)

def show_information(information: str="", title: str="信息"):
    """显示信息"""
    global information_window
    global information_scrolledtext
    
    def save_txt(information=information, title=title):
        filename = tkinter.filedialog.asksaveasfilename(
            title='导出至', filetypes=[('TXT', '*.txt'), ('All Files', '*')],
            initialfile='%s' % title,
            # time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            defaultextension = 'txt',  # 默认文件的扩展名
            )  # 返回文件名--另存为
         # title='Select the diagnostic instrument .exe file', filetypes=[('EXE', '*.exe'), ('All Files', '*')],initialdir='C:\\Windows')
        if filename == '':
            return False
        else:
            with open(filename, 'w') as f:
                f.write(information)
            return True

    try:
        # 尝试显示信息窗口（窗口已被创建）
        information_window.deiconify()
        information_window.title(title)
        information_scrolledtext.delete(0.0, tk.END)
        information_scrolledtext.insert(tk.END, information)

    except:
        # 失败时创造一个窗口
        information_window = tk.Tk()
        information_window.title(title)

        information_scrolledtext = tkinter.scrolledtext.ScrolledText(
            information_window,
            width=70,
            height=30,
            undo=True
            # font=('宋体', 12)
            )  # 滚动文本框（宽，高（这里的高应该是以行数为单位），字体样式）
        information_scrolledtext.pack(expand=tk.YES, fill=tk.BOTH, padx=5, pady=5)
 
        information_scrolledtext.insert(tk.INSERT, information)

        SetRightClickMenu(information_scrolledtext) # 设置右键菜单
        
        bottom_frame = tk.Frame(information_window)
        bottom_frame.pack()
        
        save_button = tk.Button(
                bottom_frame,
                text="保存为文本文档(*.txt)",
                command=lambda:save_txt(information=information_scrolledtext.get('1.0', tk.END).rstrip()))
        save_button.pack(side=tk.RIGHT, padx=5,pady=5)

        close_button = tk.Button(
                bottom_frame,
                text="关闭",
                command=information_window.destroy)
        close_button.pack(side=tk.RIGHT, padx=5,pady=5)

        def copy_to_clipboard():
            """Copy current contents of text_entry to clipboard."""
            information_window.clipboard_clear()  # Optional.
            information_window.clipboard_append(information_scrolledtext.get('1.0', tk.END).rstrip())
        
        copy_button = tk.Button(
                bottom_frame,
                text="复制内容到剪贴板",
                command=copy_to_clipboard,
                )
        copy_button.pack(side=tk.LEFT, padx=5,pady=5)
        
        information_window.mainloop()

def show_help():
    """显示帮助"""
    show_information(information=f"""       {PROGRAM} V{VERSION_STR}帮助信息

{PROGRAM} 会从网络上爬取指定 Codeforce 用户的 rating、max rating、last online time。并可以将这些数据导出为 Excel 97-2003 电子表格(*.xls) 

首先您需要
程序会从“{handles_file_name}”读取 handles
格式为一个 handle 占一行

有问题，找作者
 联系方式：
  邮箱：3434623263@qq.com
  QQ：3434623263
  哔哩哔哩(www.bilibili.com)：
    用户名：小喾苦
    UID：513689605
    空间：https://space.bilibili.com/513689605
  个人网站：
    Github Pages：https://xkk1.github.io/
    Gitee Pages：https://xkk2.gitee.io/
  GitHub：https://github.com/xkk1
  Gitee：https://gitee.com/xkk2
  CSDN：https://blog.csdn.net/qq_55207049
""",title=f"{PROGRAM} V{VERSION_STR} 帮助信息")

def show_error():
    """显示报错"""
    info = f"""很抱歉，{PROGRAM} 程序出BUG了，请您把这个错误信息导出发给我，我会把它变得更好
联系方式：
  邮箱：3434623263@qq.com  
  QQ：3434623263 
  哔哩哔哩：小喾苦 (UID：513689605)

程序：{PROGRAM}
版本：{VERSION_STR}
制作者：小喾苦
联系方式：
  邮箱：3434623263@qq.com
  QQ：3434623263
  哔哩哔哩(www.bilibili.com)：
    用户名：小喾苦
    UID：513689605
    空间：https://space.bilibili.com/513689605
  个人网站：
    Github Pages：https://xkk1.github.io/
    Gitee Pages：https://xkk2.gitee.io/
时间：{time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime())}
错误信息：
{format_exc()}"""
    show_information(information=info ,title=f"{PROGRAM} V{VERSION_STR} 错误信息 {time.strftime(r'%Y-%m-%d', time.localtime())}")

class Application(tk.Frame):
    """程序主窗口"""
    handles_list: List = []

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=tk.YES)
        self.columns: Tuple[str] = ("Handle", "Rating", "Max Rating", "Last Online Time")
        self.columns_width: Tuple[int] = (120, 50, 70, 130)
        self.user_data_useful: List[List] = []
        self.user_data_format: List[List] = []
        # self.create_widgets()
        self.creat_heading()
        self.creat_handles_file_select()
        self.creat_show_result()
        self.master.protocol('WM_DELETE_WINDOW', lambda : sys.exit(0))
        self.master.title(f"{PROGRAM} V{VERSION_STR}")

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")
        show_help()

    def creat_heading(self):
        self.heading_Frame = tk.Frame(master=self)
        self.heading_Frame.pack()
        self.heading_program_name_Lable = tk.Label(
            master=self.heading_Frame,
            text=f"{PROGRAM}",
            font=("Times New Roman", 20, tkinter.font.BOLD),
        )
        self.heading_program_name_Lable.pack(side=tk.LEFT)
        self.heading_program_version_Lable = tk.Label(
            master=self.heading_Frame,
            text=f"V{VERSION_STR}",
            font=("Times New Roman", 10, tkinter.font.ITALIC),
        )
        self.heading_program_version_Lable.pack(side=tk.RIGHT)

    def creat_handles_file_select(self):
        """handles 文件选择"""
        self.handles_file_selete_Frame = tk.Frame(self)
        self.handles_file_selete_Frame.pack(fill=tk.X)
        # Entry
        self.handles_file_selete_Entry_Frame = tk.Frame(self.handles_file_selete_Frame)
        self.handles_file_selete_Entry_Frame.pack(padx=4, pady=4, fill=tk.X)
        self.handles_file_selete_Label = tk.Label(
            master=self.handles_file_selete_Entry_Frame,
            text="handles 文件:",
        )
        self.handles_file_selete_Label.pack(side=tk.LEFT)
        self.handles_file_name_StringVar = tk.StringVar()
        self.handles_file_name_StringVar.set(handles_file_name)
        self.handles_file_selete_Entry = tk.Entry(
            self.handles_file_selete_Entry_Frame,
            textvariable=self.handles_file_name_StringVar,
            width=50,
            )
        SetRightClickMenu(self.handles_file_selete_Entry, undo=False)
        self.handles_file_selete_Entry.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        # Button
        self.handles_file_selete_Button_Frame = tk.Frame(self.handles_file_selete_Frame)
        self.handles_file_selete_Button_Frame.pack(padx=4, pady=4, fill=tk.X)
        self.handles_file_selete_choice_Button = tk.Button(
            master=self.handles_file_selete_Button_Frame,
            text="选择文件",
            # font=("Times New Roman", 12),
            command=self.choice_handles_file,
        )
        self.handles_file_selete_choice_Button.pack(side=tk.LEFT)
        self.handles_file_selete_load_Button = tk.Button(
            master=self.handles_file_selete_Button_Frame,
            text="读取文件",
            # font=("Times New Roman", 12),
            command=self.load_handles_file,
        )
        self.handles_file_selete_load_Button.pack(side=tk.LEFT)
        self.handles_file_selete_getter_Button = tk.Button(
            master=self.handles_file_selete_Button_Frame,
            text="获取数据",
            # font=("Times New Roman", 12),
            command=self.handles_information_getter,
        )
        self.handles_file_selete_getter_Button.pack(side=tk.LEFT)
        self.export_data_Button = tk.Button(
            master=self.handles_file_selete_Button_Frame,
            text="导出数据",
            # font=("Times New Roman", 12),
            command=self.export_data,
        )
        self.export_data_Button.pack(side=tk.LEFT)
        self.show_help_Button = tk.Button(
            master=self.handles_file_selete_Button_Frame,
            text="帮助",
            command=show_help,
        )
        self.show_help_Button.pack(side=tk.RIGHT)
    
    def choice_handles_file(self):
        choice_handles_file_name: str = tkinter.filedialog.askopenfilename(
            title="打开 handles 文件(*.txt)",
            filetypes=[('TXT', '*.txt'), ('All Files', '*')],
        )
        if choice_handles_file_name != "":
            self.handles_file_name_StringVar.set(choice_handles_file_name)
    
    def load_handles_file(self):
        handles_file_name: str = self.handles_file_name_StringVar.get()
        if not os.path.isfile(handles_file_name):
            # Handle file not exist
            tkinter.messagebox.showerror(
                title=f"{PROGRAM} 读取 Handle 文件出错！",
                message=f"不能够读取 Handle 文件!\n文件 \"{handles_file_name}\" 不存在!"
            )
            return
        try:
            handles_file_encoding: str = get_file_coding(handles_file_name)
            with open(handles_file_name, mode="r", encoding=handles_file_encoding) as handles_file:
                handles: List[str] = handles_file.readlines()
            for i in range(len(handles)):
                # 删掉每行多余的回车
                if i != len(handles) - 1:
                    handles[i] = handles[i][:-1]
                else:
                    if handles[i][-1] == "\n":
                        handles[i] = handles[i][:-1]
            for i in range(len(handles)):
                # 删掉多余的空行
                while i < len(handles) and handles[i] == "":
                    del handles[i]
            self.handles_list = handles
        except Exception:
            tkinter.messagebox.showerror(
                title=f"读取文件失败 - {PROGRAM} V{VERSION_STR}",
                message="读取文件时出错!\n报错信息：\n" + format_exc()
            )
            return

        # 清空表格
        show_result_Treeview_children = self.show_result_Treeview.get_children()
        for item in  show_result_Treeview_children:
            self.show_result_Treeview.delete(item)
        
        # 插入数据
        for item in self.handles_list:
            self.show_result_Treeview.insert("", tk.END, values=[item])
        
        tkinter.messagebox.showinfo(
            title=f"{PROGRAM} V{VERSION_STR}",
            message=f"成功导入 {len(self.handles_list)} 个 handle(s)."
        )

    def creat_show_result(self):
        """创建显示数据表格"""
        self.show_result_Frame = tk.Frame(master=self)
        self.show_result_Frame.pack(padx=4, pady=4, fill=tk.BOTH, expand=tk.YES)
        
        
        self.show_result_Treeview = ttk.Treeview(
            master=self.show_result_Frame,
            columns=self.columns,
            height=15,
            show='headings', # 不显示表的第一列
        )
        self.show_result_Treeview.pack(fill=tk.BOTH, expand=tk.YES)
        # 每一列的具体设置用 column 函数，heading 为显示指定列名
        for i in range(len(self.columns)):
            self.show_result_Treeview.column(column=self.columns[i], width=self.columns_width[i], anchor=tk.CENTER, stretch=True)
            self.show_result_Treeview.heading(self.columns[i], text=self.columns[i])
        # # ----vertical scrollbar------------
        # self.show_result_vScrollbar = ttk.Scrollbar(self.show_result_Treeview, orient=tk.VERTICAL, command=self.show_result_Treeview.yview)
        # self.show_result_Treeview.configure(yscrollcommand=self.show_result_vScrollbar.set)
        # self.show_result_vScrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # # ----horizontal scrollbar----------
        # self.show_result_hScrollbar = ttk.Scrollbar(self.show_result_Treeview, orient=tk.HORIZONTAL, command=self.show_result_Treeview.xview)
        # self.show_result_Treeview.configure(xscrollcommand=self.show_result_hScrollbar.set)
        # self.show_result_hScrollbar.pack(side=tk.BOTTOM, fill=tk.X)


    def handles_information_getter(self):
        """获取 Handles 数据"""
        if len(self.handles_list) == 0:
            tkinter.messagebox.showerror(
                title=f"错误 - {PROGRAM} V{VERSION_STR}",
                message="错误！没有 Handle\n请先读取文件"
            )
            return
        handles_str: str = ";".join(self.handles_list)
        url: str = API_user_info + handles_str
        try:
            user_data: Dict = get_json(url)
        except urllib.error.HTTPError as e:
            if e.getcode() == 400:
                show_information(
                    title=f"获取 Handle 信息失败！ - {PROGRAM} V{VERSION_STR}",
                    information=f"获取 Handle 信息失败！ - {PROGRAM} V{VERSION_STR}\n\
400 错误!\n\
请检查 handles 是否正确！\n\n\
Request URL: {url}\n\
报错信息：\n{format_exc()}"
                )
            else:
                show_information(
                    title=f"获取 Handle 信息失败！ - {PROGRAM} V{VERSION_STR}",
                    information=f"获取 Handle 信息失败！ - {PROGRAM} V{VERSION_STR}\n\
未知错误!\n\
请检查您的网络是否通畅.\n\n\
Request URL: {url}\n\
报错信息：\n{format_exc()}"
                )
            return
        if user_data["status"] != "OK":
            # 获取用户数据出错
            show_information(
                information="获取 Handle 信息失败！\n已获取的数据：\n" + str(user_data),
                title=f"错误!\n获取 Handle 信息失败！ - {PROGRAM} V{VERSION_STR}",
                )
            return

        # for i in range(len(user_data["result"])):
        #     print(
        #         "%s\t%d\t%d\t%s\t%s" % ( 
        #         user_data["result"][i]["handle"],
        #         user_data["result"][i]["rating"] if "rating" in user_data["result"][i].keys() else 0,
        #         user_data["result"][i]["maxRating"] if "maxRating" in user_data["result"][i].keys() else 0,
        #         user_data["result"][i]["rank"] if "rank" in user_data["result"][i].keys() else "-",
        #         # user_data["result"][i]["maxRating"],
        #         # user_data["result"][i]["rank"],
        #         time.strftime("%Y-%m-%d %X", time.localtime(user_data["result"][i]["lastOnlineTimeSeconds"])))
        #         )
        self.user_data_useful: List[List] = []
        self.user_data_format: List[List] = []
        for i in range(len(user_data["result"])):
            self.user_data_format.append([
                user_data["result"][i]["handle"],
                user_data["result"][i]["rating"] if "rating" in user_data["result"][i].keys() else 0,
                user_data["result"][i]["maxRating"] if "maxRating" in user_data["result"][i].keys() else 0,
                # user_data["result"][i]["rank"] if "rank" in user_data["result"][i].keys() else "-",
                time.strftime(r"%Y/%m/%d %X", time.localtime(user_data["result"][i]["lastOnlineTimeSeconds"]))
                ])
            self.user_data_useful.append([
                user_data["result"][i]["handle"],
                user_data["result"][i]["rating"] if "rating" in user_data["result"][i].keys() else 0,
                user_data["result"][i]["maxRating"] if "maxRating" in user_data["result"][i].keys() else 0,
                # user_data["result"][i]["rank"] if "rank" in user_data["result"][i].keys() else "-",
                user_data["result"][i]["lastOnlineTimeSeconds"]
                ])
        # for i in user_data_format:
        #     print(*i)

        # 清空表格
        show_result_Treeview_children = self.show_result_Treeview.get_children()
        for item in  show_result_Treeview_children:
            self.show_result_Treeview.delete(item)
        
        # 插入数据
        for item in self.user_data_format:
            self.show_result_Treeview.insert("", tk.END, values=item)
    
    def export_data(self):
        """导出数据"""
        if len(self.user_data_useful) == 0:
            tkinter.messagebox.showerror(
                title=f"错误 - {PROGRAM} V{VERSION_STR}",
                message="错误！没有 Handle 数据\n请先获取数据"
            )
            return
        export_filename = tkinter.filedialog.asksaveasfilename(
            title='导出为', filetypes=[('Excel 97-2003 电子表格', '*.xls'), ('All Files', '*')],
            initialfile='Codeforce' + time.strftime(r'%Y%m%d%H%M%S', time.localtime()),
            # time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            defaultextension = 'xls',  # 默认文件的扩展名
            )  # 返回文件名--另存为
        if export_filename == "":
            # 导出文件名为空
            return
        
        # 时间格式
        style_time = xlwt.easyxf(num_format_str='yyyy/m/d h:mm:ss')
        # 获取名字颜色
        def get_name_colour_style(rating: int) -> xlwt.Font:
            # 黑色 < 1
            style_black = xlwt.XFStyle()
            font_black = xlwt.Font()
            font_black.colour_index = 0
            style_black.font = font_black
            # 灰名 < 1200
            style_grey = xlwt.XFStyle()
            font_grey = xlwt.Font()
            font_grey.colour_index = 23
            style_grey.font = font_grey
            # 绿名 < 1400
            style_green = xlwt.XFStyle()
            font_green = xlwt.Font()
            font_green.colour_index = 17
            style_green.font = font_green
            # 青名 < 1600
            style_cyan = xlwt.XFStyle()
            font_cyan = xlwt.Font()
            font_cyan.colour_index = 38
            style_cyan.font = font_cyan
            # 蓝名 < 1900
            style_blue = xlwt.XFStyle()
            font_blue = xlwt.Font()
            font_blue.colour_index = 4
            style_blue.font = font_blue
            # 紫名 < 2100
            style_purple = xlwt.XFStyle()
            font_purple = xlwt.Font()
            font_purple.colour_index = 20
            style_purple.font = font_purple
            # 橙名 < 2400
            style_orange = xlwt.XFStyle()
            font_orange = xlwt.Font()
            font_orange.colour_index = 52
            style_orange.font = font_orange
            # 红名 < 3000
            style_red = xlwt.XFStyle()
            font_red = xlwt.Font()
            font_red.colour_index = 2
            style_red.font = font_red
            # 黑红名 >= 3000
            style_black_red = xlwt.XFStyle()
            font_black_red = xlwt.Font()
            font_black_red.colour_index = 16
            style_black_red.font = font_black_red
            if rating < 1:
                return style_black
            elif rating < 1200:
                return style_grey
            elif rating < 1400:
                return style_green
            elif rating < 1600:
                return style_cyan
            elif rating < 1900:
                return style_blue
            elif rating < 2100:
                return style_purple
            elif rating < 2400:
                return style_orange
            elif rating < 3000:
                return style_red
            else:
                return style_black_red

        # 新建工作簿
        work_book = xlwt.Workbook(encoding='utf-8')
        # 增加 sheet 表
        work_sheet = work_book.add_sheet(time.strftime(r'%Y%m%d%H%M%S', time.localtime()))

        columns_len: int = len(self.columns)
        # 添加表头
        for i in range(columns_len):
            work_sheet.write(0, i, self.columns[i])
        # 设置列宽
        for i in range(len(self.columns_width)):
            work_sheet.col(i).width = self.columns_width[i] * 40
        # 添加数据
        for i in range(len(self.user_data_useful)):
            work_sheet.write(i+1, 0, self.user_data_useful[i][0], get_name_colour_style(self.user_data_useful[i][1]))
            work_sheet.write(i+1, 1, self.user_data_useful[i][1], get_name_colour_style(self.user_data_useful[i][1]))
            work_sheet.write(i+1, 2, self.user_data_useful[i][2], get_name_colour_style(self.user_data_useful[i][2]))
            work_sheet.write(i+1, 3, datetime.datetime.fromtimestamp(self.user_data_useful[i][3]), style_time)
            # for j in range(columns_len):
            #     if j == 3:
            #         work_sheet.write(i+1, j, datetime.datetime.fromtimestamp(self.user_data_useful[i][j]), style_time)
            #     else:
            #         work_sheet.write(i+1, j, self.user_data_useful[i][j])
        # 设置冻结为真
        work_sheet.set_panes_frozen(True)
        # 水平冻结
        work_sheet.set_horz_split_pos(1)
        # 保存
        work_book.save(export_filename)



def main():
    """程序入口，主函数"""
    try:
        # 程序主窗口
        root = tk.Tk()
        app = Application(master=root)
        app.mainloop()
    except SystemExit:
        # 正常退出
        pass
    except Exception:
        show_error()


if __name__ == "__main__":
    main()

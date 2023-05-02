# Codeforce User Information Getter

## 介绍

从网络上爬取指定 Codeforce 用户的 rating、max rating、last online time。可以将这些数据导出为 Excel 97-2003 电子表格(*.xls) 

![使用截图](https://raw.githubusercontent.com/xkk1/Codeforce_User_Information_Getter/main/screenshot.png)

## 安装

搭建 Python3.8+ 环境 [Python 3.8.10 Release](https://www.python.org/downloads/release/python-3810/) 


克隆仓库 main 分支到本地（也可以自行前往 [GitHub](https://github.com/xkk1/Codeforce_User_Information_Getter/tree/main) [下载](https://github.com/xkk1/Codeforce_User_Information_Getter/archive/refs/heads/main.zip)后解压）

```bash
git clone -b main https://github.com/xkk1/Codeforce_User_Information_Getter.git
```

进入目录
```bash
cd Codeforce_User_Information_Getter
```

pip 安装依赖的第三方库

```bash
pip install -r requirements.txt
```

启动程序

```bash
python Codeforce_User_Information_Getter.py
```

## 使用

使用步骤：选择文件 → 读取文件 → 获取数据 → 导出数据

选择文件：  
选择一个包含“姓名信息”和对应“handle”的txt文件  
每一行的格式为“姓名 handle”  
其中“姓名”“handle”之间用空白字符（空格、Tab）分隔  
可以没有“姓名”，但必须有“handle”  

读取文件：  
程序会读取您选择文件的信息  
并把读取到的信息显示到下方的表格中  

获取数据：  
程序会爬取相应的信息并显示到表格中  
期间请保持网络通畅  

导出数据：  
将获取到的数据导出为 Excel 97-2003 电子表格(*.xls)  

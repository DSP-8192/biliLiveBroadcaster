from platform import system
from tkinter import HORIZONTAL, Tk, Toplevel
from tkinter import messagebox, filedialog
from tkinter import Checkbutton, Button, scrolledtext, OptionMenu
from tkinter import Label, font, BooleanVar, DoubleVar, Scale
import tkinter as tk
from huoZiYinShua import *
from multiprocessing import Process, freeze_support
from PIL import ImageTk, Image
import json
import threading
import time
import inspect
import ctypes
from biliLiveBroadcaster import *
import sys
from getcookie import *
from update import *
from jsonloader import runjsonloader
import webbrowser
global livethread
global liveactionflag
liveactionflag = 0	#检测是否处于播报模式

#新建活字印刷类实例
HZYS = huoZiYinShua("./settings.json")
#播放音频的进程
myProcess = Process()
global iflivemodeon

#主框架
#-------------------------------------------
mainWindow = Tk()
stoplivemode = threading.Event()
stopcookie = threading.Event()


#动作
#-------------------------------------------
#直接播放的监听事件
def onDirectPlay():
	global myProcess
	#停止播放按钮上次点击时播放的音频
	try:
		myProcess.terminate()
	except:
		pass
	#播放	
	textToRead = textArea.get(1.0, 'end')
	myProcess = Process(target=HZYS.directPlay,
						kwargs={"rawData": textToRead,
								"inYsddMode": inYsddMode.get(),
								"pitchMult": pitchMultOption.get(),
								"speedMult": speedMultOption.get(),
								"norm": normAudio.get(),
								"reverse": reverseAudio.get()})
	myProcess.start()

#套个壳来禁用启动，直到getcookienow返回值
def beforegetcookie(stopcookie):
	actionButton.config(state="disable")
	livemodeCkBt.config(state="disable")
	cookieButton.config(state="disable")
	try:
		loginstatecode = getcookienow(stopcookie)		#开启代理软件时无法获取cookie
		if (loginstatecode==0):
			messagebox.showinfo("登录成功", "登录成功, 请手动关闭二维码图片")
		if (loginstatecode==86038):
			messagebox.showinfo("登录失败", "登录失败, 原因: 超时, 请尝试重启整个程序")
	except:
		messagebox.showinfo("登录失败", "登录失败, 无法建立连接\n警告: 请关闭所有代理软件(加速器、VPN等), 否则无法正常登录！！\n\n")
		pass
	actionButton.config(state="normal")
	livemodeCkBt.config(state="normal")
	cookieButton.config(state="normal")

#尝试获取cookie
def onTrytologin():
	global cookieProcess
	#停止上次点击时尝试获取的cookie
	try:
		stop_thread(cookieProcess)
		print("打断了上一次登录……")
	except:
		pass
	print("请使用哔哩哔哩APP扫描二维码\n如果二维码没有弹出, 请手动打开此目录下\"Qrcode.png\"")
	cookieProcess = threading.Thread(target=beforegetcookie,args=(stopcookie,))
	cookieProcess.start()
	#cookieButton.config(state="disable")
	
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
 
 
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)



#导出的监听事件
def onExport():
	textToRead = textArea.get(1.0, 'end')
	outputFile = filedialog.asksaveasfilename(title="选择导出路径",
											filetypes = (("wav音频文件", "*.wav"),))
	if(outputFile != ""):
		if not outputFile.endswith(".wav"):
			outputFile += ".wav"
		HZYS.export(textToRead,
					filePath=outputFile,
					inYsddMode=inYsddMode.get(),
					pitchMult=pitchMultOption.get(),
					speedMult=speedMultOption.get(),
					norm=normAudio.get(),
					reverse=reverseAudio.get())
		messagebox.showinfo("疑似是成功了", "已导出到" + outputFile +"下")


#读取设定文件
def readConfig():
	#若./settings.json存在
	try:
		configFile = open("./settings.json", "r", encoding="utf8")
		configuration = json.load(configFile)
		configFile.close()
		return configuration
	#若不存在
	except:
		configuration = {
			"sourceDirectory": "",
			"ysddSourceDirectory": "",
			"dictFile": "",
			"ysddTableFile": "",
			"numOfThreads": "1",
			"keywordDir":"",
			"roomID": "22603245"
		}
		return configuration


#更改设定
def setConfig(option, texts):
	#读取当前设定
	configuration = readConfig()
	userConfig = ""
	#让用户选择文件或目录
	if (option == "sourceDirectory" or option == "ysddSourceDirectory"):
		userConfig = filedialog.askdirectory(title="选择文件夹") + "/"
	elif (option == "dictFile" or option == "ysddTableFile"or option =="keywordDir"):
		userConfig = filedialog.askopenfilename(title="选择文件",
											filetypes = (("json配置文件", "*.json"),))
	#写入
	configuration[option] = userConfig
	configFile = open("./settings.json", "w", encoding="utf8")
	json.dump(configuration, configFile, ensure_ascii=False, indent="\t")
	configFile.close()
	#更新配置窗口
	optionArray = ["sourceDirectory", "ysddSourceDirectory", "dictFile", "ysddTableFile","keywordDir"]
	texts[optionArray.index(option)].configure(text=configuration[option])
	#更新活字印刷实例配置
	global HZYS
	HZYS = huoZiYinShua("./settings.json")

#两项文本框的设置写入
def commitnumberchange(option, numbers):
	configuration = readConfig()
	userConfig = numbers
	configuration[option] = userConfig
	configFile = open("./settings.json", "w", encoding="utf8")
	json.dump(configuration, configFile, ensure_ascii=False, indent="\t")
	configFile.close()
	messagebox.showinfo("保存设置", "成功")
	configWindow.destroy()

#恢复默认设置
def setConfigtodef():
	configuration = {
			"sourceDirectory": "./sources/",
			"ysddSourceDirectory": "./ysddSources/",
			"dictFile": "./dictionary.json",
			"ysddTableFile": "./ysddTable.json",
			"numOfThreads": "1",
			"keywordDir":"./keyword.json",
			"roomID":"22603245"
		}
	configFile = open("./settings.json", "w", encoding="utf8")
	json.dump(configuration, configFile, ensure_ascii=False, indent="\t")
	messagebox.showinfo("恢复默认设置", "成功")
	configWindow.destroy()

#########################################################

#与主线程通信
def huichuan(huichuantext):
	if iflivemodeon.get() == True:
		try:
			textArea.insert('end',huichuantext)
			textArea.see('end')
		except Exception:
			pass

#语音播报器
class voiceBroadcaster:
	listToRead = []
	locker = Lock()
	global liveactionflag
	#初始化
	def __init__(self, numThread):
		self.numThread = int(numThread)
		self.hzysProcesser = huoZiYinShua("./settings.json")
	
	#添加需要朗读的文本
	def appendText(self, data):
		self.locker.acquire()
		self.listToRead.append(data)
		self.locker.release()
	
	#单个线程的播报
	def __broadcast(self, filePath, stoplivemode):
		global liveactionflag
		while(True):
			if(len(self.listToRead) != 0):
				#从列表中移除要播报的文本
				self.locker.acquire()
				data = self.listToRead.pop(0)
				self.locker.release()
				#用活字印刷播报
				self.hzysProcesser.directPlay(data, filePath,inYsddMode.get(),pitchMultOption.get(),speedMultOption.get(),normAudio.get(),reverseAudio.get())
			if stoplivemode.is_set():
				self.locker.acquire()
				self.listToRead = []
				self.locker.release()
				break
			if (liveactionflag == 0):
				self.locker.acquire()
				self.listToRead = []
				self.locker.release()
				break

	
	#开始播报
	def startOperation(self):
		
		for n in range(1, self.numThread+1):
			if iflivemodeon.get():
				threading.Thread(target=self.__broadcast, args=("./tempOutput/"+str(n)+".wav", stoplivemode, )).start()
			else:
				break

#感谢礼物
def thank(voiceBroad, sender, quantity, giftName):
	global liveactionflag
	if (liveactionflag==1):
		text = "感谢{}的{}个{}\n".format(sender, quantity, giftName)
		mainWindow.after(0, huichuan, text)
		if isgifton.get():
			voiceBroad.appendText(text)


#欢迎观众
def welcome(voiceBroad, audience):
	global liveactionflag
	if (liveactionflag==1):
		text = "欢迎{}进入直播间\n".format(audience)
		mainWindow.after(0, huichuan, text)
		if iswelcomeon.get():
			voiceBroad.appendText(text)



#传话太监
def chuanHua(voiceBroad, speaker, content):
	global liveactionflag
	if (liveactionflag==1):
		text = "\"{}\"说\"{}\"".format(speaker, content)
		mainWindow.after(0, huichuan, text)
		chuanhuaswitch = 1
		if ischuanhuaon.get():
			#关键词过滤	
			if iskeywordspoton.get():
					configFile = open(".\settings.json", encoding="utf8")
					settings = json.load(configFile)
					keywordDir = open(settings["keywordDir"], encoding="utf8")
					for keyword in json.load(keywordDir).items():
							if keyword[0] in text:
								chuanhuaswitch = 0

			if (chuanhuaswitch):
				mainWindow.after(0, huichuan, "\n")
				voiceBroad.appendText(text)	
			else:
				mainWindow.after(0, huichuan, ", 但被屏蔽了\n")

		else:
			mainWindow.after(0, huichuan, "\n")
		



#############################################
#创建设定窗口
def createConfigWindow():
	#窗口属性
	global configWindow
	configWindow = Toplevel(mainWindow)
	configWindow.geometry("480x750")
	configWindow.title("设定")
	try:
		img = ImageTk.PhotoImage(Image.open("./lizi.ico"))
		configWindow.tk.call('wm', 'iconphoto', configWindow._w, img)
	except:
		messagebox.showwarning("警告", "缺失图标")
	#读取设置
	configuration = readConfig()

	#文字
	text1_1 = Label(configWindow, text="活字印刷单字音频存放文件夹：",
					font=font.Font(family="微软雅黑", size=11))
	text1_2 = Label(configWindow, text=configuration["sourceDirectory"])
	text2_1 = Label(configWindow, text="活字印刷原声大碟音频存放文件夹：",
					font=font.Font(family="微软雅黑", size=11))
	text2_2 = Label(configWindow, text=configuration["ysddSourceDirectory"])
	text3_1 = Label(configWindow, text="非中文字符读法字典文件：",
					font=font.Font(family="微软雅黑", size=11))
	text3_2 = Label(configWindow, text=configuration["dictFile"])
	text4_1 = Label(configWindow, text="原声大碟关键词与音频对照表：",
					font=font.Font(family="微软雅黑", size=11))
	text4_2 = Label(configWindow, text=configuration["ysddTableFile"])
	text5_1 = Label(configWindow, text="敏感词词库：",
					font=font.Font(family="微软雅黑", size=11))
	text5_2 = Label(configWindow, text=configuration["keywordDir"])
	text6_1 = Label(configWindow, text="线程数(1-5之间的数字): ",
					font=font.Font(family="微软雅黑", size=11))	
	text7_1 = Label(configWindow, text="房间号: ",
					font=font.Font(family="微软雅黑", size=11))
	texts = [text1_2, text2_2, text3_2, text4_2, text5_2]

	#按钮
	configButton1 = Button(configWindow, text="选择目录", command=lambda: setConfig("sourceDirectory", texts),
					height=1, width=8, font=font.Font(family="微软雅黑", size=11))
	configButton2 = Button(configWindow, text="选择目录", command=lambda: setConfig("ysddSourceDirectory", texts),
					height=1, width=8, font=font.Font(family="微软雅黑", size=11))
	configButton3 = Button(configWindow, text="选择文件", command=lambda: setConfig("dictFile", texts),
					height=1, width=8, font=font.Font(family="微软雅黑", size=11))
	configButton3_1 = Button(configWindow, text="编辑字典", command=lambda: runjsonloader(2),
					height=1, width=8, font=font.Font(family="微软雅黑", size=11))
	configButton4 = Button(configWindow, text="选择文件", command=lambda: setConfig("ysddTableFile", texts),
					height=1, width=8, font=font.Font(family="微软雅黑", size=11))
	configButton4_1 = Button(configWindow, text="编辑列表", command=lambda: runjsonloader(3),
					height=1, width=8, font=font.Font(family="微软雅黑", size=11))
	configButton5 = Button(configWindow, text="选择文件", command=lambda: setConfig("keywordDir", texts),
					height=1, width=8, font=font.Font(family="微软雅黑", size=11))
	configButton5_1 = Button(configWindow, text="编辑词库", command=lambda: runjsonloader(1),
					height=1, width=8, font=font.Font(family="微软雅黑", size=11))
	configButtonx= Button(configWindow, text="全部恢复默认设置", command=lambda: setConfigtodef(),
					height=1, width=16, font=font.Font(family="微软雅黑", size=11))
	configButton6 = Button(configWindow, text="确定", command=lambda: commitnumberchange("numOfThreads", numbers=numberArea1.get()),
					height=1, width=8, font=font.Font(family="微软雅黑", size=11))
	configButton7 = Button(configWindow, text="确定", command=lambda: commitnumberchange("roomID", numbers=numberArea2.get()),
					height=1, width=8, font=font.Font(family="微软雅黑", size=11))


	configFile = open(".\settings.json", encoding="utf8")
	settings = json.load(configFile)
	configFile.close()
	numOfThreads = settings["numOfThreads"]		#线程数
	roomID = settings["roomID"]

	numberArea1 = tk.Entry(configWindow ,width=8,
									font=font.Font(family="微软雅黑", size=10),)
	numberArea2 = tk.Entry(configWindow ,width=8,
									font=font.Font(family="微软雅黑", size=10),)

	#位置
	text1_1.place(x=0, y=0)
	text1_2.place(x=0, y=20)
	text2_1.place(x=0, y=100)
	text2_2.place(x=0, y=120)
	text3_1.place(x=0, y=200)
	text3_2.place(x=0, y=220)
	text4_1.place(x=0, y=300)
	text4_2.place(x=0, y=320)
	
	configButton1.place(x=0, y=40)
	configButton2.place(x=0, y=140)
	configButton3.place(x=0, y=240)
	configButton3_1.place(x=100 ,y=240)
	configButton4.place(x=0, y=340)
	configButton4_1.place(x=100 ,y=340)

	configButtonx.place(x=200, y=340)
	text5_1.place(x=0, y=400)
	text5_2.place(x=0, y=420)
	configButton5.place(x=0, y=440)
	configButton5_1.place(x=100 ,y=440)

	text6_1.place(x=0, y=500)
	numberArea1.place(x=0, y=520)
	numberArea1.insert('end',numOfThreads)
	configButton6.place(x=0, y=540)

	text7_1.place(x=0, y=600)
	numberArea2.place(x=0, y=620)
	numberArea2.insert('end',roomID)
	configButton7.place(x=0, y=640)






#储存生成选项的变量
#-------------------------------------------
inYsddMode = BooleanVar()
normAudio = BooleanVar()
reverseAudio = BooleanVar()
pitchMultOption = DoubleVar()
speedMultOption = DoubleVar()
iflivemodeon = BooleanVar()
iskeywordspoton = BooleanVar()
iswelcomeon = BooleanVar()
ischuanhuaon = BooleanVar()
ishidemsgon = BooleanVar()
isgifton = BooleanVar()

#是否开启直播模式
def livemode():
	global livehidden
	if livehidden:			#直播模式关闭
		keywordCkBt.config(state="disable")
		welcomeCkBt.config(state="disable")
		hidemsgCkBt.config(state="disable")
		chuanhuaCkBt.config(state="disable")
		giftCkBt.config(state="disable")

		actionButton.grid()
		actionButton.grid_remove()		
		cookieButton.config(state="normal")
		cookieButton.grid()
		cookieButton.grid_remove()
		playButton.place(x=70, y=230)
		exportButton.place(x=190, y=230)


		playButton.place(x=70, y=230)
		exportButton.place(x=190, y=230)
		textArea.config(state="normal")	#自动重置文本框
		ishidemsgon.set(False)
		textArea.delete("1.0", "end")
		try:
			stopcookie.set()
		except:
			pass
		try:
			stoplivemode.set()
		except:
			pass
		try:
			stop_thread(livethread)
		except:
			pass
		
		
	else:					#直播模式开启
		exportButton.grid()
		exportButton.grid_remove()
		playButton.grid()
		playButton.grid_remove()

		keywordCkBt.config(state="normal")
		welcomeCkBt.config(state="normal")
		hidemsgCkBt.config(state="normal")
		chuanhuaCkBt.config(state="normal")
		giftCkBt.config(state="normal")

		actionButton.place(x=70, y=230)
		cookieButton.place(x=190, y=230)
		textArea.delete("1.0", "end")
		#livemodeCkBt.config(state="disable")
		try:
			stoplivemode.clear()
		except:
			pass
		try:
			stopcookie.clear()
		except:
			pass
		try:
			myProcess.terminate()
		except:
			pass
	livehidden = not livehidden
	
	

#直播模式壳,解决按钮卡住问题
def livemodelauncher():
	if iflivemodeon.get() == True:
		try:
			stoplivemode.clear()
		except:
			pass
		try:
			stopcookie.set()
		except:
			pass
		try:
			stop_thread(livethread)
		except:
			pass
		try:
			stop_thread(cookieProcess)
			print("登录被打断……")
		except:
			print("使用储存的信息登录…")
		livethread = threading.Thread(target=livemodePlay)

		livethread.start()
	
	livemodeCkBt.config(state="disable")
	cookieButton.config(state="disable")
	actionButton.grid()
	actionButton.grid_remove()
	stopButton.place(x=70, y=230)
	configButton.config(state="disable")
	sleep(2)#缓一缓先
	global liveactionflag
	liveactionflag = 1
pass

#停止按钮
def livemodestop():
	print('已停止\n')
	print('\n')
	stopButton.grid()
	stopButton.grid_remove()
	actionButton.place(x=70, y=230)
	configButton.config(state="normal")
	livemodeCkBt.config(state="normal")
	cookieButton.config(state="normal")
	try:
		stopcookie.clear()
	except:
		pass
	try:
		stoplivemode.set()
	except:
		pass
	try:
		stop_thread(livethread)
	except:
		pass
	global liveactionflag
	liveactionflag = 0
	sleep(2)#缓一缓先

#直播模式主函数，在livethread线程中运行
def livemodePlay():
	configFile = open(".\settings.json", encoding="utf8")
	settings = json.load(configFile)
	configFile.close()
	
	#读取设置
	numOfThreads = settings["numOfThreads"]		#线程数
	roomId = settings["roomID"]	
	userUID =int(load_UID())				#用户的UID
	userSESSDATA = load_cookie()
	#b站cookie获取方式可以参考：https://zmtblog.xdkd.ltd/2021/10/06/Get_bilibili_cookie/
	#1.1更新：新增扫码登录，旧方法已废弃



	#房间号
	#roomId = 22603245
	#roomId = input("最后更新于 2023.10.31  by DJKawaii\n\n基于DSP-8192的项目修改而来\n\n更新地址：https://github.com/flagchess/biliLiveBroadcaster/releases\n\n============\n输入房间号：")
	
	vb = voiceBroadcaster(numOfThreads)
	
	
	broadcaster = biliLiveBroadcaster(roomId,
								   	userUID,		#新增
									userSESSDATA,		#新增
									partial(chuanHua, vb),
									partial(thank, vb),
									partial(welcome, vb),
									stoplivemode
									)
	
	
	#开始运行
	vb.startOperation()
	broadcaster.startBroadcasting()

#更新日志
def updateinfo():
	global updateinfoWindow
	updateinfoWindow = Toplevel(mainWindow)
	updateinfoWindow.geometry("480x400")
	updateinfoWindow.title("关于")
	updateinfoWindow.resizable(False, False)
	update_info_scrolledtext = scrolledtext.ScrolledText(updateinfoWindow, width=55, height=20,
									font=font.Font(family="微软雅黑", size=10))
	update_info_text = getupdateinfo()
	update_info_scrolledtext.place(x=10, y=0)
	update_info_scrolledtext.insert('end', update_info_text)
	update_info_scrolledtext.config(state="disabled")

# 重定向输出
class StdoutRedirector(object):
    
	def __init__(self,text_widget):
		self.text_space = text_widget
        # 将其备份
		self.stdoutbak = sys.stdout
		self.stderrbak = sys.stderr

	def write(self, str):
		try:
			self.text_space.insert('end', str)
			self.text_space.see('end')
		except Exception:
			pass
    
	def restoreStd(self):
        # 恢复标准输出
		sys.stdout = self.stdoutbak
		sys.stderr = self.stderrbak
    
	def flush(self):
		pass

#隐藏日志
def hidemsg():
	if(ishidemsgon.get()):
		textArea.config(state="disabled")
	else:
		textArea.config(state="normal")


#GUI元素
#-------------------------------------------
#文本框
textArea = scrolledtext.ScrolledText(mainWindow, width=55, height=11,
									font=font.Font(family="微软雅黑", size=10))


#按钮们
#播放按钮
playButton = Button(mainWindow, text="直接播放", command=onDirectPlay, height=1, width=8,
					font=font.Font(family="微软雅黑", size=11))

#停止直播
stopButton = Button(mainWindow, text="停止！", command=livemodestop, height=1, width=8,
					font=font.Font(family="微软雅黑", size=11))

#启动直播
actionButton = Button(mainWindow, text="启动！", command=livemodelauncher, height=1, width=8,
					font=font.Font(family="微软雅黑", size=11))

#导出按钮
exportButton = Button(mainWindow, text="导出", command=onExport, height=1, width=8,
					font=font.Font(family="微软雅黑", size=11))

#获取cookie按钮
cookieButton = Button(mainWindow, text="重新登录", command=onTrytologin, height=1, width=8,
					font=font.Font(family="微软雅黑", size=11))

#设置按钮
configButton = Button(mainWindow, text="设置", command=createConfigWindow, height=1, width=8,
					font=font.Font(family="微软雅黑", size=11))


#原声大碟复选框
ysddCkBt = Checkbutton(mainWindow, text="匹配到特定文字时使用原声大碟",
						variable=inYsddMode, onvalue=True, offvalue=False,
						font=font.Font(family="微软雅黑", size=10))


#标准化音频复选框
normCkBt = Checkbutton(mainWindow, text="音量统一",
						variable=normAudio, onvalue=True, offvalue=False,
						font=font.Font(family="微软雅黑", size=10))


#倒放音频复选框
reverseCkBt = Checkbutton(mainWindow, text="频音放倒",
						variable=reverseAudio, onvalue=True, offvalue=False,
						font=font.Font(family="微软雅黑", size=10))

#开启直播模式复选框
livemodeCkBt = Checkbutton(mainWindow, text="直播模式",
						variable=iflivemodeon, onvalue=True, command=livemode, offvalue=False,
						font=font.Font(family="微软雅黑", size=10))

#关键词过滤复选框
keywordCkBt = Checkbutton(mainWindow, text="敏感词屏蔽",
						variable=iskeywordspoton, onvalue=True, offvalue=False,
						font=font.Font(family="微软雅黑", size=10))

#欢迎进场功能复选框
welcomeCkBt = Checkbutton(mainWindow, text="进场欢迎",
						variable=iswelcomeon, onvalue=True, offvalue=False,
						font=font.Font(family="微软雅黑", size=10))

#感谢送礼功能复选框
giftCkBt = Checkbutton(mainWindow, text="感谢礼物",
						variable=isgifton, onvalue=True, offvalue=False,
						font=font.Font(family="微软雅黑", size=10))

#传话功能复选框
chuanhuaCkBt = Checkbutton(mainWindow, text="读弹幕",
						variable=ischuanhuaon, onvalue=True, offvalue=False,
						font=font.Font(family="微软雅黑", size=10))

#隐藏日志复选框
hidemsgCkBt = Checkbutton(mainWindow, text="隐藏日志(用于缓解大量弹幕时的卡顿问题)",
						variable=ishidemsgon, onvalue=True, command=hidemsg,offvalue=False,
						font=font.Font(family="微软雅黑", size=10))


#音调偏移文本
pitchMultLabel = Label(mainWindow, text="音调偏移：",
						font=font.Font(family="微软雅黑", size=10))


#音调偏移滑块
pitchMultScale = Scale(mainWindow, from_=0.5, to=2.0, orient=HORIZONTAL, width=15, length=200,
						resolution=0.1, variable=pitchMultOption,
						font=font.Font(family="微软雅黑", size=9))


#播放速度文本
speedMultLable = Label(mainWindow, text="播放速度：",
						font=font.Font(family="微软雅黑", size=10))


#播放速度滑块
speedMultScale = Scale(mainWindow, from_=0.5, to=2.0, orient=HORIZONTAL, width=15, length=200,
						resolution=0.1, variable=speedMultOption,
						font=font.Font(family="微软雅黑", size=9))



#检查更新相关

checkupdateCkBt = Button(mainWindow, text="更新", command=checkupdate, height=1, width=8,
					font=font.Font(family="微软雅黑", size=8))
checkupdateinfo = Label(mainWindow, 
						text="最后更新于 2023.11.05  by DJKawaii\n基于DSP-8192的项目修改而来\n更新地址：https://github.com/flagchess/biliLiveBroadcaster/releases", 
						font=font.Font(family="微软雅黑", size=10))
updateinfoCkBt = Button(mainWindow, text="关于", command=updateinfo, height=1, width=8,
					font=font.Font(family="微软雅黑", size=8))


#主函数
#-------------------------------------------
if __name__ == "__main__":
	#multiprocess和Windows的兼容
	freeze_support()
	#匹配DPI
	if (system() == "Windows"):
		from ctypes import windll
		windll.shcore.SetProcessDpiAwareness(1)

	#主窗口
	#-----------------------------
	mainWindow.geometry("480x760")
	mainWindow.title("电棍棍活字 ver.2023.11.05")
	mainWindow.resizable(False, False)
	#窗口图标
	try:
		img = ImageTk.PhotoImage(Image.open("./lizi.ico"))
		mainWindow.tk.call('wm', 'iconphoto', mainWindow._w, img)
	except:
		messagebox.showwarning("警告", "缺失图标")



	

	#元素属性
	#-----------------------------
	textArea.place(x=10, y=0)

	playButton.place(x=70, y=230)
	exportButton.place(x=190, y=230)
	configButton.place(x=310, y=230)

	ysddCkBt.place(x=20, y=280)
	normCkBt.place(x=20, y=305)
	reverseCkBt.place(x=20, y=330)
	livemodeCkBt.place(x=20, y=360)


	pitchMultLabel.place(x=20, y=555)
	pitchMultOption.set(1)
	pitchMultScale.place(x=110, y=540)

	speedMultLable.place(x=20, y=595)
	speedMultOption.set(1)
	speedMultScale.place(x=110, y=580)
	
	checkupdateinfo.place(x=20, y=640)
	checkupdateCkBt.place(x=20, y=710)
	updateinfoCkBt.place(x=100, y=710)
	
	keywordCkBt.place(x=20,y=390)
	welcomeCkBt.place(x=20,y=420)
	hidemsgCkBt.place(x=20,y=510)
	chuanhuaCkBt.place(x=20,y=450)
	giftCkBt.place(x=20,y=480)

	keywordCkBt.config(state="disable")
	welcomeCkBt.config(state="disable")
	hidemsgCkBt.config(state="disable")
	chuanhuaCkBt.config(state="disable")
	giftCkBt.config(state="disable")
	
	iswelcomeon.set(True)
	ischuanhuaon.set(True)
	isgifton.set(True)

	#关闭getcookie线程用
	
	stopcookie.clear()

	#关闭直播线程用
	
	stoplivemode.clear()

	liveactionflag = 0
	livehidden = False
	sys.stdout = StdoutRedirector(textArea)

	#检查活字印刷实例是否配置正确
	if not HZYS.configSucceed():
		messagebox.showwarning("初始化活字印刷实例失败", "请检查设置的文件路径是否正确")
	
	#启动主窗口
	mainWindow.mainloop()

	#退出
	try:
		stoplivemode.set()
	except:
		pass

	try:
		stopcookie.set()
	except:
		pass

	try:
		myProcess.terminate()
	except:
		pass


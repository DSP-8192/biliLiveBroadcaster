from biliLiveBroadcaster import *
from huoZiYinShua import *
from threading import Thread
from threading import Lock




#语音播报器
class voiceBroadcaster:
	listToRead = []
	locker = Lock()
	
	#初始化
	def __init__(self, numThread):
		self.numThread = numThread
		self.hzysProcesser = huoZiYinShua("./settings.json")
	
	#添加需要朗读的文本
	def appendText(self, data):
		self.locker.acquire()
		self.listToRead.append(data)
		self.locker.release()
	
	#单个线程的播报
	def __broadcast(self, filePath):
		while(True):
			if(len(self.listToRead) != 0):
				#从列表中移除要播报的文本
				self.locker.acquire()
				data = self.listToRead.pop(0)
				self.locker.release()
				#用活字印刷播报
				self.hzysProcesser.directPlay(data, filePath,ysdd)
	
	#开始播报
	def startOperation(self):
		for n in range(1, self.numThread+1):
			Thread(target=self.__broadcast, args=("./tempOutput/"+str(n)+".wav", )).start()



#感谢礼物
def thank(voiceBroad, sender, quantity, giftName):
	text = "感谢{}的{}个{}".format(sender, quantity, giftName)
	print(text)
	voiceBroad.appendText(text)



#欢迎观众
def welcome(voiceBroad, audience):
	text = "欢迎{}进入直播间".format(audience)
	print(text)
	voiceBroad.appendText(text)



#传话太监
def chuanHua(voiceBroad, speaker, content):
	text = "\"{}\"说\"{}\"".format(speaker, content)
	chuanhuaswitch = 1


	#关键词过滤	
	if iskeywordspoton:
			for keyword in keyworddictionary.items():
					if keyword[0] in text:
						chuanhuaswitch = 0


	if chuanhuaswitch:
		print(text)	
		voiceBroad.appendText(text)	
	else:
		print(text+"，但被屏蔽了")






if __name__ == "__main__":
	#打开设置文件
	configFile = open(".\\settings.json", encoding="utf8")
	settings = json.load(configFile)
	configFile.close()
	
	#读取设置
	sourceDir = settings["sourceDirectory"]		#音频文件存放目录
	dictDir = settings["dictFile"]				#词典存放目录
	numOfThreads = settings["numOfThreads"]		#线程数
	userUID = settings["userUID"]				#用户的UID
	userSESSDATA = settings["usercookie"]			#用户的cookie，仅需要提供SESSDATA，需要与userUID匹配
	isysddon = settings["isysddon"]				#原声大碟是否开启
	iskeywordspoton = settings["iskeywordspoton"]		#关键词过滤是否开启
	keywordDir = open(settings["keywordDir"], encoding="utf8")		#关键词词典目录 		
	#b站cookie获取方式可以参考：https://zmtblog.xdkd.ltd/2021/10/06/Get_bilibili_cookie/

	keyworddictionary = json.load(keywordDir)	

	if isysddon == 1:
		ysdd = True
	else:
		ysdd = False

	#房间号
	roomId = input("输入房间号：")
	
	vb = voiceBroadcaster(numOfThreads)
	
	
	broadcaster = biliLiveBroadcaster(roomId,
								   	userUID,		#新增
									userSESSDATA,		#新增
									partial(chuanHua, vb),
									partial(thank, vb),
									partial(welcome, vb))
	
	
	#开始运行
	vb.startOperation()
	broadcaster.startBroadcasting()
	
	#由于整个main线程被websocket占用，以下代码都不会被执行

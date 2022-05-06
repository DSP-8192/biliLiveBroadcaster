from biliLiveBroadcaster import *
from huoZiYinShua import *
from threading import Thread
from threading import Lock




#语音播报器
class voiceBroadcaster:
	listToRead = []
	locker = Lock()
	
	#初始化
	def __init__(self, numThread, voicePath, dictPath):
		self.numThread = numThread
		self.hzysProcesser = huoZiYinShua(voicePath, dictPath)
	
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
				self.hzysProcesser.playText(data, filePath)
	
	#开始播报
	def startOperation(self):
		for n in range(1, self.numThread+1):
			Thread(target=self.__broadcast, args=(".\\tempOutput\\"+str(n)+".wav", )).start()



#感谢礼物
def thank(voiceBroad, sender, quantity, giftName):
	text = "感谢{}的{}个{}".format(sender, quantity, giftName)
	print(text)
	voiceBroad.appendText(text)



#欢迎观众
def welcome(voiceBroad, audience):
	text = "欢迎{}进入直播间".format(audience)
	print(text)
	#voiceBroad.appendText(text)



#传话太监
def chuanHua(voiceBroad, speaker, content):
	text = "\"{}\"说\"{}\"".format(speaker, content)
	print(text)
	voiceBroad.appendText(text)






if __name__ == "__main__":
	#房间号
	roomId = 866574
	
	
	vb = voiceBroadcaster(1, "E:\\鬼畜\\活字印刷\\sources\\",
						"E:\\鬼畜\\活字印刷\\dictionary.csv")
	
	
	broadcaster = biliLiveBroadcaster(roomId,
									partial(chuanHua, vb),
									partial(thank, vb),
									partial(welcome, vb))
	
	
	#开始运行
	vb.startOperation()
	broadcaster.startBroadcasting()
	
	#由于整个main线程被websocket占用，以下代码都不会被执行

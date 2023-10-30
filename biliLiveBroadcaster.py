import websocket
import brotli
import time
import rel
from threading import Thread
from threading import Lock
import json
import requests
from functools import partial
import timeit



headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3880.400 QQBrowser/10.8.4554.400 '}
#获取真实房间号
def _getRealRoomId(roomId):
	roomInfo = requests.get("https://api.live.bilibili.com/room/v1/Room/room_init?id=" + str(roomId),headers=headers).json()
	realRoomId = roomInfo["data"]["room_id"]
	return realRoomId



#获取key
def _getKey(realRoomId):
	keyInfo = requests.get("https://api.live.bilibili.com/room/v1/Danmu/getConf?room_id=" + str(realRoomId) + "&platform=pc&player=web",headers=headers).json()
	key = keyInfo["data"]["token"]
	return key



#转换byte array为json dictionary
def _raw2Json(raw):
	jsonList = []
	bracketPair = 0
	startPosition = 0
		
	n = 0
	while (n < len(raw)):
		#检测左括号
		if raw[n:n+1] == b"{":
			if bracketPair == 0:	#此处为起始
				startPosition = n	#标记
			bracketPair += 1
		
		#检测右括号
		elif raw[n:n+1] == b"}":
			bracketPair -= 1
			if bracketPair == 0:	#此处为末尾
				jsonList.append(json.loads(raw[startPosition:n+1]))	#截取段落
				n += 16				#跳过两个段落之间的乱码
		
		n += 1
		
	return jsonList		#输出



#解读处理好的数据
def _interpreteJson(data, onReceiveDanmu, onAudienceEnter, giftStat):
	for info in data:
		try:
			match info["cmd"]:
				#弹幕
				case "DANMU_MSG":
					speaker = info["info"][2][1]
					content = info["info"][1]
					onReceiveDanmu(speaker, content)
				
				
				#礼物
				case "SEND_GIFT":
					sender = info["data"]["uname"]
					quantity = info["data"]["num"]
					giftName = info["data"]["giftName"]
					giftStat.add(sender, giftName, quantity)
					
	
				
				#进入直播间
				case "INTERACT_WORD":
					audience = info["data"]["uname"]
					onAudienceEnter(audience)
		
		except:			#无关信息
			pass
		



#收到数据
def _onMessage(onReceiveDanmu, onAudienceEnter, giftStat, ws, message):
	if message[7] == 3:				#用brotli解压缩
		rawData = brotli.decompress(message[16:])[16:]
		
	elif message[7] == 0:			#无需解压缩
		rawData = message[16:]
		
	else:							#与直播间内容无关
		return
	
	try:
		data = _raw2Json(rawData)	#转换为json词典
	except:
		print(rawData)
	
	#解读数据
	_interpreteJson(data, onReceiveDanmu, onAudienceEnter, giftStat)



#处理错误
def _onError(ws, error):
	print("出现错误")
	print(error)



#断开连接
def _onClose(ws, close_status_code, close_msg):
	print("已断开连接")



#发送心跳包
def _sendHeartBeat(ws):
	while(True):
		#每30秒发送一次
		time.sleep(30)
		ws.send(bytearray.fromhex("0000001f0010000100000002000000015b6f626a656374204f626a6563745d"))



#统计收到的礼物
def _collectGiftReceived(giftStat, onReceiveGift):
	while(True):
		time.sleep(1)
		#统计
		giftList = giftStat.extractData()
		
		for gift in giftList:
			onReceiveGift(gift[0], gift[2], gift[1])	#用户自定义函数
		


#已连接上
def _onOpen(realRoomId, key, giftStat, onReceiveGift, ws):
	#编辑确认信息
	verification = b'{"uid":382228653,"roomid":' + bytes(str(realRoomId), "utf-8") + b',"protover":3,"buvid":"XY87B558B729BA2CD745A4FB711BC37C3139D","platform":"danmuji","type":2,"key":"' + bytes(key, "utf-8") + b'"}'
	dataToSend = (len(verification)+16).to_bytes(4, "big") + bytearray.fromhex("001000010000000700000001") + verification
	
	#发送确认信息
	ws.send(dataToSend)
	
	#开启心跳包定时
	Thread(target=_sendHeartBeat, args=(ws,)).start()
	
	#定时统计收到的礼物
	Thread(target=_collectGiftReceived, args=(giftStat, onReceiveGift)).start()
	
	print("已连接")



#收到的礼物列表
class _giftInfoArray:
	def __init__(self):
		self.__data = []		#所有收到的礼物
	
	
	#向列表中添加礼物
	def add(self, sender, giftName, quantity):
		#寻找相同用户赠送的相同礼物并叠加
		for i in range(0, len(self.__data)):
			if(self.__data[i][0:2] == [sender, giftName]):
				self.__data[i][2] += quantity
				self.__data[i][3] = timeit.default_timer()
				return
		#否则新建一个元素
		self.__data.append([sender, giftName, quantity, timeit.default_timer()])
	
	
	#提取数据
	def extractData(self):
		currentTime = timeit.default_timer()
		listToReturn = []
		
		for info in self.__data:
			#超过3秒未赠送同样的礼物（连击停止）
			if(currentTime - info[3] > 3):
				listToReturn.append(info)
				self.__data.remove(info)
		
		return listToReturn
		



class biliLiveBroadcaster:	
	def __init__(self, roomId, onReceiveDanmu, onReceiveGift, onAudienceEnter):
		self.__giftStat = _giftInfoArray()
		self.__roomId = roomId
		self.__onReceiveDanmu = onReceiveDanmu
		self.__onReceiveGift = onReceiveGift
		self.__onAudienceEnter = onAudienceEnter
	
	
	def startBroadcasting(self):
		print("连接中")
		
		#获取真实房间号和key
		self.__realRoomId = _getRealRoomId(self.__roomId)
		self.__key = _getKey(self.__realRoomId)
		
		#开启连接
		websocket.enableTrace(False)
		ws = websocket.WebSocketApp("wss://broadcastlv.chat.bilibili.com/sub",
									on_open = partial(_onOpen,
														self.__realRoomId,
														self.__key,
														self.__giftStat,
														self.__onReceiveGift),
									on_message = partial(_onMessage,
														self.__onReceiveDanmu,
														self.__onAudienceEnter,
														self.__giftStat),
									on_error = _onError,
									on_close = _onClose)
		
		ws.run_forever(dispatcher = rel)
		rel.signal(2, rel.abort)
		rel.dispatch()

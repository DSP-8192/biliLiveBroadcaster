import websocket
import brotli
import time
import rel
from threading import Thread
import json
import requests
from functools import partial



#获取真实房间号
def _getRealRoomId(roomId):
	roomInfo = requests.get("https://api.live.bilibili.com/room/v1/Room/room_init?id=" + str(roomId)).json()
	realRoomId = roomInfo["data"]["room_id"]
	return realRoomId



#获取key
def _getKey(realRoomId):
	keyInfo = requests.get("https://api.live.bilibili.com/room/v1/Danmu/getConf?room_id=" + str(realRoomId) + "&platform=pc&player=web").json()
	key = keyInfo["data"]["token"]
	return key



#转换byte array为json dictionary
def _raw2Json(raw):
	jsonList = []
	bracketPair = 0
	startPosition = 0
		
	
	for n in range(0, len(raw)):
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
	
	return jsonList		#输出



#解读处理好的数据
def _interpreteJson(data, onReceiveDanmu, onReceiveGift, onAudienceEnter):		
	for info in data:
		match info["cmd"]:
			#弹幕
			case "DANMU_MSG":
				speaker = info["info"][2][1]
				content = info["info"][1]
				onReceiveDanmu(speaker, content)
			
			
			#礼物（单次点击）
			case "SEND_GIFT":
				sender = info["data"]["uname"]
				quantity = info["data"]["num"]
				giftName = info["data"]["giftName"]
				if info["data"]["batch_combo_id"] == "" or (giftName != "小心心" and giftName != "辣条"):
					onReceiveGift(sender, quantity, giftName)
			
			
			#礼物（连击）
			case "COMBO_SEND":
				sender = info["data"]["uname"]
				quantity = info["data"]["combo_num"]
				giftName = info["data"]["gift_name"]
				onReceiveGift(sender, quantity, giftName)
			
			
			#进入直播间
			case "INTERACT_WORD":
				audience = info["data"]["uname"]
				onAudienceEnter(audience)



#收到数据
def _onMessage(onReceiveDanmu, onReceiveGift, onAudienceEnter, ws, message):
	if message[7] == 3:			#用brotli解压缩
		rawData = brotli.decompress(message[16:])[16:]
	elif message[7] == 0:		#无需解压缩
		rawData = message[16:]
	else:						#与直播间内容无关
		return
	
	data = _raw2Json(rawData)	#转换为json词典
	#解读数据
	_interpreteJson(data, onReceiveDanmu, onReceiveGift, onAudienceEnter)



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



#已连接上
def _onOpen(realRoomId, key, ws):
	#编辑确认信息
	verification = b'{"uid":0,"roomid":' + bytes(str(realRoomId), "utf-8") + b',"protover":3,"platform":"web","type":2,"key":"' + bytes(key, "utf-8") + b'"}'
	dataToSend = (len(verification)+16).to_bytes(4, "big") + bytearray.fromhex("001000010000000700000001") + verification
	
	#发送确认信息
	ws.send(dataToSend)
	
	#开启心跳包定时
	x = Thread(target=_sendHeartBeat, args=(ws,))
	x.start()
	print("已连接")




class biliLiveBroadcaster:
	def __init__(self, roomId, onReceiveDanmu, onReceiveGift, onAudienceEnter):
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
		ws = websocket.WebSocketApp("wss://tx-sh-live-comet-01.chat.bilibili.com/sub",
									on_open = partial(_onOpen, self.__realRoomId, self.__key),
									on_message = partial(_onMessage,
														self.__onReceiveDanmu,
														self.__onReceiveGift,
														self.__onAudienceEnter),
									on_error = _onError,
									on_close = _onClose)
		
		ws.run_forever(dispatcher = rel)
		rel.signal(2, rel.abort)
		rel.dispatch()

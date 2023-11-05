import webbrowser


def getupdateinfo():
    updateinfo = ("最后更新于 2023.11.05  by DJKawaii\n\
基于@DSP_8192 的项目修改而来\n\
感谢@伏尸王结城友奈 的测试\n\
更新地址：https://github.com/flagchess/biliLiveBroadcaster/releases\n\
\n\
===========\n\
⭐⭐使用方法：\n\
\n\
\"dictionary.json\"里面可以定义非汉字字符的读法\n\
\n\
\"ysddTable.json\"里面可定义关键词与原声大碟的匹配\n\
\n\
\"keyword.json\"里面可以自定义屏蔽词\n\
\n\
首次使用在线模式时需要扫码登录\n\
当弹幕姬无法获取弹幕时可以考虑重新扫码登录\n\
\n\
===========\n\
\n\
\n\
\n\
\n\
\n\
更新日志\n\
===========\n\
\n\
2023.11.05\n\
二维码现在将会生成本地副本\n\
添加了对于使用代理软件时二维码无法弹出的问题的说明\n\
※感谢@Zero原色 @蓝月-亮的反馈\n\
添加了更新日志查看功能\n\
添加了由于开启代理软件导致登录失败时的提示\n\
修复了一些小错误\n\
⭐现在原声大碟、敏感词、字符读法词典可以在GUI界面中编辑\n\
\n\
\n\
===========\n\
\n\
\n\
2023.11.04\n\
⭐将HZYS_GUI与弹幕姬进行了合并\n\
※原本地功能仍可用\n\
※倒放、移调、音量统一现在在在线模式中可用\n\
\n\
倒放、移调、音量统一、原声大碟、屏蔽词、进场欢迎功能现在可在在线模式中启用和关闭\n\
\n\
更换了新的b站登陆方式——扫码登陆\n\
简化了settings.json\n\
※现在仅需GUI界面即可完成所有操作\n\
\n\
⭐新增：在线模式\n\
userUID、userCookie现在为程序自动获取\n\
线程数、房间号现在被整合进GUI界面的设置中\n\
\n\
将所有标准输出重定向到文本框中\n\
\n\
添加了程序说明与更新按钮\n\
新增日志隐藏功能以解决性能问题\n\
\n\
新增：读弹幕、感谢礼物功能开关\n\
※读弹幕、感谢礼物、进场欢迎功能默认开启\n\
===========\n\
\n\
2023.10.31\n\
⭐将HZYS与danmuji两个项目进行了合并\n\
※这使得原声大碟功能可用\n\
\n\
添加了cookie登录以解决弹幕读取不全的问题\n\
\n\
更换了新的b站token接口\n\
※现在在cookie和uid正确设置的情况下可以完整接受所有内容\n\
\n\
修改了loadAudio以解决读取字符报错的问题\n\
将usercookie、userUID、isysddon添加到设置中\n\
忽略了“\"”的报错\n\
\n\
添加了关键词过滤功能和进场欢迎开关\n\
\n\
\n\
===========\n\
\n\
2023.10.28\n\
添加了headers来绕过b站防爬检测\n\
\n\
===========\n\
\n\
2023.09.21\n\
更换登陆方式使弹幕姬可用\n\
\n\
===========\n\
\n\
2023.09.13\n\
更换WSS源使弹幕姬可用\n\
\n\
===========\n\
设置在\"settings.json\"中编辑，其中：\n\
    \"usercookie\"为自己的cookie，只需要填SESSDATA的值。获取方法可以参考：https://zmtblog.xdkd.ltd/2021/10/06/Get_bilibili_cookie/\n\
    \"userUID\"为自己的UID\n\
    \numOfThreads\"为进程数，当值＞1时可实现并行读弹幕效果\n\
   \"ysddTableFile\"、\"dictFile\"分别为原声大碟与非汉字字符的字典路径\n\
    \"sourceDirectory\"、\"ysddSourceDirectory\"分别为汉字与原声大碟音频素材路径\n\
    \"isysddon\"可以开关原声大碟功能（1为开启，0为关闭）\n\
    \"iskeywordspoton\"可以开关关键词屏蔽功能（1为开启，0为关闭）\n\
    \"keywordDir\"为关键词字典路径\n\
    \"iswelcomeon\"可以开关进场欢迎功能（1为开启，0为关闭）\n\
===========\n\
\n\
1.0\n\
\n\
本版本包含命令行版(HZYS.exe)和铸币都会用的GUI版(HZYS_GUI.exe)\n\
命令行版支持原有活字印刷的操作流程，也可以在命令行里直接操作，具体可执行HZYS.exe -h 查看帮助\n\
\n\
\n\
素材目录、词典目录、语音播报线程数量在\"settings.json\"中编辑\n\
\"main.exe\"是打包好的程序，可直接运行\n\
===========")
    return (updateinfo)

#检查更新
def checkupdate():
	webbrowser.open_new("https://github.com/flagchess/biliLiveBroadcaster/releases")
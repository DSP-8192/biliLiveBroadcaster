最后更新于 2023.10.31  by DJKawaii
基于DSP-8192的项目修改而来

===========
"dictionary.json"里面可以定义非汉字字符的读法

"ysddTable.json"里面可定义关键词与原声大碟的匹配

"keyword.json"里面可以自定义屏蔽词

设置在"settings.json"中编辑，其中：
    "usercookie"为自己的cookie，只需要填SESSDATA的值。获取方法可以参考：https://zmtblog.xdkd.ltd/2021/10/06/Get_bilibili_cookie/
    "userUID"为自己的UID
    "numOfThreads"为进程数，当值＞1时可实现并行读弹幕效果
    "ysddTableFile"、"dictFile"分别为原声大碟与非汉字字符的字典路径
    "sourceDirectory"、"ysddSourceDirectory"分别为汉字与原声大碟音频素材路径
    "isysddon"可以开关原声大碟功能（1为开启，0为关闭）
    "iskeywordspoton"可以开关关键词屏蔽功能（1为开启，0为关闭）
    "keywordDir"为关键词字典路径

===========




更新日志



===========

2023.10.31
⭐将HZYS与danmuji两个项目进行了合并
※这使得原声大碟功能可用

添加了cookie登录以解决弹幕读取不全的问题

更换了新的b站token接口
※现在在cookie和uid正确设置的情况下可以完整接受所有内容

修改了loadAudio以解决读取字符报错的问题
将usercookie、userUID、isysddon添加到设置中
忽略了“"”的报错

添加了关键词过滤的功能


===========

2023.10.28
添加了headers来绕过b站防爬检测

===========

2023.9.21
更换登陆方式使弹幕姬可用

===========

2023.9.13
更换WSS源使弹幕姬可用

===========

1.0

本版本包含命令行版(HZYS.exe)和铸币都会用的GUI版(HZYS_GUI.exe)
命令行版支持原有活字印刷的操作流程，也可以在命令行里直接操作，具体可执行HZYS.exe -h 查看帮助


素材目录、词典目录、语音播报线程数量在"settings.json"中编辑
"main.exe"是打包好的程序，可直接运行
===========

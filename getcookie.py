import json
import httpx
import qrcode
import os
from time import sleep


def get_qrurl() -> list:
    """返回qrcode链接以及token"""
    with httpx.Client() as client:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        }
        url = 'https://passport.bilibili.com/x/passport-login/web/qrcode/generate?source=main-fe-header'
        data = client.get(url=url, headers=headers)
    total_data = data.json()
    qrcode_url = total_data['data']['url']
    qrcode_key = total_data['data']['qrcode_key']
    data = {}
    data['url'] = qrcode_url
    data['qrcode_key'] = qrcode_key
    return data


def make_qrcode(data):
    """制作二维码"""
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,
        border=4,
    )
    qr.add_data(data['url'])
    qr.make(fit=True)
    img = qr.make_image(fill_color="black")
    try:
        img.save("Qrcode.png")
    except:
        pass
    try:
        img.show()
    except:
        pass
    print('\n')


def sav_cookie(data, id):
    """用于储存cookie"""
    try:
        with open(f'./{id}.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception as e:
        print(e+'\n')


def getcookienow(stopcookie):
    data = get_qrurl()
    token = data['qrcode_key']
    make_qrcode(data)
    print("等待扫码中")
    print('\n')
    while(1):
        sleep(3)
        with httpx.Client() as client:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        }
            url = f"https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={token}&source=main-fe-header"
            data_login = client.get(url=url, headers=headers)  # 请求二维码状态
            data_login = json.loads(data_login.text)
        code = int(data_login['data']['code'])
        if code == 86090:
            print("已扫码，请在手机上确认登录")
            print('\n')
            break
        if code == 86038:
            print("登录失败，二维码超时")
            print('\n')
            break  
        if stopcookie.is_set():
            break
    while(1):
        if code == 0:
            print("登录成功")
            print('\n')
            cookie = dict(client.cookies)
            sav_cookie(cookie, 'cookie')
            print("成功保存了新的登录状态")
            print('\n')
            break
        if code == 86038:
            break  
        if stopcookie.is_set():
            break
        sleep(3)
        with httpx.Client() as client:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        }
            url = f"https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={token}&source=main-fe-header"
            data_login = client.get(url=url, headers=headers)  # 请求二维码状态
            data_login = json.loads(data_login.text)
        code = int(data_login['data']['code'])
    return code
        



def load_cookie() -> dict:
    """用于加载cookie"""
    try:
        file = open(f'./cookie.json', 'r')
        cookie = dict(json.load(file))
        userSESSDATA = cookie["SESSDATA"]
    except Exception:
        msg = "cookie错误, 请重启程序后重新登录"
        cookie = 'null'
        print(msg)
        print('\n')
    return userSESSDATA

def load_UID() -> dict:
    #用于加载UID
    try:
        file = open(f'./cookie.json', 'r')
        cookie = dict(json.load(file))
        UID = cookie["DedeUserID"]
    except Exception:
        msg = "cookie错误, 请重启程序后重新登录"
        cookie = 'null'
        print(msg)
        print('\n')
    return UID

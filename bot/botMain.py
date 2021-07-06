from flask import Flask, request
import requests
import time,json,re
import os
from bot import botImpl,botutils
from PIL import Image, ImageDraw, ImageFont
app = Flask(__name__)

#打包命令pyinstaller -F botMain.py  -p botImpl.py  -p botutils.py  -p otherImpl.py --hidden-import botImpl  --hidden-import botutils --hidden-import otherImpl

configs={
    # 'url':"http://127.0.0.1:10429",
    'url':"http://192.168.112.132:10429",
    'textcont': 0
}
#清空命令行
def clear():
    if configs['textcont'] == 20:
        os.system('cls')
        configs['textcont'] = 0
    else:
        configs['textcont']+=1

def resetevent():
    while True:
        url = configs.get('url') + '/resetevent'
        data = {
            'sessid':1
        }
        requests.post(url, data=data)
        time.sleep(10)


@app.route('/', methods=['GET', 'POST'])
def index():
    clear()
    data = request.get_data()
    try:
        data = json.loads(data)
        print(f'=======>收到私聊信息' if data['type'] != 'groupmsg' else f'===>接收到群：{data["fromgroup"]["name"]}的消息')
        msg_type(data)
    except:
        pass

# {'type': 'privatemsg', 'fromqq': {'qq': 2996964572, 'qq2': 0, 'nickname': '黑猫'}, 'logonqq': 180802337, 'timestamp': {'recv': 1624788559, 'send': 1624788559}, 'fromgroup': {'group': 0}, 'msg': {'req': 39902, 'seq': 72057595659213644, 'random': 1621285708, 'type': 166, 'subtype': 134, 'subtemptype': 0, 'text': '吃好喝好', 'bubbleid': 0}, 'hb': {'type': 0}, 'file': {'id': '', 'md5': '', 'name': '', 'size': 0}, 'msgpart': {'seq': 0, 'count': 1, 'flag': 0}, 'sessiontoken': ''}
    return '{msg:"成功"}'
#功能的实现
def msg_type(data):
    loginqq = data['logonqq']  #框架qq
    fromqq = data['fromqq']['qq']  #对方qq
    #处理群聊消息
    if data['type'] == 'groupmsg':
        atfromqq = '[@' + str(fromqq) + ']'
        msg = data['msg']['msg']#群消息
        # fromqqname = data['fromqq']['card']#取群昵称
        group = data['fromgroup']['group'] #取群号
        if msg[:4] == '战甲攻略':
            msg = msg[4:]
            botutils.groupmsg(loginqq, group, atfromqq + botImpl.ordis(msg))
        elif msg[:4] == '平原时间':
            try:
                botutils.groupmsg(loginqq, group, atfromqq + botImpl.dayTime())
            except:
                botutils.groupmsg(loginqq, group, atfromqq + '正在进行昼夜更替，稍后查询哦')
        elif msg[:4].lower() == 'wiki':
            msg = msg[4:]
            botutils.groupmsg(loginqq, group, atfromqq + botImpl.wiki(msg))
        elif msg[:4]=='金星温度':
            try:
                botutils.groupmsg(loginqq, group, atfromqq + botImpl.jxwd())
            except:
                botutils.groupmsg(loginqq, group, atfromqq + '金星的温度现在不稳定，请稍后查询哦')
        elif msg == '菜单':
            botutils.groupmsg(loginqq, group, atfromqq + botImpl.caidan())
        elif msg[:2].lower()=='wm':
            mod_rank = ''
            if re.findall(f'[0-9]', msg[2:]):
                mod_ranks = re.findall(f'[0-9]', msg[2:].replace(" ", ""))
                for m in mod_ranks:
                    mod_rank = mod_rank + m
                msg = msg[2:].replace(" ", "").replace(mod_rank, "")
            else:
                mod_rank = '0'
                msg = msg[2:].replace(" ", "")
            botutils.groupmsg(loginqq, group, atfromqq + botImpl.botci(msg, mod_rank))
        elif msg[:2].lower()=='rm':
            msg = msg[2:]
            botImpl.wfrm(loginqq, group,msg)
            # botutils.groupmsg(loginqq, group, atfromqq + botImpl.wfrm(msg))
            # botutils.privatemsg(loginqq,fromqq,botImp.wfrm(msg))
            # botutils.groupmsg(loginqq, group, atfromqq + '查询的信息已通过私聊发送给您')

    #处理私聊消息
    elif data['type'] == 'privatemsg':
        #私聊消息
        fromqqname = data['fromqq']['nickname']#取昵称
        botutils.privatemsg(loginqq,fromqq,fromqqname+',暂时无私聊功能')


if __name__ == '__main__':
    botqq = list(json.loads(botutils.getlogonqq())['ret']['QQlist'])[0]
    # print(json.loads(botutils.getlogonqq()))
    # botqq = input('输入框架qq：')
    print(f'当前框架qq是:{botqq}')
    master = input('主人qq：')
    botutils.privatemsg(botqq,master,'启动成功')
    try:
        app.run(host='127.0.0.1', port=886, debug=False)  # 设置调试模式，生产模式的时候要关掉debug
        app.run()
    except Exception as err:
        print('别问，问就是异常没处理')
    # resetevent()

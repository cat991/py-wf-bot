from flask import Flask, request
import requests
import time,json,re
import os,sys
from bot import botImpl,botutils,otherImpl,jsonAndXml
from PIL import Image, ImageDraw, ImageFont
app = Flask(__name__)
master = True #主人qq

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
    return str(pass_list())
#功能的实现
def msg_type(data):
    loginqq = data['logonqq']  #框架qq
    fromqq = data['fromqq']['qq']  #对方qq
    #处理群聊消息
    if data['type'] == 'groupmsg':
        atfromqq = '[@' + str(fromqq) + ']'
        msg = otherImpl.TraditionalToSimplified(data['msg']['msg'])#群消息,并将繁体转成简体
        # fromqqname = data['fromqq']['card']#取群昵称
        group = data['fromgroup']['group'] #取群号
        #指令输出
        for i in pass_list():
            if msg == i['instruction']:
                    botutils.groupmsg(loginqq, group, atfromqq + i['content'])

        if msg[:2] == '攻略':
            botutils.groupmsg(loginqq, group, atfromqq + botImpl.ordis(msg[2:]))
        elif msg == '地球时间':
            botutils.groupmsg(loginqq,group,atfromqq + botImpl.earthCycle())
        elif msg == '平原时间':
            try:
                botutils.groupmsg(loginqq, group, atfromqq + botImpl.dayTime())
            except:
                botutils.groupmsg(loginqq, group, atfromqq + '正在进行昼夜更替，稍后查询哦')
        elif msg == '仲裁' or msg == '仲裁任务':
            botutils.groupmsg(loginqq, group, atfromqq + botImpl.arbitration())
        elif msg[:4].lower() == 'wiki':
            botutils.groupmsg(loginqq, group, atfromqq + botImpl.wiki(msg[4:]))
        elif msg == '测试':
            pass
            # botutils.groupmsg(loginqq, group, jsonAndXml.ceshi, 'xml')
        elif msg == '二次元':
            botutils.groupmsg(loginqq,group,botImpl.二次元(loginqq,group))
        elif msg[:2] == '遗物':
            botutils.groupmsg(loginqq,group,botImpl.search_relics(loginqq,group,msg[2:]))
        elif '突击' in msg and len(msg) <= 5:
            if msg =='突击':
                botutils.groupmsg(loginqq, group, atfromqq + botImpl.sortie(0))
            elif msg == '国服突击':
                botutils.groupmsg(loginqq, group, atfromqq + botImpl.sortie(1))
            elif msg == '国际服突击':
                botutils.groupmsg(loginqq, group, atfromqq + botImpl.sortie(2))

        elif msg[:4]=='金星温度':
            try:
                botutils.groupmsg(loginqq, group, atfromqq + botImpl.jxwd())
            except:
                botutils.groupmsg(loginqq, group, atfromqq + '金星的温度现在不稳定，请稍后查询哦')
        elif msg == '火卫二' or msg == 'hw2':
            try:
                botutils.groupmsg(loginqq, group, atfromqq + botImpl.hw2())
            except:
                botutils.groupmsg(loginqq, group, atfromqq + '当前查询出现了一点小状况，请联系作者修复')
        elif msg == '菜单':
            botutils.groupmsg(loginqq, group, atfromqq + botImpl.caidan())

        elif msg == '奸商' or msg == '虚空商人':
            try:
                botutils.groupmsg(loginqq, group, atfromqq + botImpl.voidTrader())
            except:
                botutils.groupmsg(loginqq, group, atfromqq + '当前查询出现了一点小状况，请联系作者修复')
        elif msg[:2] == '翻译':
            botutils.groupmsg(loginqq, group,  botImpl.botci(msg[2:]))

        elif msg == '查询口令':
            botutils.groupmsg(loginqq, group,  botImpl.queryAll_json())
        elif msg == '火卫二赏金':
            botutils.groupmsg(loginqq,group,botImpl.allOutmsg('EntratiSyndicate'))
        elif msg == '地球赏金':
            botutils.groupmsg(loginqq,group,botImpl.allOutmsg('Ostrons'))
        elif msg == '金星赏金':
            botutils.groupmsg(loginqq,group,botImpl.allOutmsg('Solaris'))
        elif msg == '达尔沃' or msg =='折扣':
            botutils.groupmsg(loginqq,group,botImpl.allOutmsg('dailyDeals'))
        elif msg == '地球赏金':
            botutils.groupmsg(loginqq,group,botImpl.allOutmsg('Ostrons'))
        elif msg == '入侵':
            botutils.groupmsg(loginqq,group,botImpl.allOutmsg('invasions'))
        elif msg == '活动':
            botutils.groupmsg(loginqq,group,botImpl.allOutmsg('events'))
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
            botutils.groupmsg(loginqq, group, atfromqq + botImpl.wfwm(msg, mod_rank))
        elif msg[:2].lower()=='rm' or msg[:2].lower()=='zk':
            msg = msg[2:]
            botImpl.wfrm(loginqq, group,msg)
            # botutils.groupmsg(loginqq, group, atfromqq + botImpl.wfrm(msg))
            # botutils.privatemsg(loginqq,fromqq,botImp.wfrm(msg))
            # botutils.groupmsg(loginqq, group, atfromqq + '查询的信息已通过私聊发送给您')
        #主人指令，群内添加群
        elif msg[:3] == '添加群' and int(fromqq) == int(master):
             botutils.privatemsg(loginqq, master,botutils.addgroup(loginqq,msg[3:]))
             botutils.groupmsg(loginqq, group, atfromqq + '亲爱的，已经成功添加群聊哦~')
        elif msg[:4] == '新增口令' and int(fromqq) == int(master):
            botutils.groupmsg(loginqq, group, atfromqq + botImpl.password(msg))
        elif msg[:4] == '删除口令' and int(fromqq) == int(master):
            botutils.groupmsg(loginqq, group, botImpl.delete_json(msg[4:]))
        elif msg[:2] == '公告' and int(fromqq) == int(master):
            botImpl.group_announcement(loginqq, msg[2:])
            botutils.groupmsg(loginqq,group,"群公告发送完毕")

    #处理私聊消息
    elif data['type'] == 'privatemsg':
        if int(fromqq) == int(master):
            msg = otherImpl.TraditionalToSimplified(data['msg']['text'])#获取私聊消息,并将繁体转成简体
            if msg[:3] == '添加群':
                botutils.privatemsg(loginqq, master,botutils.addgroup(loginqq, msg[3:]))
                botutils.privatemsg(loginqq,fromqq,'成功添加群聊')
            elif msg[:2] == '公告':
                botImpl.group_announcement(loginqq, msg[2:])
                botutils.groupmsg(loginqq, master, "群公告发送完毕")

        else:
            #私聊消息
            fromqqname = data['fromqq']['nickname']#取昵称
            botutils.privatemsg(loginqq,fromqq,fromqqname+',暂时无私聊功能')


#获取指令内容
def pass_list():
    botpath = os.path.dirname(os.path.realpath(sys.argv[0]))+'\\botqq.json'
    try:
        with open(botpath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
    except:
        word = [{
            'instruction': '口令',
            'content': '新增的功能哦~'
        }]
        with open(botpath, 'w', encoding='utf-8') as f2:
            json.dump(word, f2, ensure_ascii=False)
            f2.close()
    return item_list



if __name__ == '__main__':
    botqq = list(json.loads(botutils.getlogonqq())['ret']['QQlist'])[0]
    for i in pass_list():
        if i['instruction'] == 'master':
           print(f'当前框架qq是:{botqq}\n主人qq：{i["content"]}')
           master = i['content']
    if master == True:
        print(f'当前框架qq是:{botqq}')
        master = input('主人qq：')
        word = {
            'instruction': 'master',
            'content': master
        }
        botImpl.write_json(word)

    try:
        app.run(host='0.0.0.0', port=886, debug=False)  # 设置调试模式，生产模式的时候要关掉debug
        app.run()
        botutils.privatemsg(botqq, master, '启动成功')
    except Exception as err:
        print('别问，问就是异常没处理')
    # resetevent()

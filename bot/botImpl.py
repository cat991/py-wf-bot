import json,time,re
import requests
from bot import otherImpl
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}


#奥迪斯攻略接口
def ordis(msg):
    data={
        'text': msg
    }
    text = requests.post('https://api.null00.com/ordis/getTextMessage',data=data).text
    text = json.loads(text)['msg']
        # .replace('\/r\/n','\n')
    return text

#warframe维基
def wiki(search):
    resp = requests.get('https://warframe.huijiwiki.com/api.php?action=opensearch&search='+search,headers=headers)
    resp = json.loads(resp.text)
    msg = '你要找的是\n'
    for title, url in zip(resp[1], resp[3]):
        msg+=f'{title}\n{url}\n'
    return msg

#平原时间，星际战甲
def dayTime():
    resp = requests.get('https://api.null00.com/world/ZHCN')
    resp = json.loads(resp.text)
    day = resp['cetus']['day']
    times = resp['cetus']['cetusTime']
    if day:
        times = int(times) - int(time.time())
        hours = time.strftime('%H', time.localtime(times))
        hours = int(hours)-8
        time1 = time.strftime('%M分%S秒', time.localtime(times))
        return f'\t\n现在时间是--白天--\n剩余时间:{hours}时{time1}'
    else:
        times = times - int(time.time())
        hours = time.strftime('%H', time.localtime(times))
        hours = int(hours)-8
        time1 = time.strftime('%M分%S秒', time.localtime(times))
        return f'\t\n现在时间是--晚上--\n剩余时间:{hours}时{time1}'


#奸商信息
def voidTrader():
    resp = requests.get('https://api.null00.com/world/ZHCN')
    resp = json.loads(resp.text)
    arrivals = resp['voidTrader']['arrivals']
    times = resp['voidTrader']['expiry']
    place = resp['voidTrader']['node']
    # times = int(times) - 28800000
    if arrivals:
        guofu = f'\t\n-------国服-------\n奸商已抵达：{place}'
    else:
        times = times - int(time.time())
        hours = time.strftime('%H', time.localtime(times))
        hours = int(hours) - 8
        time1 = time.strftime('%M分%S秒', time.localtime(times))
        guofu = f'\t\n-------国服-------\n奸商到来时间还剩：{hours}时{time1} \n地点：{place}'
    guojifu = requests.get('http://nymph.rbq.life:3000/wf/robot/voidTrader').text
    return f'{guofu}\n\n-------国际服-------\n{guojifu}'


#星际战甲金星温度判断
def states(state):
    if state == 1:
        return '极寒'
    elif state == 2:
        return '寒冷'
    elif state == 3:
        return '温暖'
    elif state == 4:
       return '寒冷'
    elif state ==5:
        return '极寒'


#星际战甲金星温度
def jxwd():
    resp = requests.get('https://api.null00.com/world/ZHCN')
    resp = json.loads(resp.text)
    times = resp['solaris']['solarisExpiry']
    state = resp['solaris']['state']
    times =times-int(time.time())
    time1 = time.strftime('%M分%S秒', time.localtime(times))
    return f'现在温度是--{states(int(state))}--\n{time1}后切换\n--{states(state+1)}--'
#火卫二时间
def hw2():
    resp = requests.get('http://nymph.rbq.life:3000/wf/robot/cambionCycle').text
    if 'fass' in resp:
        return resp.replace('fass','毁灭(fass)')
    else:
        return resp.replace('vome','秩序(vome)')


#warframe玄骸紫卡交易
def wfrm(loginqq, group,str):
    resp = requests.get(f'http://nymph.rbq.life:3000/rm/robot/{str.replace(" ","")}')
    otherImpl.toImage(loginqq, group,resp.text,'wfrm')


#warframe物品交易
def wfwm(msg, mod_rank):
    str = {}
    str['itme'] = botci(msg)
    str['mod_rank'] = int(mod_rank)
    str['str'] = msg
    try:
        resp = requests.get(f'https://api.warframe.market/v1/items/{str["itme"].replace(" ", "_").lower()}/orders?include=item')
        resp = json.loads(resp.text)
    except:
        return str['itme']
    orderslist = resp['payload']['orders']
    orderslist = sorted(orderslist, key=lambda x: x["platinum"], reverse=False)
    orderre = f'\t\n默认展示价格最低前10个\n你要搜索的是：{str["str"]} \n翻译：{str["itme"]}'
    cont = 0 #统计10个
    number = 0 #统计全部价格
    conts = 0 #统计全部
    for i in orderslist:
        if i['order_type'] == "sell":
            number += i['platinum']
            conts += 1
        if str['mod_rank'] == 0:
            if i['order_type'] == "sell" and cont < 10 and i['user']['status'] != "offline":  # 判断是否是出售商品
                cont += 1
                baijin = i['platinum']  # 获取到的白鸡
                name = i['user']['ingame_name']  # 获取到的游戏名
                state = i['user']['status']
                orderre += f' \n白金:{baijin}--游戏id: {name}'
        else:
            if i['order_type'] == "sell" and cont < 10 and i['user']['status'] != "offline" and i['mod_rank'] == str['mod_rank']:  # 判断是否是出售商品
                cont += 1
                baijin = i['platinum']  # 获取到的白鸡
                name = i['user']['ingame_name']  # 获取到的游戏名
                state = i['user']['status']
                orderre += f' \n白金:{baijin}--游戏id: {name}--物品等级:{str["mod_rank"]}级'
            # orderre += f'\n在线状态：{"在线" if state != "offline" else "离线"}\n白金:{baijin}---游戏昵称: {name}'

    if cont == 0:
        return '\t\n没有该商品或并没有查到该等级的商品'
    else:
        return orderre + f'\n总出售人数{conts}人，平均:{int(number/conts)}白鸡'

#翻译&warframe查字典
def botci(str):
    resp = requests.get(f'http://nymph.rbq.life:3000/dict/tran/robot/{str.replace(" ","")}').text
    num = 0
    # ret ={}
    txt = ''
    for lis in resp.split('\n'):
        num +=1
        if num ==2:
            itme = re.findall(f'\\[(.*?)]',lis)
            txt = itme[0]
            # txt = itme[0].replace(' ', '_').lower()
            # ret={
            #     'itme':itme[0].replace(' ', '_').lower(),
            #      'str':itme[0],
            #     'mod_rank':mod_rank
            # }
    try:
        # return wfwm(ret)
        return txt
    except:
        return resp

#菜单
def caidan():
    return f'\t\n你要的菜单来了\n---菜单---\n战甲攻略  关键词\nwiki  关键词\n物品交易: wm \n紫卡玄骸交易：rm\n平原时间 \n金星温度 \n火卫二 \n虚空商人 \n ↓↓↓主人指令↓↓↓\n添加群 + 群号'
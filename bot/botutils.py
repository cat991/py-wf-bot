import requests
import win32api,win32con
import json
configs={
    'url':"http://127.0.0.1:10429",
    'textcont': 0
}

#获取桌面路径
def get_desktop():
    key =win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',0,win32con.KEY_READ)
    return win32api.RegQueryValueEx(key,'Desktop')[0]
#发送私聊消息
def privatemsg(login,toqq,text):
    url =  configs.get('url')+ '/sendprivatemsg'
    print('====>触发私聊消息')
    data = {
    'logonqq':login,
    'toqq':toqq,
    'msg':text
    }
    requests.post(url,data=data)
#获取框架登陆qq信息
def getlogonqq():
    url = configs.get('url')+'/getlogonqq'
    return requests.post(url).text
def uploadgrouppic(logonqq,group,path):
    url = configs.get('url')+'/uploadgrouppic'
    data={
        'logonqq': logonqq,
        'group': group,
        'type':"path",
        'pic':get_desktop()+'\\'+path+'.png'
    }
    print(data['pic'])
    resp = requests.post(url, data=data).text
    print(resp)
    resp = json.loads(resp)
    groupmsg(logonqq,group,resp['ret'])
#发送群聊消息
def groupmsg(logonqq,group,msg):
    url = configs.get('url') + '/sendgroupmsg'
    print('====>触发群消息' )
    data = {
        'logonqq': logonqq,
        'group':group,
        'msg':msg,
        'anonymous':'false'
    }
    requests.post(url, data=data)
# -*- coding: UTF-8 -*-

import requests
from lxml import etree
from multiprocessing.dummy import Pool
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

loginurl='http://kdjw.hnust.cn/kdjw/Logon.do?method=logon'#登录地址
captchaurl='http://kdjw.hnust.cn/kdjw/verifycode.servlet'#验证码
headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}
s = requests.session()
##### 获取到验证码并保存
checkcodecontent = s.get(captchaurl,headers=headers)
with open('checkcode.gif', 'wb') as f:
    f.write(checkcodecontent.content)
print('验证码已写入到本地！')
os.startfile('checkcode.gif')
checkcode = raw_input('请输入验证码：')

payload = {
    'dlfl':'0',
    'USERNAME':'1405040113',#input('请输入账号：'),
    'PASSWORD': '140015',#raw_input('请输入密码：'),
    'RANDOMCODE': checkcode,
    'x':'0',
    'y':'0'
}
data={
    'kksj':'2016-2017-2',
    'kcxz':'04',
    'kcmc':'',
    'xsfs':'qbcj',
    'ok':''
}
#kcxz :02公共基础课 03专业基础课 04专业课 05公共选修课
cj='http://kdjw.hnust.cn/kdjw/xszqcjglAction.do?method=queryxscj'
response = s.post(loginurl, data=payload, headers=headers)

html=s.post(cj,data=data)
# print(html.text)
selector=etree.HTML(html.text)
tr=selector.xpath('//div[@id="mxhDiv"]/table[@border="1"]/tr')
cj=[]
for each in tr:
    tds=each.xpath('td')
    cj_c={
        'kc':tds[5].text,
        'cj':tds[6].text,
        'xf':tds[11].text
    }
    cj.append(cj_c)
    print "课程名称:"+tds[5].text, "成绩:"+tds[6].text,"学分:"+tds[11].text
    # print(tds)
    # for td in tds:
    #     print(td)
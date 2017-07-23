#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from PIL import  Image
import requests
import time

class scoreSpider(object):
    def __init__(self, user, pwd):
        self.url_img = 'http://kdjw.hnust.cn/kdjw/verifycode.servlet' #验证码地址
        self.url_login = 'http://kdjw.hnust.cn/kdjw/Logon.do?method=logon' #登陆地址
        self.url_grade = 'http://kdjw.hnust.cn/kdjw/xszqcjglAction.do?method=queryxscj' #查成绩地址
        self.url_kebiao = 'http://kdjw.hnust.cn/kdjw/tkglAction.do?method=goListKbByXs&xnxqh={}&zc={}' #查课表地址
        self.user = user
        self.pwd = pwd
        self.fontMods = []

    def fontInit(self):
        for i in range(1, 4):
            self.fontMods.append((str(i), Image.open("./font/%d.bmp" % i)))
        self.fontMods.append(('b', Image.open("./font/b.bmp")))
        self.fontMods.append(('c', Image.open("./font/c.bmp")))
        self.fontMods.append(('m', Image.open("./font/m.bmp")))
        self.fontMods.append(('n', Image.open("./font/n.bmp")))
        self.fontMods.append(('v', Image.open("./font/v.bmp")))
        self.fontMods.append(('x', Image.open("./font/x.bmp")))
        self.fontMods.append(('z', Image.open("./font/z.bmp")))

    def recognize(self, f):
        self.fontInit()
        im = Image.open(f).convert('1')
        # result = "./result/"
        yzm = ''
        for i in range(4):
            x = 3 + i * 10
            y = 4
            target = im.crop((x, y, x + 10, y + 12))
            points = []
            for mod in self.fontMods:
                diffs = 0
                for yi in range(12):
                    for xi in range(10):
                        if mod[1].getpixel((xi, yi)) != target.getpixel((xi, yi)):
                            diffs += 1
                points.append((diffs, mod[0]))
            points.sort()
            yzm += points[0][1]
            # result += points[0][1]
        # result += ".png"
        # im.save(result)
        return yzm

    def login(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }
        s = requests.session()
        r = s.get(self.url_img, headers=headers)
        with open('yzm.png', 'wb') as file:
            file.write(r.content)
        yzm = self.recognize('yzm.png')
        # user = input('input username:')
        # psw = input('input password:')
        data = {
            'dlfl': '0',
            'PASSWORD': self.pwd,
            'RANDOMCODE': yzm,
            'USERNAME': self.user,
            'x': '0',
            'y': '0'
        }

        s.post(self.url_login, data=data)
        return s

    def getKebiao(self, term, week):
        s = self.login()
        kebiao = []
        wb = s.get(self.url_kebiao.format(term, week))
        soup = BeautifulSoup(wb.text, 'html.parser')
        trs = soup.select('table#kbtable tr')
        for index, tr in enumerate(trs[1:6]):
            line = []
            for item in tr.select('td > div:nth-of-type(2)'):
                data = item.get_text(' ', strip=True).split(' ')
                res = ''
                if (data[0]):
                    res = {
                        'weeks': data[2],
                        'course': data[0],
                        'place': data[3],
                        'index': '{}-{}节课'.format(2 * index + 1, 2 * index + 2)
                    }
                line.append(res)
            kebiao.append(line)
        weekShort = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
        res = {}
        for day in range(7):
            dayCourse = []
            for row in kebiao:
                if (row[day]):
                    dayCourse.append(row[day])
            res[weekShort[day]] = dayCourse
        return res

    def getData(self, s):
        def cmp(x):
            return x['term']
        code = {
            'xsfs': 'qbcj'
        }

        wb = s.post(self.url_grade, data=code)
        soup = BeautifulSoup(wb.text, 'html.parser')
        response = soup.select('tr.smartTr')
        list = []

        for td in response:
            td = td.select('td')
            dict = {
                # 'num': td[1].text,
                # 'stu_num': td[2].text,
                # 'name': td[3].text,
                'term': td[4].text,
                'course': td[5].text,
                'score': td[6].text,
                # 'property': td[8].text,
                # 'category': td[9].text,
                # 'period': td[10].text,
                'credit': td[11].text
            }
            list.append(dict)
        list.sort(key = cmp, reverse=True)
        return list

    def getScore(self):
        s = self.login()
        data = self.getData(s)
        last_term = ''
        list = []
        index = -1
        for each in data:
            term = each.get('term')
            if term != last_term:
                list.append([])
                last_term = term
                index += 1
            list[index].append(each)
        return list

    def getScoreWX(self):
        s = self.login()
        data = self.getData(s)
        next_term = ''
        content = ''
        flag = 1
        for each in data:
            term = each.get('term')
            if term != next_term:
                if flag == 1:
                    content += term + '\n'
                    flag = 2
                else:
                    content += '\n' + term + '\n'
                next_term = term
            content += each.get('course') + '  ' + each.get('score') + '\n'
        return content
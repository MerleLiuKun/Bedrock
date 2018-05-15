# -*- coding: utf-8 -*-
import math
import time
import hashlib

#


class TransCookie(object):
    def __init__(self, cookie):
        self.cookie = cookie

    def string_to_dict(self):
        """
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        """
        item_dict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            item_dict[key] = value
        return item_dict


def getASCP():
    t = int(math.floor(time.time()))
    e = hex(t).upper()[2:]
    m = hashlib.md5()
    m.update(str(t).encode(encoding='utf-8'))
    i = m.hexdigest().upper()

    if len(e) != 8:
        AS = '479BB4B7254C150'
        CP = '7E0AC8874BB0985'
        return AS, CP
    n = i[0:5]
    a = i[-5:]
    s = ''
    r = ''
    for o in range(5):
        s += n[o] + e[o]
        r += e[o + 3] + a[o]

    AS = 'A1' + s + e[-3:]
    CP = e[0:3] + r + 'E1'
    return AS, CP

# def get_signature(c_time):
#     chrome.get('https://www.toutiao.com/ch/internet/')
#     signature = chrome.execute_script('return TAC.sign({})'.format(c_time))
#     return signature

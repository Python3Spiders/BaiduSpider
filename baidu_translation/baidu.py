import re
import js
import time
import js2py
import requests

class baidu():
    def __init__(self):
        self.session = requests.Session()
        # Chrome : 设置-->高级-->内容设置-->cookie-->查看所有cookie和网站数据-->baidu.com的cookie
        self.session.cookies.set('BAIDUID', '19288887A223954909730262637D1DEB:FG=1;')
        self.session.cookies.set('PSTM', '%d;' % int(time.time()))
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }
        self.data = {
            'query': '',
            'simple_means_flag': '3',
            'sign': '',
            'token': '',
        }
        self.url = 'https://fanyi.baidu.com/v2transapi'

    def translate(self, word):
        self.data['query'] = word
        self.data['token'], gtk = self.getTokenGtk()
        self.data['token'] = '6482f137ca44f07742b2677f5ffd39e1'
        self.data['sign'] = self.getSign(gtk, word)
        res = self.session.post(self.url, data=self.data)
        return res.json()['trans_result']['data'][0]['result'][0][1]

    def getTokenGtk(self):
        url = 'https://fanyi.baidu.com/'
        res = requests.get(url, headers=self.headers)
        token = re.findall(r"token: '(.*?)'", res.text)[0]
        gtk = re.findall(r";window.gtk = ('.*?');", res.text)[0]
        return token, gtk

    def getSign(self, gtk, word):
        evaljs = js2py.EvalJs()
        js_code = js.js_code
        js_code = js_code.replace('null !== i ? i : (i = window[l] || "") || ""', gtk)
        evaljs.execute(js_code)
        sign = evaljs.e(word)
        return sign

if __name__ == "__main__":
    t = baidu()
    to_translate = input('请输入待翻译词:')
    while True:
        result = t.translate(to_translate)
        print('{}的翻译结果是:{}'.format(to_translate,result))
        to_translate = input('请继续输入待翻译词，或者回车结束')
        # 翻译结束
        if len(to_translate) == 0:
            print('本次翻译结束')
            break

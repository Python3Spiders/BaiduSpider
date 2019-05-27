# -*- coding: utf-8 -*-
# author:           inspurer(月小水长)
# pc_type           lenovo
# create_time:      2019/5/22 21:40
# file_name:        scrapy.py
# github            https://github.com/inspurer
# qq邮箱            2391527690@qq.com
# 微信公众号         月小水长(ID: inspurer)

import requests, math,os.path
from set import USER_NAME,PASSWORD
from bs4 import BeautifulSoup
BASE_PATH = 'imgs'
if not os.path.exists(BASE_PATH):
    os.mkdir(BASE_PATH)
def main():
    session = login()
    keyword = input('请输入你想要爬取图片的贴吧：')
    # 构建贴吧主页url
    index_url = "https://tieba.baidu.com/f?kw={}".format(keyword)
    # 获取帖子总页数（经过测试发现不登录的情况下是无法获取帖子数目的）
    total_page = get_total_page(index_url, session)
    # 获取每一页的帖子url 放在列表中
    all_tiezi_urls = get_tiezi_url_list(total_page, keyword, session)
    """
    以“关键字/数字序号.jpg”的形式保存爬取的图片
    判断文件夹是否存在 如果不存在 则先创建文件夹
    """
    img_dir = BASE_PATH+'/' + keyword
    if (not os.path.exists(img_dir)):
        os.mkdir(img_dir)
    i = 0
    for each in all_tiezi_urls:
    # 获取帖子的具体内容
        res = session.get(each)
        # 从中解析出图片url
        soup = BeautifulSoup(res.text, 'html.parser')
        img_urls = soup.find_all('img', class_='BDE_Image')
        for img in img_urls:
            i = i + 1
            with open(img_dir + "/" + str(i) + '.jpg', 'wb') as f:
                print("开始下载第" + str(i) + "张图片" )
                f.write(session.get(img.attrs['src']).content)
                print("图片下载成功！")
# 模拟登陆的方法
def login():
    # 登录所需的参数
    login_data = {
    'username': USER_NAME,
    'password': PASSWORD,
    'u': 'https://tieba.baidu.com/index.html?traceid=#',
    #tb 贴吧，表明是从百度贴吧登录百度站点的
    'tpl': 'tb',
    'staticpage': 'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
    'isPhone': 'false',
    'charset': 'utf-8',
    'callback': 'parent.bd__pcbs__3rjsif'
    }
    # 构造所需的headers
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
        }
    # 登录的url
    baidu_loginurl = "https://passport.baidu.com/v2/api/?login"
    # 创建session
    session = requests.session()
    # 模拟登陆
    session.post(baidu_loginurl, data=login_data, headers=headers)
    # 创建session
    return session
# 获取总页数的方法

def get_total_page(url, session):
 # 获取网页内容
    res = session.get(url)
    # 解析出帖子总数
    soup = BeautifulSoup(res.text, 'html.parser')
    tiezi_total_num = soup.find('span', class_='card_infoNum').text
    tiezi_total_num = int(tiezi_total_num.replace(',', ''))
    # 贴吧默认每页50条帖子
    page_size = 50
    # 计算出总页数
    total_page = math.ceil(tiezi_total_num / page_size)
    return total_page
# 获取帖子url列表的方法
def get_tiezi_url_list(total_page, keyword, session):
    """
    为了节省爬取时间 此处只爬取前1页
    """
    all_tiezi_urls = []
    for i in range(1, 2):
    # 构造url
        tiezi_url = "http://tieba.baidu.com/f?kw=" + keyword + "&pn=" + str((i - 1) * 50)
        # 获取每一页的帖子url
        tiezis = get_tiezi_list(tiezi_url, session)
        # 将所有帖子url加入到all_tiezi_urls中
        all_tiezi_urls.extend(tiezis)
    return all_tiezi_urls

# 获取当前页所有帖子列表的方法
def get_tiezi_list(tiezi_url, session):
    # 获取某个帖子列表页面的网页内容
    res = session.get(tiezi_url)
    # 从中解析出每个帖子的链接
    soup = BeautifulSoup(res.text, 'html.parser')
    a_list= soup.find_all('a', class_='j_th_tit ')
    # 拼接出真实的帖子链接
    static_tiezi_urls = []
    for each in a_list:
        static_tiezi_urls.append("http://tieba.baidu.com" + each.attrs['href'])
    return static_tiezi_urls

if __name__ == '__main__':
    main()

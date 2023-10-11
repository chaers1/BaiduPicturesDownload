# encoding=utf8
import os
import sys
import time
import random
import requests
from multiprocessing import Value
from fake_useragent import UserAgent

# 创建一个请求头
headers = {"User-agent": UserAgent().random,  # 这是一个随机生成一个代理的请求，可以每一次请求都可以随机生一个代理为了应对网站的反爬
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
           "Connection": "keep-alive"}  # 定义请求头，模拟浏览器请求使用，这个应用需要在发送请求的时候添加进参数内
"""创建一个类用于数据存储和爬取"""
class Core():
    def __init__(self, name=None, sdtas=None, sdta=None, drive_letter=None, names=None):
        super().__init__()
        self.name = name
        self.sdtas = sdtas
        self.sdta = sdta
        self.drive_letter = drive_letter  # 指定盘符
        self.parent_dir = "Baiduimages"
        self.names = names
        self.count = Value('i', 1)

    """图片获取和存储函数"""
    def tian_pian(self):

        """存储模块"""
        datas = os.path.join(f"{self.drive_letter}:/{self.parent_dir}/{self.names}")
        if not os.path.exists(datas):
            os.makedirs(datas)
        """图片爬取模块"""
        for i in range(self.sdtas, self.sdta):
            url = f"https://image.baidu.com/search/acjson?tn=resultjson_com&word={self.name}&pn={i * 30}"  # name是对应网站中搜索关键字的，i是网站的页数
            name_url = requests.get(url, headers=headers)  # 向网站发送get请求
            json_name = name_url.json()  # 将请求到的数据进行转换
            name_date_list = json_name['data']  # 获取到 json_name 内的数据只要data内的数据，然后在data内的数据再次进行转换和提炼
            for data in name_date_list[:-1]:
                frompagetitleencs = data['fromPageTitleEnc']  # 获取图片名字
                replaceurls = data['replaceUrl']  # 获取图片的下载链接，这里需要做一个循环

                for object1 in replaceurls:  # 这里添加一个循环，因为replaceUrls中的ObjURL才可以找到高清的大图
                    try:
                        Objurl = object1['ObjURL']
                        sys.stdout.write(f"第【{self.count.value}】张图片【{frompagetitleencs}】下载成功.\n")
                        with self.count.get_lock():  # 获取锁，保证计数器的线程安全
                            self.count.value += 1
                        img_Objurl = requests.get(Objurl).content
                        frompagetitleencs = frompagetitleencs[:200]
                        with open(os.path.join(datas, frompagetitleencs + ".png"), "wb") as f:
                            f.write(img_Objurl)
                            time.sleep(random.uniform(0.1, 0.4))
                    except Exception as e:
                        with open("baogao.log", 'a') as fo:
                            fo.write(str(e))
        sys.stdout.write(f"您需要的{self.name}图片已经全部下载完成，保存路径是【{datas}】复制粘贴即可找到图片位置.\n")



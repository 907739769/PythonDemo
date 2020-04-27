# -*- coding: utf-8 -*-
import os
import random
import re
import socket
import threading
import time
import urllib.request
import urllib.parse
from urllib.error import HTTPError

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent',
                      'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10')]
urllib.request.install_opener(opener)

socket.setdefaulttimeout(30)

downloaddir = 'D:\\Python-Crawler-Warehouse\\tags\\'

downloadcount = 0

cookies = r'__cfduid=de242687d45160a0dfaf13ae256f95f3d1567420791; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6Im9IQ3daYkZUSWRpT0NYWDhxeDBWRWc9PSIsInZhbHVlIjoiWjVlOGJoMUNXU1RUUWFtdnR0U09LTXY5MHFSTnU3bVRPSFlwcXpaTFQ1SVpIbWFFUXF3UVp3bWhwKzVvQnZLS2c0WEErTElcL3hnZFQyamdaTmk4cHp4b0piVU1nbXRaK0lyK0hyZ25ZcVAwcG9tWFc5blJwMXVQaDV4SXY4MjZqSjJcL2RoZU05M09WaFJqK2VnNHpHNEtnanZNZDBUaTNPYmpJazRXQ3NFeGVITVJ2VlhUTStqOEFBVWVHbE1ZK3QiLCJtYWMiOiI0YjAyN2FkOTY1NTU0MzAxZDhkZmRlOWQ1OTBjZDZiYzRlZTg5OTNhMGZiNzA3ZmY5MGM3NDg1ODNiOGUzNDg4In0%3D; XSRF-TOKEN=eyJpdiI6ImRrcmluVE5mc2RTbmE3eDJJbXMwK3c9PSIsInZhbHVlIjoicTlzd2hvS2xDcHBINVJkYVZON2hxbFhNZGtRcGp6aDVMNTN1KzdDT0R6eWd2RmJJXC96dUFGNWM5U3JPbDlWV0YiLCJtYWMiOiJlN2YyZTkwODUzNjQ1OTgyOTE0ODNjMzgxYWIwNzJjOTJjZTFjN2ZhYmMyYzhiNDhkN2E3MGUzNTNhYmZkNGJlIn0%3D; wallhaven_session=eyJpdiI6ImYxQzNZMDhcL0VqU044U2I3TUFGVVwvZz09IiwidmFsdWUiOiIxOXoyYnN4WVwvR0libXpFQm1ZUmxcL0NMcjM4WHlCVDlxbDVcL2czb1RhNWNWdlwvdzFHenFVYjJkQ3R5NkdpdUxJTCIsIm1hYyI6IjE4ZDAyYWIyYTk3ZjQyNTJlMjBjODhiODFjNjhlODM3OGUzNDQ2ZDNiNTI1NDEwOWFhMDcxNGYwNDYwMjhmZjYifQ%3D%3D'


# 定义一个getHtml()函数
def getHtml(url):
    print(url.full_url)
    try:
        page = urllib.request.urlopen(url)  # urllib.request.urlopen()方法用于打开一个URL地址
        htmls = page.read().decode('utf-8')  # read()方法用于读取URL上的数据
        return htmls
    except:
        print("未知错误" + url)
        return ""


def getImg(htmlx):
    reg = r'data-src="(.+?\.jpg)" src='  # 正则表达式，得到图片地址
    imgre = re.compile(reg)  # re.compile() 可以把正则表达式编译成一个正则表达式对象.
    imglist = re.findall(imgre, htmlx)  # re.findall() 方法读取html 中包含 imgre（正则表达式）的数据
    print(imglist)

    for imgurl in imglist:
        imgurl = urlformat(imgurl)
        time.sleep(random.randrange(1, 5))
        urldownload(imgurl)


def urldownload(url):
    try:
        download(url)
    except socket.timeout:
        print("Download", url, 'timeout')
        delfile(url)
    # except ContentTooShortError:
    #     download(url)
    except:
        print("UNKNOWN ERROR", url)
        delfile(url)
    else:
        global downloadcount
        downloadcount += 1
        print('Download Over', url)
        print('Downloaded', downloadcount)


def download(url):
    try:
        name = url[url.rindex("/"):]
        urllib.request.urlretrieve(url, downloaddir + name, downloadinfo)
    except HTTPError:
        print('.jpg is not exist , down .png')
        url = url.replace(".jpg", ".png", 1)
        name = url[url.rindex("/"):]
        urllib.request.urlretrieve(url, downloaddir + name, downloadinfo)


def delfile(url):
    name = url[url.rindex("/"):]
    path = downloaddir + name
    if os.path.exists(path):
        os.remove(path)
    else:
        path = path.replace(".jpg", ".png", 1)
        if os.path.exists(path):
            os.remove(path)


def urlformat(url):
    url = url.replace("th", "w", 1).replace("/small/", "/full/", 1).replace('/orig/', '/full/')
    temp = url.rindex("/")
    url = url[0:temp] + url[temp:].replace("/", "/wallhaven-", 1)
    return url


def downloadinfo(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('Downloading', '%.2f%%' % per)


def mkdirdownload(tags):
    global downloaddir
    downloaddir = downloaddir.replace("tags", tags)
    if not os.path.lexists(downloaddir):
        os.mkdir(downloaddir)


def justdoit(url):
    req = urllib.request.Request(url)
    req.add_header('cookie', cookies)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36')
    getImg(getHtml(req))


if __name__ == '__main__':
    tags = str(input("输入要下载的内容："))
    mkdirdownload(tags)
    html = "https://wallhaven.cc/search?q=" + tags + "&categories=111&purity=100&sorting=date_added&order=desc&page=###"
    for x in range(1, 2):
        t = threading.Thread(target=justdoit, args=(html.replace("###", str(x)),))
        t.start()
        time.sleep(random.randint(5, 10))

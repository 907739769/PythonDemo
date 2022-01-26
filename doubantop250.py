import requests
from lxml import etree

__headers = {
    'Referer': 'https://movie.douban.com/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}


def get_movie_html():
    res = requests.get("https://movie.douban.com/top250?start=0&filter=", headers=__headers)
    html = etree.HTML(res.text)
    result = html.xpath('//*[@id="content"]/div/div[1]/ol//li/div/div[2]/div[1]/a/@href')
    print(result)


def get_imdb():
    res = requests.get("https://movie.douban.com/subject/1292052/", headers=__headers)
    html = etree.HTML(res.text)
    result = html.xpath('//*[@id="info"]/span[15]/text()')
    print(result)


if __name__ == '__main__':
    get_imdb()

import requests
import re
import json
from lxml import etree


class Spider:
    def __init__(self, headers, url, fp=None, title='', date=''):
        self.headers = headers
        self.url = url
        self.fp = fp
        self.title = title
        self.date = date

    def open_file(self):
        self.fp = open(r'/address/%s/%s' %
                       (self.date, self.title+'.doc'), 'w', encoding='utf8')

    # 获取带id参数的资讯url内容,一个参数是资讯url，一个参数是由文章列表传来的资讯类型
    def __getArticleDetail_id__(self):
        jsUrlTemp = self.url.split('?id=')
        jsUrl = jsUrlTemp[0]  # 带id参数的详情url地址
        return requests.get(url=jsUrl).text.lstrip("callback(").rstrip(')')

    def parse_home_data(self):
        ex = '"url":"(.*?)"'
        home_data = self.__getArticleDetail_id__()
        print(re.findall(ex, home_data))
        return re.findall(ex, home_data)

    def parse_detail_data(self):
        detail_url = self.parse_home_data()
        i = 0
        for url in detail_url:
            i += 1
            try:
                jsUrlTemp = url.split('?id=')[1]
                jsurl = jsUrlTemp.split('&item_id=')[0]
                self.url = 'networkaddress'+jsurl+'.js'
                detail_data = json.loads(self.__getArticleDetail_id__())
                self.date = detail_data['publish_time'].split('-')[0]
                self.title = detail_data['title']
                tree = etree.HTML(detail_data['content'])
                content_list = tree.xpath('.//p/text()')
                if len(content_list) < 5:
                    content_list = tree.xpath('.//p/span/text()')

                self.open_file()
                self.fp.write(
                    detail_data['title'] + '\n' + '\n\n  '.join(content_list) + '\n\n')
            except Exception as e:
                print(e)
                continue

    def close_file(self):
        self.fp.close()

    def run(self):
        self.parse_detail_data()
        self.close_file()


if __name__ == '__main__':
    headers = {
        'Host': 'address',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    }
    url = 'json.address'
    spider = Spider(url=url, headers=headers)
    spider.run()

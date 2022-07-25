import requests
import re
import json
from lxml import etree


class Spider:
    def __init__(self, headers, url, fp=None, title='', date=''):
        self.headers = headers
        self.url = url
        self.fp = fp
        self.title = ''
        self.date = ''

    def open_file(self):
        self.fp = open(r'/address/%s/%s' %
                       (self.date, self.title + '.doc'), 'w', encoding='utf8')

    def get_data(self):
        return requests.get(url=self.url).text

    def parse_home_data(self):
        ex = '"static_page_url":"(.*?)"'
        home_data = self.get_data()
        return re.findall(ex, home_data)

    def parse_detail_data(self):
        detail_url = self.parse_home_data()
        i = 0
        for url in detail_url:
            i += 1
            try:
                jsUrlTemp = url.rsplit('/')
                self.url = jsUrl = "http:" + '//' + \
                    jsUrlTemp[2] + '/' + jsUrlTemp[3] + '/data' + \
                    jsUrlTemp[4].replace('html',  'js')
                detail_data = self.get_data()
                detail_data = detail_data.replace('globalCache = ', '')[:-1]
                dic_data = json.loads(detail_data)
                first = list(dic_data.keys())[0]
                self.date = dic_data[first]['detail']['original_time'].split(
                    '-')[0]
                title = dic_data[first]['detail']['frst_name']
                self.title = title
                content_html = dic_data[first]['detail']['content_list'][0]['content']
                tree = etree.HTML(content_html)
                content_list = tree.xpath('.//p/text()')
                if len(content_list) < 5:
                    content_list = tree.xpath('.//p/span/text()')
                print(len(content_list))
                # self.open_file()
            except Exception as e:
                print(e)
                continue
            self.fp.write(title + '\n' + '\n\n'.join(content_list) + '\n\n')

    def close_file(self):
        self.fp.close()

    def run(self):
        self.open_file()
        self.parse_detail_data()
        self.close_file()


if __name__ == '__main__':
    headers = {
        'Host': '',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    }
    url = ''
    spider = Spider(url=url, headers=headers)
    spider.run()

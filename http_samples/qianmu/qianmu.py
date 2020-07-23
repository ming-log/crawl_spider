import time
import requests
from lxml import etree


start_url = 'http://qianmu.iguye.com/2018USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D'
download_pages = 0


def fetch(url):
    """请求并下载网页"""
    r = requests.get(url)
    if r.status_code != 200:
        r.raise_for_status()
    global download_pages
    download_pages += 1
    return r.text.replace('\t', '')


def parse_univerity(url):
    """处理大学详情页面"""
    selector = etree.HTML(fetch(url))
    data = {}
    data['name'] = selector.xpath('//div[@id="wikiContent"]/h1/text()')[0]
    table = selector.xpath(
        '//div[@id="wikiContent"]/div[@class="infobox"]/table')
    if table:
        table = table[0]
        keys = table.xpath('.//td[1]/p/text()')
        cols = table.xpath('.//td[2]')
        values = [' '.join(col.xpath('.//text()')) for col in cols]
        if len(keys) != len(values):
            return None
        data.update(zip(keys, values))
        return data


def process_data(data):
    """处理数据"""
    if data:
        print(data)


if __name__ == '__main__':
    start_time = time.time()
    # 1. 请求入口页面
    selector = etree.HTML(fetch(start_url))
    # 2. 提取列表页面的链接
    links = selector.xpath('//div[@id="content"]//tr[position()>1]/td[2]/a/@href')
    for link in links:
        if not link.startswith('http://qianmu.iguye.com'):
            link = 'http://qianmu.iguye.com/%s' % link
        # 3. 提取详情页的信息
        data = parse_univerity(link)
        # 4. 处理信息
        process_data(data)

    cost_seconds = time.time() - start_time
    print('downloaded %s pages , cost %.2f seconds' %
          (download_pages, cost_seconds))


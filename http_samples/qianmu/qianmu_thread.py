import time
import threading
from queue import Queue
import requests
from lxml import etree


start_url = 'http://qianmu.iguye.com/2018USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D'
link_queue = Queue()
threads_num = 50
threads = []
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


def download():
    while True:
        # 阻塞直到从队列里获取一条消息
        link = link_queue.get()
        if link is None:
            break
        data = parse_univerity(link)
        process_data(data)
        link_queue.task_done()
        print('remaining queue: %s' % link_queue.qsize())


if __name__ == '__main__':
    start_time = time.time()
    # 1. 请求入口页面
    selector = etree.HTML(fetch(start_url))
    # 2. 提取列表页面的链接
    links = selector.xpath('//div[@id="content"]//tr[position()>1]/td[2]/a/@href')
    for link in links:
        if not link.startswith('http://qianmu.iguye.com'):
            link = 'http://qianmu.iguye.com/%s' % link
        link_queue.put(link)

    # 启动线程，并将线程对象放入一个列表保存
    for i in range(threads_num):
        t = threading.Thread(target=download)
        t.start()
        threads.append(t)
    # 阻塞队列，直到队列被清空
    link_queue.join()
    # 向队列发送N个None，以通知线程退出
    for i in range(threads_num):
        link_queue.put(None)
    # 退出线程
    for t in threads:
        t.join()

    cost_seconds = time.time() - start_time
    print('downloaded %s pages , cost %.2f seconds' %
          (download_pages, cost_seconds))



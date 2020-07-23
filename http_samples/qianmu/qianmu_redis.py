import sys
import time
import signal
import threading
from queue import Queue
import requests
from lxml import etree
import redis

start_url = 'http://qianmu.iguye.com/2018USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D'
link_queue = Queue()
threads_num = 10
threads = []
download_pages = 0
r = redis.Redis(host='127.0.0.1')
thread_on = True


def fetch(url):
    """请求并下载网页"""
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            r.raise_for_status()
        global download_pages
        download_pages += 1
        return r.text.replace('\t', '')
    except Exception:
        print('error raised when fetch %s' % url)

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


def download(i):
    while thread_on:
        link = r.lpop('qianmu.queue')
        if link:
            data = parse_univerity(link)
            process_data(data)
            print('remaining queue: %s' % r.llen('qianmu.queue'))
        time.sleep(0.2)
    print('Thread-%s eixt now' % i)


def sigint_handler(signum, frame):
    print('received Ctrl+C, wait for exit gracefully')
    global thread_on
    thread_on = False


if __name__ == '__main__':
    start_time = time.time()
    if len(sys.argv) > 1:
        start_url = sys.argv[1]
        # 1. 请求入口页面
        selector = etree.HTML(fetch(start_url))
        # 2. 提取列表页面的链接
        links = selector.xpath('//div[@id="content"]//tr[position()>1]/td[2]/a/@href')
        for link in links:
            if not link.startswith('http://qianmu.iguye.com'):
                link = 'http://qianmu.iguye.com/%s' % link
            if r.sadd('qianmu.seen', link):
                r.rpush('qianmu.queue', link)
    else:
        # 启动线程，并将线程对象放入一个列表保存
        for i in range(threads_num):
            t = threading.Thread(target=download, args=(i+1,))
            t.start()
            threads.append(t)

        signal.signal(signal.SIGINT, sigint_handler)
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



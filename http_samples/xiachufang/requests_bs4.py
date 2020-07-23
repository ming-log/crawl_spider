import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.26 Safari/537.36"
headers = {'User-Agent': user_agent}
r = requests.get('http://www.xiachufang.com/', headers = headers )
soup = BeautifulSoup(r.text)

img_list = []
for img in soup.select('img'):
    if img.has_attr('data-src'):
        img_list.append(img.attrs['data-src'])
    else:
        img_list.append(img.attrs['src'])

# 初始化下载文件目录
image_dir = os.path.join(os.curdir, 'images')
# if not os.path.isdir(image_dir):
#     os.mkdir(image_dir)

for img in img_list[0:-2]:
    if img:
        o = urlparse(img)
        filename = o.path[1:].split('@')[0]
        filepath = os.path.join(image_dir, filename)
        if not os.path.isdir(os.path.dirname(filepath)):
            os.mkdir(os.path.dirname(filepath))
        url = '%s://%s/%s' % (o.scheme, o.netloc, filename)
        print(url)
        resp = requests.get(url)
        with open(filepath, 'wb') as f:
            for chunk in resp.iter_content(1024):#每次往里面写1024个字节
                f.write(chunk)
import re
import os
from io import BytesIO
from urllib.parse import urlparse
from pycurl import Curl


buffer = BytesIO()
c = Curl()
c.setopt(c.URL, 'http://www.xiachufang.com/')
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()
body = buffer.getvalue()
text = body.decode('utf-8')
print(text)


img_list = re.findall(r'src=\"(http://i2\.chuimg\.com/\w+\.jpg)',
                      text)

# 初始化下载文件目录
image_dir = os.path.join(os.curdir, 'images')
# if not os.path.isdir(image_dir):
#     os.mkdir(image_dir)

for img in img_list[::-1]:
    o = urlparse(img)
    filename = o.path[1:]
    filepath = os.path.join(image_dir, filename)
    if not os.path.isdir(os.path.dirname(filepath)):
        os.mkdir(os.path.dirname(filepath))
    url = '%s://%s/%s' % (o.scheme, o.netloc, filename)
    print(url)
    with open(filepath, 'wb') as f:
        c = Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()
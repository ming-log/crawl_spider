import requests

# GET请求
r = requests.get('http://httpbin.org/get')
print(r.status_code, r.reason)
print('GET请求', r.text)
# 带参数的GET请求
r = requests.get('http://httpbin.org/get', params={'a': '1', 'b': '2'})
print('带参数的GET请求', r.json())

#POST请求
r = requests.post('http://httpbin.org/post', data={'a': '1'})
print('POST请求', r.json())

# 自定义headers请求
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) ' \
     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77' \
     ' Safari/537.36'
headers = {'User-Agent': ua}
r = requests.get('http://httpbin.org/headers', headers=headers)
print('自定义headers请求', r.json())

# 带cookies的请求
cookies = dict(userid='123456', token='xxxxxxxxxxxxxxxxxxxx')
r = requests.get('http://httpbin.org/cookies', cookies=cookies)
print('带cookies的请求', r.json())

# Basic-auth认证请求
r = requests.get('http://httpbin.org/basic-auth/guye/123456', auth=('guye', '123456'))
print('Basic-auth认证请求', r.json())

# 主动抛出状态码异常
bad_r = requests.get('http://httpbin.org/status/404')
print(bad_r.status_code)
bad_r.raise_for_status()

#使用requests.Session对象请求
# 创建一个Session对象
s = requests.Session()
# session对象会保存服务器返回的set-cookies头信息里面的内容
s.get('http://httpbin.org/cookies/set/userid/123456789')
s.get('http://httpbin.org/cookies/set/token/xxxxxxxxxxxxxxxxxx')
# 下一次请求会将本地所有的cookies信息自动添加到请求头信息里面
r = s.get('http://httpbin.org/cookies')
print('检查session中的cookies', r.json())


# 在requests中使用代理
print('不使用代理：', requests.get('http://httpbin.org/ip').json())
print('使用代理：', requests.get(
    'http://httpbin.org/ip',
    proxies={'http': 'http://iguye.com:41801'}
).json())

r = requests.get('http://httpbin.org/delay/4', timeout=5)
print(r.text)

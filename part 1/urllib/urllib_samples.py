import urllib.request
import json


# 接收一个字符串作为参数
r = urllib.request.urlopen('http://httpbin.org/get')
# 读取response的内容
text = r.read()
print(text)
# http返回状态码和msg
print(r.status, r.reason)
r.close()

# 返回的内容是json格式，直接用Load函数加载
obj = json.loads(text)
print(obj)

# r.headers是一个HTTPMessage对象
# print(r.headers)
for k, v in r.headers._headers:
    print('%s: %s' % (k, v))


## 不添加User-Agent时的返回     >>> user-agent:  Python-urllib/3.6
req = urllib.request.Request('http://httpbin.org/user-agent')
r = urllib.request.urlopen(req)
resp = json.load(r)
# 打印出httpbin网站返回信息里的user-agent
print("user-agent: ", resp["user-agent"])


## 添加User-Agent时的返回      >>>  返回对应的ua
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) ' \
     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77' \
     ' Safari/537.36'
# 添加自定义的头信息
req = urllib.request.Request('http://httpbin.org/user-agent')
req.add_header('User-Agent', ua)
# 接收一个urllib.request.Request对象作为参数
r = urllib.request.urlopen(req)
resp = json.load(r)
# 打印出httpbin网站返回信息里的user-agent
print("user-agent: ", resp["user-agent"])


# 发起带basic auth的请求
# 带用户名密码认证
auth_handler = urllib.request.HTTPBasicAuthHandler()
auth_handler.add_password(realm='Fake Realm',
                          uri='http://httpbin.org',
                          user='guye',
                          passwd='123456')
opener = urllib.request.build_opener(auth_handler)
urllib.request.install_opener(opener)
r = urllib.request.urlopen('http://httpbin.org/basic-auth/guye/123456')
print(r.read().decode('utf-8'))

# 使用GET参数
params = urllib.parse.urlencode({'spam': 1, 'eggs':2, 'bacon': 2})
url = 'http://httpbin.org/get?%s' % params
with urllib.request.urlopen(url) as f:
    print(json.load(f))

# 使用POST方法传递参数
data = urllib.parse.urlencode({'name': '小明', 'age': 2})  #变成能够通过url传输的形式
data = data.encode()   #编码为bytes
with urllib.request.urlopen('http://httpbin.org/post', data) as f:
    print(json.load(f))

# 使用代理IP请求远程url
proxy_handler = urllib.request.ProxyHandler({
                        'http': 'http://iguye.com:41801'
                    })
# proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()  #带用户名密码认证的代理
opener = urllib.request.build_opener(proxy_handler)
r = opener.open('http://httpbin.org/ip')
print(r.read())


# urlparse模块
o = urllib.parse.urlparse('http://httpbin.org/get')
type(o)
dir(o)
o.port

o.scheme

o.username

o.geturl()

o.encode()

o.fragment
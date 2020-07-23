from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
# 创建一个BeautifulSoup对象
soup = BeautifulSoup(html_doc)
print(soup.prettify())
soup.title
type(soup.title)
dir(soup.title)
soup.title.text
#取出第一个a标签的所有属性
soup.a.attrs
# 取出a标签的href属性
soup.a.attrs['href']
#判断是否有class属性
soup.a.has_attr('class')
#取出第一个p标签下的所有的子节点
soup.p.children
# 取出来的结果是一个迭代器，所以用list转换一下
list(soup.p.children)
list(soup.p.children)[0]
list(soup.p.children)[0].text

# 取出本页面内所有的链接
for a in soup.find_all('a'):
    print(a.attrs['href'])

# 取出id=link3的那个节点
soup.find(id='link3')
# 取出页面内所有的文本
soup.get_text()

# 支持CSS选择器
# 查找类名为story的节点
soup.select('.story')
# 查找id=link1的节点
soup.select('#link1')


soup_lxml = BeautifulSoup(html_doc, 'lxml')
print('##' * 10, soup_lxml.a)
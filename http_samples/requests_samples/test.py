import urllib.request


auth_handler = urllib.request.HTTPBasicAuthHandler()
auth_handler.add_password(realm='Fake Realm',
                          uri='http://httpbin.org',
                          user='guye',
                          passwd='123456')
opener = urllib.request.build_opener(auth_handler)
urllib.request.install_opener(opener)
r = urllib.request.urlopen('http://httpbin.org/basic-auth/guye/123456')
print(r.read().decode('utf-8'))
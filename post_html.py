
import urllib.request
import urllib.parse
from urllib.error import URLError,HTTPError

url='https://api.weibo.com/oauth2/access_token'
values={'client_id':'339837652',    #key
        'client_secret':'92299b8986fbc70e2c67d5f14075a3bc',#secret
        'grant_type':'authorization_code',
        'redirect_uri':'www.baidu.com',#回执网页
        'code':'1ecb3d82b39ead686dc8d842e44da491'}#回执代码

url_values=urllib.parse.urlencode(values)
print(url_values)

url_values=url_values.encode(encoding='UTF8')
full_url=urllib.request.Request(url,url_values)

try:
    response=urllib.request.urlopen(full_url) 
    print(response.read())
except HTTPError as e:
    print('Error code:',e.code) 
except URLError as e:
    print('Reason',e.reason)

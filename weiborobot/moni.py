#! /usr/bin/env python
#coding=utf-8
import urllib
import urllib2
import cookielib
import base64
import re
import json
import hashlib
import weibo
import os
import time
import binascii 

cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)
postdata = {
    'entry': 'weibo',
    'gateway': '1',
    'from': '',
    'savestate': '7',
    'userticket': '1',
    'ssosimplelogin': '1',
    'vsnf': '1',
    'vsnval': '',
    'su': '',
    'service': 'miniblog',
    'servertime': '',
    'nonce': '',
    'pwencode': 'wsse',
    'sp': '',
    'encoding': 'UTF-8',
    'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
    'returntype': 'META'
}

def get_servertime():
    url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=dW5kZWZpbmVk&client=ssologin.js(v1.3.18)&_=1329806375939'
    data = urllib2.urlopen(url).read()
    p = re.compile('\((.*)\)')
    try:
        json_data = p.search(data).group(1)
        data = json.loads(json_data)
        servertime = str(data['servertime'])
        nonce = data['nonce']
        return servertime, nonce
    except:
        print ('Get severtime error!')
        return None

def get_pwd(pwd, servertime, nonce):
    pwd1 = hashlib.sha1(pwd).hexdigest()
    pwd2 = hashlib.sha1(pwd1).hexdigest()
    pwd3_ = pwd2 + servertime + nonce
    pwd3 = hashlib.sha1(pwd3_).hexdigest()
    return pwd3

def get_user(username):
    username_ = urllib.quote(username)
    username = base64.encodestring(username_)[:-1]
    return username


def login():
    username = '18710517099' #你的新浪微博账号
    pwd = 'yangshuainet'        #你的新浪微博密码  
    url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.3.18)'
    try:
        servertime, nonce = get_servertime()
    except:
        return
    global postdata
    postdata['servertime'] = servertime
    postdata['nonce'] = nonce
    postdata['su'] = get_user(username)
    postdata['sp'] = get_pwd(pwd, servertime, nonce)
    postdata = urllib.urlencode(postdata)
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}
    req  = urllib2.Request(
        url = url,
        data = postdata,
        headers = headers
    )
    result = urllib2.urlopen(req)
    text = result.read()
    p = re.compile('location\.replace\(\"(.*?)\"\)')
    try:
        login_url = p.search(text).group(1)
        
        urllib2.urlopen(login_url)
        print ('Login sucess!')
    except:
        print ('Login error!')
    	



    
    """cmd = 'sudo cat /sys/bus/w1/devices/28-*/w1_slave'    
    temp = os.popen(cmd).read()
  
    time_s =  time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))
  
    temp1 = temp[-6:-3]
    temp2 = (float(temp1))/10
    temp3 = str(temp2)    
    text1 = "  当前室温："
    text2 = "°C"
    """
    sta_key = "status="
    token = "&access_token=2.00PfQ8CE09Svz3930c0656c0_yppwC"
    #mdb = sta_key+time_s+text1+temp3+text2+token
    mdb = sta_key+'xxxxxxxxxxxxxx'+token

    req = urllib2.Request(url='https://api.weibo.com/2/statuses/update.json',data = mdb)
    result = urllib2.urlopen(req)
    print (result) 


login()

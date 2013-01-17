# -*- coding: utf-8 -*- 
import os
import urllib,urllib2,time,hashlib
import sae
#需要的第三方库
import web
from lxml import etree

#TOKEN 到微信公众平台自己设置
config={"TOKEN":'fengyoujing',
    "WEIXIN": 'weixin'}
        
urls = (
    '/weixin', 'weixin'
)

app_root = os.path.dirname(__file__)

class weixin:
    TOKEN = "fengyoujing"

    
    #GET方法，主要用来注册url
    def GET(self):
        data = web.input()
        #以下是微信公众平台请求的参数
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr

        #自己定义的 TOKEN
        token = config['TOKEN']
        
        #对微信发送的请求，做验证
        tmplist = [ token, timestamp, nonce ]
        tmplist.sort()
        tmplist.sort()
        tmpstr = ''.join( tmplist )
        hashstr = hashlib.sha1( tmpstr ).hexdigest()

        #如果相等，返回验证信息
        if hashstr == signature:
            return echostr
        
        #如果不相等，返回错误，并打印调试信息
        print signature,timestamp,nonce
        print tmpstr,hashstr
        return 'Error' + echostr


    def POST(self):
        #接收微信的请求内容
        data = web.data()
        #解析XML内容
        root = etree.fromstring( data )
        child = list( root )
        recv = {}
        for i in child:
            recv[i.tag] = i.text

        #print data
        #print recv
        YOUDAO_KEY = 696996954
        YOUDAO_KEY_FROM = "Feng123"
        YOUDAO_DOC_TYPE = "xml"
        queryStr = recv['Content']

        raw_youdaoURL = "http://fanyi.youdao.com/openapi.do?keyfrom=%s&key=%s&type=data&doctype=%s&version=1.1&q=" % (YOUDAO_KEY_FROM,YOUDAO_KEY,YOUDAO_DOC_TYPE)
        youdaoURL = "%s%s" % (raw_youdaoURL,urllib2.quote(queryStr))

        req = urllib2.Request(url=youdaoURL)
        result = urllib2.urlopen(req).read()
        rootElem = etree.fromstring( result )
        replyContent = ''
        if rootElem.tag == 'youdao-fanyi':
            for child in rootElem:
                # 错误码
                if child.tag == 'errorCode':
                    if child.text == '20':
                        return 'too long to translate\n'
                    elif child.text == '30':
                        return 'can not be able to translate with effect\n'
                    elif child.text == '40':
                        return 'can not be able to support this language\n'
                    elif child.text == '50':
                        return 'invalid key\n'

                # 查询字符串
                elif child.tag == 'query':
                    replyContent = "%s%s\n" % (replyContent, child.text)

                # 有道翻译
                elif child.tag == 'translation': 
                    replyContent = '%s%s\n%s\n' % (replyContent, '-' * 3 + u'youdao' + '-' * 3, child[0].text)

                # 有道词典-基本词典
                elif child.tag == 'basic': 
                    replyContent = "%s%s\n" % (replyContent, '-' * 3 + u'basic' + '-' * 3)
                    for c in child:
                        if c.tag == 'phonetic':
                            replyContent = '%s%s\n' % (replyContent, c.text)
                        elif c.tag == 'explains':
                            for ex in c.findall('ex'):
                                replyContent = '%s%s\n' % (replyContent, ex.text)

                # 有道词典-网络释义
                elif child.tag == 'web': 
                    replyContent = "%s%s\n" % (replyContent, '-' * 3 + u'web' + '-' * 3)
                    for explain in child.findall('explain'):
                        for key in explain.findall('key'):
                            replyContent = '%s%s\n' % (replyContent, key.text)
                        for value in explain.findall('value'):
                            for ex in value.findall('ex'):
                                replyContent = '%s%s\n' % (replyContent, ex.text)
                        replyContent = '%s%s\n' % (replyContent,'--')

        textTpl = """<xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[%s]]></MsgType>
            <Content><![CDATA[%s]]></Content>
            <FuncFlag>0</FuncFlag>
            </xml>"""
        echostr = textTpl % (recv['FromUserName'], recv['ToUserName'],recv['CreateTime'],recv['MsgType'],replyContent)
        return echostr
        
       
app = web.application(urls, globals()).wsgifunc()

application = sae.create_wsgi_app(app)
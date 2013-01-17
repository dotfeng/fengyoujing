风油精
===========
微信公众账号+SAE（Django/web.py）+有道翻译  自动翻译助手。

参考 http://blog.csdn.net/liushuaikobe/article/details/8453716

包含Django和web.py两个版本，选择其一即可。

1、申请SAE账号：http://sae.sina.com.cn/

2、申请有道API key：http://fanyi.youdao.com/openapi?path=data-mode

3、申请微信公众账号：http://mp.weixin.qq.com/

web.py：
4、修改webpy/config.yaml中的appname为你的sae appname，修改index.wsgi中的token为你在微信公众账号设置的token，修改YOUDAO_KEY为你申请的有道翻译key，YOUDAO_KEY_FROM

Django：
4、修django/feng/views.py中的token为你在微信公众账号设置的token，修改YOUDAO_KEY为你申请的有道翻译key，YOUDAO_KEY_FROM

5、在微信公众平台/设置中，设置关键词自动回复，接口配置信息中，url填写：http://yourappname.sinaapp.com/weixin/
，token填写你设置的token

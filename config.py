#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import requests
import configparser

from NexusPHP.utility.function import cookieParse


def generateHeader(url):

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Accept-Language': 'zh-CN',
        'Referer': url
    }
    return header

def generateConfig():
    # 获取cookie , 环境变量取不到就到配置文件取
    try:
        # COOKIE JSON 格式放入 github 仓库 Secrets中
        config_str = os.environ["CONFIG"]
    except:
        # COOKIE DICT 格式在此填写 ，此处会明文暴露 ，不建议在此填写
        config_obj = configparser.RawConfigParser()
        config_obj.read('config.ini')
        config_str = config_obj['NexusPHP']['config']

    configs = eval(config_str)

    for config in configs:
        config['cookie'] = cookieParse(config['cookie'])

        header = generateHeader(config['url'])

        # 设置请求头 、 cookie
        session = requests.session()
        session.headers.update(header)
        session.cookies.update(config['cookie'])

        yield {'url':config['url'],'session':session,'tasks':config['tasks']}


if __name__ == '__main__':

    [ print(config) for config in generateConfig() ]




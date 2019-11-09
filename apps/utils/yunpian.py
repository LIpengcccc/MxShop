# encoding: utf-8
"""
@author:lipeng
@time:2019/10/22  11:35
"""

import requests
import json


class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        #需要传递的参数
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "您的验证码是{code}".format(code=code)
        }

        response = requests.post(self.single_send_url, data=parmas)
        re_dict = json.loads(response.text)
        return re_dict

if __name__ == "__main__":
    #例如：9b11127a9701975c734b8aee81ee3526
    # yun_pian = YunPian("52f5c9723e5cb5eef56d12d8ab8062f4")
    # yun_pian.send_sms("1222", "13554518280")
    pass
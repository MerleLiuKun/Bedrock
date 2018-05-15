# coding=utf-8

"""
    custom user agent.
"""
import logging
from fake_useragent import UserAgent
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from scrapy import log


class RotateUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self, user_agent=''):
        # super(RotateUserAgentMiddleware, self).__init__(user_agent)
        self.user_agent = user_agent

    def process_request(self, request, spider):
        user_agent = UserAgent()
        ua = user_agent.random
        if ua:
            # show current user_agent
            print("********Current UserAgent:%s************".format(ua))
            # 记录
            log.msg('Current UserAgent: ' + ua, level=logging.INFO)
            request.headers.setdefault('User-Agent', ua)
            request.headers.setdefault('Host', 'www.toutiao.com')

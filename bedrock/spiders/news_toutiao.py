# coding=utf-8

"""
    The new's data from toutiao.
    'http://m.toutiao.com/list/?tag=__all__&ac=wap&count=100&format=json_raw&as=A17538D54D106FF&cp=585DF0A65F0F1E1&min_behot_time=0'
"""
import re
import json
from scrapy import Request, Spider
from libs import getASCP
from bedrock.items import NewsItem, CommentItem


class ToutiaoNews(Spider):
    name = "toutiao"
    md = re.compile(r"<.*?>")

    cookies = {
        'tt_webid': '6550245978044745229'
    }

    download_delay = 1

    allowed_domains = ['toutiao.com']
    start_urls = [
        'http://m.toutiao.com/list/?tag=__all__&ac=wap&count=100&format=json_raw&'
        'as=A17538D54D106FF&cp=585DF0A65F0F1E1&min_behot_time=0'
    ]
    url = 'http://m.toutiao.com/list/?tag=__all__&ac=wap&count=50&format=json_raw&' \
          'as={c_as}&cp={c_cp}&min_behot_time=0'

    content_url = 'http://m.toutiao.com{source_url}info/'
    comment_url = 'https://www.toutiao.com/api/comment/list/?group_id={group_id}&item_id={item_id}&offset=0&count=20'

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies=self.cookies)

    def parse(self, response):
        """
        获取到新闻信息列表，从中得到某新闻的具体信息，并
        :param response:
        :return:
        """
        response_data = json.loads(response.body.decode("utf-8"))
        # print(response_data['data'])
        data = response_data["data"]
        c_as, c_cp = getASCP()
        if response_data.get('return_count'):
            for row_data in data:
                source_url = row_data.get('source_url')
                pre_data = {
                    'keywords': row_data.get('keywords', ''),  # 关键词
                    'abstract': row_data['abstract'],  # 摘要
                    'tag_id': row_data['tag_id'],  # 新闻ID
                    'datetime': row_data['datetime'],  # 创建时间
                }
                if source_url:
                    yield Request(
                        url=self.content_url.format(source_url=source_url),
                        callback=self.parse_article,
                        meta=pre_data,
                    )

                item_id = row_data.get('item_id')
                group_id = row_data.get('group_id')
                if all([item_id, group_id]):
                    yield Request(
                        url=self.comment_url.format(group_id=group_id, item_id=item_id),
                        callback=self.parse_comments,
                        meta={'tag_id': row_data['tag_id']}
                    )
            # 刷新列表
            yield Request(
                url=self.url.format(
                    c_as=c_as, c_cp=c_cp
                ),
                callback=self.parse,
            )
        else:
            print("error.")

    def parse_article(self, response):
        pre_data = response.meta
        data = json.loads(response.text.decode('utf-8'))['data']
        item = NewsItem()
        item['news_id'] = pre_data['tag_id']
        item['abstract'] = pre_data['abstract']
        item['keywords'] = pre_data['keywords']
        item['created_at'] = data['publish_time']  # TODO time
        item['source'] = data['source']
        item['comments_count'] = data['comment_count']
        item['content'] = re.sub(self.md, '', data['content'])
        item['title'] = data['title']
        yield item

    @staticmethod
    def parse_comments(response):
        meta = response.meta
        data = json.loads(response.text.decode('utf-8'))['data']
        comments = data['comments']
        for comment in comments:
            item = CommentItem()
            item['comment_id'] = comment['id']
            item['news_id'] = meta['tag_id']
            item['text'] = comment['text']
            item['create_time'] = comment['create_time']
            item['from_user_name'] = comment['user']['name']
            item['from_user_id'] = comment['user']['user_id']
            yield item

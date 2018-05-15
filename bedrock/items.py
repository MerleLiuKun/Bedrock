# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BedrockItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class NewsItem(scrapy.Item):
    news_id = scrapy.Field()
    title = scrapy.Field()
    keywords = scrapy.Field()
    source = scrapy.Field()
    abstract = scrapy.Field()
    content = scrapy.Field()
    created_at = scrapy.Field(serializer=str)
    comments_count = scrapy.Field()


class CommentItem(scrapy.Item):
    comment_id = scrapy.Field()
    news_id = scrapy.Field()
    text = scrapy.Field()
    create_time = scrapy.Field()
    from_user_name = scrapy.Field()
    from_user_id = scrapy.Field()

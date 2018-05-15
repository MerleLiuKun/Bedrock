# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from items import NewsItem, CommentItem
from db_pool import pool


class BedrockPipeline(object):
    collection_name = 'news_items'

    def __init__(self):
        self.pool = None

    def open_spider(self, spider):
        self.pool = pool

    def close_spider(self, spider):
        self.pool.close()

    def process_item(self, item, spider):
        db = self.pool.connection()
        cur = db.cursor()
        if isinstance(item, NewsItem):
            check_sql = 'SELECT id from news_info WHERE news_id={}'.format(item['news_id'])
            news_sql = 'INSERT INTO news_info VALUES(null,%s,%s,%s,%s,%s,%s,%s)'
            try:
                if cur.execute(check_sql):
                    print('Current Item has been saved, id: {n_id}, title: {title}'.format(n_id=item['id'], title=item['title']))
                else:
                    cur.execute(
                        news_sql,
                        (
                            item['news_id'], item['title'], item['source'], item['abstract'],
                            item['content'], item['created_at'], item['comments_count']
                        )
                    )
                    db.commit()
            except Exception as e:
                print(e)
            finally:
                if cur:
                    cur.close()

        if isinstance(item, CommentItem):
            check_sql = 'SELECT id from comments WHERE comment_id={}'.format(item['comment_id'])
            comment_sql = 'INSERT INTO comments VALUES (null,%s,%s,%s,%s,%s,%s)'
            try:
                if not cur.execute(check_sql):
                    cur.execute(
                        comment_sql,
                        (
                            item['comment_id'], item['news_id'], item['text'], item['create_time'],
                            item['from_user_name'], item['from_user_id']
                        )
                    )
                    db.commit()
            except Exception as e:
                print(e)
            finally:
                if cur:
                    cur.close()
        return item

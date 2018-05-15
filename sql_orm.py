# coding=utf-8

""" build models for scrapy. """

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Text, BigInteger

engine = create_engine('mysql+mysqldb://root:123456@127.0.0.1/gp_data_dev', echo=True)

metadata = MetaData()

news = Table(
    'news_info', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('news_id', BigInteger),
    Column('title', String(100)),
    Column('source', String(100)),
    Column('abstract', String(255)),
    Column('content', Text),
    Column('created_at', BigInteger),
    Column('comments_count', Integer)
)

tags = Table(
    'tags', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('tag_name', String(100))
)

news_tag = Table(
    'news_tag', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('news_id', BigInteger),
    Column('tag_id', Integer)
)

images = Table(
    'images', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('image_url', String(255))
)

news_image = Table(
    'news_image', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('image_id', Integer),
    Column('news_id', BigInteger),
)


comments = Table(
    'comments', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('comment_id', BigInteger),
    Column('news_id', BigInteger),
    Column('text', Text),
    Column('create_time', BigInteger),
    Column('from_user_name', String(100)),
    Column('from_user_id', BigInteger)
)

metadata.create_all(engine)

# coding=utf-8

import MySQLdb
from DBUtils.PooledDB import PooledDB

import config


pool = PooledDB(
    MySQLdb,
    maxconnections=10,
    host=config.HOST, user=config.USER, passwd=config.PASSWORD,
    db=config.DB_NAME, charset=config.CHARSET
)


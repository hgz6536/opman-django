# -*- coding=utf-8 -*-
import redis
from django.conf import settings


class APBase(object):
    REDSI_POOL = 10000

    @staticmethod
    def getRedisConnection(db):
        '''根据数据源标识获取Redis连接池'''
        if db == APBase.REDSI_POOL:
            args = settings.REDSI_KWARGS_LPUSH
            if settings.REDSI_LPUSH_POOL == None:
                settings.REDSI_LPUSH_POOL = redis.ConnectionPool(host=args.get('host'), port=args.get('port'),db=args.get('db'))
            pools = settings.REDSI_LPUSH_POOL
        connection = redis.Redis(connection_pool=pools)
        return connection


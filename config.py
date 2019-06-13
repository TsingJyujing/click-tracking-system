import os

import pymongo

# 日志数据中冗余链接信息和KV数据
DATA_REDUNDANCY = True

QUEUE_MAX_SIZE = 10000
QUEUE_WRITING_LIMIT = 200
QUEUE_WAITING_TIME = 0.2

if not os.path.exists("token.txt"):
    with open("token.txt", "w") as fp:
        fp.write("")


def get_token() -> set:
    with open("token.txt", "r") as fp:
        return {line.strip("\n") for line in fp.readlines()}


def get_mongo_connection():
    """
    Get main connection for query url info
    :return:
    """
    return pymongo.MongoClient(maxPoolSize=1000)


def get_kvs(connection: pymongo.MongoClient):
    """
    Key-value system url query collection
    :param connection:
    :return:
    """
    return connection.get_database("cts").get_collection("surls")


def get_logging_collection():
    """
    The special place for the logging
    :return:
    """
    return pymongo.MongoClient().get_database('cts').get_collection('logging')

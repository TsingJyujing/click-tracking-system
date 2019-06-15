import os

import pymongo

# Redundancy the user meta data and link in the visit logs
DATA_REDUNDANCY = True

# Queue configuration

# Max size of the queue, if data in queue over this size, the visit will block
QUEUE_MAX_SIZE = 10000

# One of the condition be triggered the queue will cleaned
# The log count limit to write
QUEUE_WRITING_LIMIT = 200
# The check interval to write
QUEUE_WAITING_TIME = 0.2


def token_valid(token: str) -> bool:
    """
    Get the token, you may also read from database like MongoDB if token is too much
    :return:
    """
    with open("token.txt", "r") as fp:
        return token in {line.strip("\n") for line in fp.readlines()}


def get_mongo_connection():
    """
    Get main connection for query url info
    :return:
    """
    # todo if your db have authorize or other settings
    # todo please attach your code here
    return pymongo.MongoClient(host="127.0.0.1", port=27017, maxPoolSize=1000)


def get_kvs(connection: pymongo.MongoClient):
    """
    Key-value system url query collection
    :param connection:
    :return:
    """
    return connection.get_database("cts").get_collection("surls")


def get_logging_connection():
    """
    Get main connection for logging
    :return:
    """
    # todo if your db have authorize or other settings
    # todo please attach your code here
    return pymongo.MongoClient(host="127.0.0.1", port=27017, maxPoolSize=1000)


def get_logging_collection(connection: pymongo.MongoClient):
    """
    The special place for the logging
    :return:
    """
    return connection.get_database('cts').get_collection('logging')


def __init__():
    """
    Initial code for using collections
    :return:
    """

    print("Initializing the config")

    # If the path not exist, write the default token file
    if not os.path.exists("token.txt"):
        with open("token.txt", "w") as fp:
            fp.write("")

    # Ensure index
    with get_mongo_connection() as conn:
        kvc = get_kvs(conn)
        kvc.create_index([("url", pymongo.HASHED)])

    with get_logging_connection() as conn:
        lc = get_logging_collection(conn)
        lc.create_index([("visit_time", pymongo.ASCENDING)])
        lc.create_index([("ip", pymongo.HASHED)])
        lc.create_index([("url_id", pymongo.ASCENDING)])
        lc.create_index([("url", pymongo.HASHED)])

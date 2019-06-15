#!/usr/bin/python3

import os


def mount_data_config():
    """
    Mount all the data (database file) and config file
    :return:
    """
    # fixme Walk dir and mount everything
    os.symlink("/data/db.sqlite3", "/app/db.sqlite3")
    os.symlink("/data/token.txt", "/app/token.txt")
    os.symlink("/data/config.py", "/app/config.py")

# todo Functions: start server, migrate and set superuser passwd
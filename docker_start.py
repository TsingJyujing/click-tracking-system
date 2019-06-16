#!/usr/bin/python3

import os
import argparse


def parameter_parse():
    argparse.ArgumentParser()


def mount_data_config(src: str, target: str):
    """
    Mount all the data (database file) and config file
    :return:
    """
    for root, dirs, files in os.walk(src, topdown=False):
        print("Mounting files from {} to {}...".format(src, target))
        for file in files:
            target_file = os.path.join(target, file)
            if os.path.exists(target_file):
                os.remove(target_file)
                print("{} already in target, removed.".format(target_file))
            print("Mount file: {} -> {}".format(os.path.join(src, file), target_file))
            os.symlink(os.path.join(src, file), target_file)

# todo Functions: start server, migrate and set superuser passwd

# -*- coding: utf-8 -*-
"""
"""
import argparse
import os
import sys
import tempfile
import pathlib

from bpdb import set_trace

class Hoge(object):

    def __init__(self):
        self.tempdir = tempfile.TemporaryDirectory()

    def test(self):
        with open(str(self.tempdir.name + '/test.txt'), 'w') as f:
            f.write('jfkwjalk')

    def check(self):
        print(self.tempdir.name)

    def __del__(self):
        self.tempdir.cleanup()



if __name__ == '__main__':
    hoge = Hoge()
    hoge.test()
    hoge.check()

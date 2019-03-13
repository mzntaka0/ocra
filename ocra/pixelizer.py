# -*- coding: utf-8 -*-
"""
"""
import argparse
import os
import sys
import tempfile

from PIL import Image


class Pixelizer(object):

    def __init__(self):
        self.tempdir = tempfile.TemporaryDirectory()

    def __call__(self, texts_in_page, image_Path):
        image = Image.open(str(image_Path))

    def __del__(self):
        self.tempdir.cleanup()

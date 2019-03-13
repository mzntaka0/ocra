# -*- coding: utf-8 -*-
"""
"""
import argparse
import os
import sys


class TextAnnotationsParser(object):

    def __init__(self, textAnnotations):
        self.textAnnotations = textAnnotations

    def __getitem__(self, idx):
        coords = None
        text = None
        return coords, text

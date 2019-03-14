# -*- coding: utf-8 -*-
"""
"""
import enum


class WordOrient(enum.Enum):
    """
    Corresponding the index of a rectangle's top-left.
    """
    UP = 0
    RIGHT = 3
    DOWN = 2
    LEFT = 1

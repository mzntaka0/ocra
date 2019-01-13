# -*- coding: utf-8 -*-
"""
"""
import os
import sys


from ocra.typedocs import basedoc


class Pdf(basedoc.Basedoc):
    """

    Args:
    """

    def __init__(self, document_Path):
        self._doc_path = document_Path

    def read_lines(self, document_Path):
        pass

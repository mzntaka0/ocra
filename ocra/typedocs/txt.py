# -*- coding: utf-8 -*-
"""
"""
from pathlib import Path

from ocra.typedocs import basedoc


class Txt(basedoc.Basedoc):
    """

    Args:
    """

    def __init__(self, document_Path):
        self._doc_path = self._validate_Path(document_Path)

    def read_lines(self):
        with open(str(self._doc_path), 'r') as f:
            docs = f.read().split('\n')
            docs.remove('')
        return docs

    def _validate_Path(self, path):
        return Path(path)

# -*- coding: utf-8 -*-
"""
"""
import os
import sys
from pathlib import Path


from ocra.exceptions import ExtensionNotAvailableError

class DocAcceptor(object):
    """

    Args:
    """
    available_ext = [
            'pdf',
            'txt'
            ]


    def __init__(self):
        pass

    @classmethod
    def extract_document(cls, document_path):
        document_Path = self.wrap_to_pathlib(document_path)
        self.isFileExists(document_Path)
        ext = self.validate_ext(self.get_ext(document_Path))
        return getattr('ocra.typedocs', ext.capitalize())(document_Path)

    def validate_ext(self, ext):
        if ext not in self.available_ext:
            raise ExtensionNotAvailableError(
                    'This extension {} is not available. Select from {}'.format(self.available_ext)
                    )
        else:
            return ext

    @staticmethod
    def wrap_to_pathlib(document_path):
        return Path(document_path)

    @staticmethod
    def get_ext(document_Path):
        return document_Path.suffix.replace('.', '')

    @staticmethod
    def isFileExists(document_Path):
        if not document_Path.exists():
            raise FileNotFoundError()


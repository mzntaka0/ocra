# -*- coding: utf-8 -*-
"""
"""
import os
import sys
from pathlib import Path


from ocra.exceptions import ExtensionNotAvailableError
import ocra

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
        document_Path = cls.wrap_to_pathlib(document_path)
        cls.isFileExists(document_Path)
        ext = cls.validate_ext(cls.get_ext(document_Path))
        return getattr(ocra.typedocs, ext.capitalize())(document_Path).read_lines()

    @classmethod
    def validate_ext(cls, ext):
        if ext not in cls.available_ext:
            raise ExtensionNotAvailableError(
                    'This extension {} is not available. Select from {}'.format(cls.available_ext)
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

if __name__ == '__main__':
    acceptor = DocAcceptor.extract_document('/home/mzntaka0/Dropbox/work/oss/ocra/tests/data/mock.txt')
    print(acceptor)

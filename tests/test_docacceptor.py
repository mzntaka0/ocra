# -*- coding: utf-8 -*-
"""
"""
from pathlib import Path

from ocra import DocAcceptor


class TestDocAcceptor:
    def test_instance():
        doc_acceptor = DocAcceptor()

    def test_extract_document():
        doc_path = 'hoge.txt'
        doc_Path = Path('hoge.pdf')
        txt = DocAcceptor.extract_document(doc_path)
        txT = DocAcceptor.extract_document(doc_Path)
        assert txt == ''

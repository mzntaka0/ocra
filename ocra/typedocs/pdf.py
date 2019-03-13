# -*- coding: utf-8 -*-
"""
"""
from pathlib import Path
import glob
import os
import subprocess
import tempfile

import xmltodict

from ocra.typedocs import basedoc
from ocra.exceptions import PageNotFoundError


class Pdf(basedoc.Basedoc):
    """
    PDF object to do text extraction.
    This class is dependent on XMLPDF class.

    Args:
        - document_Path(pathlib.Path): Path of pdf.
    """

    def __init__(self, document_Path):
        self.tempdir = tempfile.TemporaryDirectory()
        self.document_Path = self._validate_Path(document_Path)
        self.xmlpdf = self.init()
        self._counter = 0

    def read_lines(self, raw=False):
        if raw:
            return self.xmlpdf.raw_texts
        return self.xmlpdf.texts

    def init(self):
        xml_Path = self.pdf2xml()
        self.pdf2img()
        xmlpdf = XMLPDF(xml_Path)
        return xmlpdf

    def __del__(self):
        self.tempdir.cleanup()

    def __repr__(self):
        return '[<PDF file> Pages: {}]'.format(len(self.xmlpdf))

    def __getitem__(self, page_num):
        """
        return image_path and text data of each page

        input:
            - page_num(int): index of page

        return:
            - text_in_page(dict): Texts information in the specified page.
            - image_Path(pathlib.Path): Path for image of specified page.
        """
        if not 1 <= page_num <= len(self.xmlpdf):
            raise PageNotFoundError('This page number [{}] is out of range. Select from 1 <= page < {} for this document.'.format(page_num, len(self.xmlpdf)))
        page_num -= 1
        page = self.xmlpdf.pages[page_num]
        texts_in_page = self.xmlpdf._extract_text(page)
        images = self._get_images()
        image_Path = Path(images[page_num])
        return texts_in_page, image_Path

    def __iter__(self):
        return self

    def __next__(self):
        if self._counter >= len(self.xmlpdf):
            self._counter = 0
            raise StopIteration()
        page = self.xmlpdf.pages[self._counter]
        texts_in_page = self.xmlpdf._extract_text(page)
        images = self._get_images()
        image_Path = Path(images[self._counter])
        self._counter += 1
        return texts_in_page, image_Path

    def pdf2xml(self):
        output_path = os.path.join(self.tempdir.name, self.document_Path.stem + '.xml')
        cmd = 'pdftohtml -c -hidden -nodrm -xml {} {}'.format(str(self.document_Path), output_path)
        subprocess.call(cmd, shell=True)
        return Path(output_path)

    def pdf2img(self):
        output_path = os.path.join(self.tempdir.name, self.document_Path.stem)
        cmd = 'pdftocairo -png {} {}'.format(str(self.document_Path), output_path)
        subprocess.call(cmd, shell=True)

    def _validate_Path(self, path):
        return Path(path)

    def _get_images(self):
        images = sorted(glob.glob(os.path.join(self.tempdir.name, '*.png')))
        return images


class XMLPDF(object):
    """
    Help to parse xml which is generated from pdftohtml.

    Args:
        - xml_Path(pathlib.Path): Path of xml which is generated from pdftohtml.
    """

    def __init__(self, xml_Path):
        self.xml_Path = xml_Path
        self.dictpdf = xmltodict.parse(self._load_xml(xml_Path))
        self._extract_pages()
        self._extract_texts()

    # TODO: parse to dict
    @property
    def pages(self):
        return self._pages

    @property
    def texts(self):
        return self._texts

    @property
    def raw_texts(self):
        return self._raw_texts

    def _load_xml(self, xml_Path):
        with open(str(xml_Path), 'r') as f:
            xml = f.read()
        return xml

    def __len__(self):
        return len(self.pages)

    def __repr__(self):
        return str(self.dictpdf)

    def _extract_pages(self):
        self._pages = self.dictpdf['pdf2xml']['page']

    def _extract_texts(self):
        _texts = list()
        _raw_texts = list()
        for page in self.pages:
            _texts.extend(self._extract_text(page))
            _raw_texts.extend(self._extract_raw_text(page))
        self._texts = _texts
        self._raw_texts = _raw_texts

    def _extract_text(self, page):
        if 'text' not in page.keys():
            return None
        texts_in_page = [{
            'boundingPoly': self._get_poly(t),
            'description': t['#text']
        } for t in page['text'] if '#text' in t.keys()]
        return texts_in_page

    def _extract_raw_text(self, page):
        if 'text' not in page.keys():
            return None
        raw_texts_in_page = [t['#text'] for t in page['text'] if '#text' in t.keys()]
        return raw_texts_in_page

    def _get_poly(self, t):
        left = int(t['@left'])
        top = int(t['@top'])
        right = left + int(t['@width'])
        bottom = top + int(t['@height'])
        return {
                    'vertices': [
                        {
                            'x': left,
                            'y': top
                        },
                        {
                            'x': right,
                            'y': top
                        },
                        {
                            'x': right,
                            'y': bottom
                        },
                        {
                            'x': left,
                            'y': bottom
                        }
                    ]}


if __name__ == '__main__':
    document_Path = Path('../../../../git/pdf2xml-viewer/00.pdf')
    pdf = Pdf(document_Path)
    texts = pdf.read_lines()
    print(texts)

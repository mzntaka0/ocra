# -*- coding: utf-8 -*-
"""
"""
import os
import subprocess
import tempfile
from pathlib import Path
from bpdb import set_trace

from ocra.typedocs import basedoc
import xmltodict


class Pdf(basedoc.Basedoc):
    """
    PDF object to do text extraction.

    Args:
        - document_Path(pathlib.Path): Path of pdf.
    """

    def __init__(self, document_Path):
        self.tempdir = tempfile.TemporaryDirectory()
        self.document_Path = self._validate_Path(document_Path)

    def read_lines(self, raw=False):
        xml_Path = self.pdf2xml()
        self.pdf2img()
        xmlpdf = XMLPDF(xml_Path)
        if raw:
            return xmlpdf.raw_texts
        return xmlpdf.texts

    def __del__(self):
        self.tempdir.cleanup()

    def pixelize(self):
        pass

    def pdf2xml(self):
        output_path = os.path.join(self.tempdir.name, self.document_Path.stem + '.xml')
        cmd = 'pdftohtml -c -hidden -nodrm -xml {} {}'.format(str(self.document_Path), output_path)
        subprocess.call(cmd, shell=True)
        return Path(output_path)

    def pdf2img(self):
        output_path = os.path.join(self.tempdir.name, self.document_Path.stem)
        cmd = 'pdftocairo -png {} {}'.format(str(self.document_Path), output_path)
        subprocess.call(cmd, shell=True)
        set_trace()

    def _validate_Path(self, path):
        return Path(path)


class XMLPDF(object):
    """
    Help to parse xml which is generated from pdftohtml.

    Args:
        - xml_Path(pathlib.Path): Path of xml which is generated from pdftohtml.
    """

    def __init__(self, xml_Path):
        self.xml_Path = xml_Path
        self.dictpdf = xmltodict.parse(self._load_xml(xml_Path))
        self._extract_page()
        self._extract_text()

    def _load_xml(self, xml_Path):
        with open(str(xml_Path), 'r') as f:
            xml = f.read()
        return xml

    def __getitem__(self, idx):
        pass

    def __len__(self):
        pass

    def __repr__(self):
        return str(self.dictpdf)

    def _extract_page(self):
        self._pages = self.dictpdf['pdf2xml']['page']

    def _extract_text(self):
        p_texts = [x['text'] for x in self.pages if 'text' in x.keys()]
        _texts = list()
        _raw_texts = list()
        for pt in p_texts:
            _texts.extend([{
                'boundingPoly': self._get_poly(t),
                'description': t['#text']
            } for t in pt if '#text' in t.keys()])
            _raw_texts.extend([t['#text'] for t in pt if '#text' in t.keys()])
        self._texts = _texts
        self._raw_texts = _raw_texts

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


if __name__ == '__main__':
    document_Path = Path('../../../../git/pdf2xml-viewer/00.pdf')
    pdf = Pdf(document_Path)
    texts = pdf.read_lines()
    print(texts)

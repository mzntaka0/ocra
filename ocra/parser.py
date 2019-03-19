# -*- coding: utf-8 -*-
"""
"""
import numpy as np

from ocra.enums import WordOrient


# TODO: should create interface class. Otherwise the definitive image-text data class can be created.
class TextAnnotationsParser(object):

    def __init__(self, textAnnotations, isRelative=True):
        self.textAnnotations = textAnnotations
        self.isRelative = isRelative
        self._counter = 0

    def __getitem__(self, idx):
        annotxt = AnnotatedText(self.textAnnotations[idx])
        coords = annotxt.relative if self.isRelative else annotxt.absolute
        description = annotxt.description
        return coords, description

    def __len__(self):
        return len(self.textAnnotations)

    def __iter__(self):
        return self

    def __next__(self):
        if self._counter >= len(self):
            self._counter = 0
            raise StopIteration()
        annotxt = AnnotatedText(self.textAnnotations[self._counter])
        coords = annotxt.relative if self.isRelative else annotxt.absolute
        description = annotxt.description

        self._counter += 1
        return coords, description


class TextAnnotationDeparser(object):

    def __init__(self, isRelative=True):
        self.isRelative = isRelative

        # TODO: Needs an implementation.
    def __call__(self, coords, description):
        pass


# TODO: Consider about the name of this class to make it more comfortable.
class AnnotatedText(object):

    def __init__(self, textAnnotation):
        self.textAnnotation = textAnnotation
        self._abs_coords = self._extract_coords()
        self.orient = self._recognize_orientation(self._abs_coords)

    @property
    def description(self):
        """
        Return description.
        """
        return self.textAnnotation.get('description', None)

    @property
    def absolute(self):
        """
        Return absolute coords. shape: [[x_min, y_min], [x_max, y_max]]
        """
        return self._absolute(self._abs_coords)

    @property
    def relative(self):
        """
        Return relative coords. shape: [[x_min, y_min], [w, h]]
        """
        return self._relative(self._abs_coords)

    # TODO: This method has yielded a state. Gatta make it be stateless.
    def _extract_coords(self):
        coords = self.textAnnotation['boundingPoly']['vertices']
        coords = [[p['x'], p['y']] for p in coords]
        return coords

    # TODO: For now this is dependent on gocr's response. Check whether it is general or not.(gocr defines coords[0] as the top-left of words.)
    def _recognize_orientation(self, coords):
        np_coords = np.array(coords)
        topleft = np_coords.sum(axis=1).argmin()
        return WordOrient(topleft)

    def _absolute(self, coords):
        np_coords = np.array(coords)
        coords_max = np_coords.max(axis=0)
        coords_min = np_coords.min(axis=0)
        return [coords_min.tolist(), coords_max.tolist()]

    def _relative(self, coords):
        np_coords = np.array(coords)
        coords_max = np_coords.max(axis=0)
        coords_min = np_coords.min(axis=0)
        _wh = coords_max - coords_min
        relative = [coords_min.tolist(), _wh.tolist()]
        return relative


if __name__ == '__main__':
    import ocra
    from PIL import Image
    import cv2

    document = ocra.Document.load('/home/mzntaka0/Dropbox/work/oss/ocra/tests/data/mock.pdf')
    texts, image = document[1]
    image = Image.open(image).convert('L')
    image = np.asarray(image).astype(np.uint8)
    text = AnnotatedText(texts[0])
    parser = TextAnnotationsParser(texts, isRelative=False)
    for coords, description in parser:
        x_min, y_min = coords[0]
        x_max, y_max = coords[1]
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color=(0, 0, 255))
        print(coords, description)
    cv2.imwrite('rect.png', image)

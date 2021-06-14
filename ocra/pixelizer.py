# -*- coding: utf-8 -*-
"""
"""
import multiprocessing
import os
import subprocess
import tempfile

from PIL import Image
import numpy as np

import ocra


# TODO: make this class be more beautiful
class DescriptionsCrop(object):

    def __init__(self, parser=ocra.TextAnnotationsParser, isMultiprocessing=True):
        self.tempdir = tempfile.TemporaryDirectory()
        self.isMultiprocessing = isMultiprocessing
        if self.isMultiprocessing:
            self.num_cpus = multiprocessing.cpu_count()
        self.parser = parser  # must be iterator class object which returns instance.coords, instance.description

    # TODO: This method is dependent on the output of Pdf object. Let this class be independent.
    def __call__(self, descriptions, image_Path):
        image = {'object': Image.open(str(image_Path)).convert('L'), 'name': image_Path.stem}
        self.image = np.asarray(image['object']).astype(np.uint8)
        descriptions = self.parser(descriptions, isRelative=False)
        materials = self._materials(image, descriptions)
        with multiprocessing.Pool(processes=self._worker()) as pool:
            pool.map(self.wrapper, materials)

    def __del__(self):
        try:
            self.tempdir.cleanup()
        except FileNotFoundError:
            pass

    def wrapper(self, args):
        return self._make_train_data(*args)

    def _worker(self):
        return max(int(self.num_cpus / 2.0), 2) if self.isMultiprocessing else 1

    # TODO: Descend the number of output
    def _materials(self, image, descriptions):
        return [(i, image, coords, description) for i, (coords, description) in enumerate(descriptions, 1)]

    def _make_train_data(self, save_id, image, coords, description):
        cropped_img = self.crop(image['object'], *coords[0], *coords[1])
        self._tmp_save(save_id, image['name'], cropped_img, description)

    def _tmp_save(self, save_id, image_name, cropped_img, description):
        save_stem_path = os.path.join(self.tempdir.name, image_name + '_{}'.format(save_id))
        self._save_img(save_stem_path, cropped_img)
        self._save_description(save_stem_path, description)

    def _save_img(self, save_stem_path, cropped_img):
        image_path = save_stem_path + '.png'
        cropped_img.save(image_path)

    def _save_description(self, save_stem_path, description):
        description_path = save_stem_path + '.txt'
        with open(description_path, 'w') as f:
            f.write(description)

    def crop(self, img, x_min, y_min, x_max, y_max):
        if not isinstance(img, Image.Image):
            raise TypeError('input img object must be PIL.Image. Got {}'.format(type(img)))
        return img.crop((x_min, y_min, x_max, y_max))

    def save(self, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        cmd = 'mv {}/* {}'.format(self.tempdir.name, output_dir)
        subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    import ocra
    pdf_path = '../tests/data/mock.pdf'
    pdf = ocra.Document.load(pdf_path)
    for descriptions, image_Path in pdf:
        cropper = DescriptionsCrop()
        cropper(descriptions, image_Path)
        cropper.save('/tmp/test/')

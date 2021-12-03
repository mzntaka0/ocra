# -*- coding: utf-8 -*-
"""
"""
import argparse
import os
import sys
import glob

try:
    from bpdb import set_trace
except ImportError:
    from pdb import set_trace

import cv2 as cv
import numpy as np
from PIL import ImageFont, ImageDraw, Image, ImageOps
from tqdm import tqdm
import torchvision


class Text2Image:
    """
    This class achieve to make image from text object with any ttf.

    Args:
        font[str]: ttf(or woff) file path which you wanna asign. Default: None

    Usage:
    >>> text2image = Text2Image()
    >>> text2image.set_font('font/TanukiMagic.ttf')
    >>> text2image.convert('狸だよ', output_dir='hogehoge')
    """

    def __init__(self, font=None):
        self.font = font  # Ex: 'TanukiMagic.ttf'
        self.resizer = randomResize()
        self.rotator = torchvision.transforms.RandomAffine(degrees=5, fillcolor=255)

    def set_font(self, font):
        """
        set font file

        input:
            - font[str]: font file path  e.g.) fonts/tegaki.ttf

        output:
            None
        """
        self.font = font

    def convert(self, text, output_dir="dataset", fill=(0, 0, 0)):
        """
        convert text to image

        input:
            - text[str]: text object you want convert to image
            - output_dir[str]: output path of images and texts
            - fill[tuple]: background color (r, g, b) each 0-255

        output:
            None
        """
        if not self.font:
            print("Please set ttf with set_font method. Try again.")
            sys.exit(0)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        text_length = len(text)
        size = (50, int(390 * (text_length / 15)), 3)  # decided experimentally
        img = np.zeros(size, dtype=np.uint8)
        if os.path.splitext(self.font)[1].replace(".", "") in ["ttf", "woff"]:
            font = ImageFont.truetype(self.font, 32)
        else:
            font = ImageFont.FreeTypeFont(self.font, 32)
        img_pil = Image.fromarray(img)
        img_pil = ImageOps.invert(img_pil)
        draw = ImageDraw.Draw(img_pil)
        draw.text((20, 10), text, font=font, fill=fill)
        img_pil = self.resizer(img_pil)
        img_pil = self.rotator(img_pil)
        img = np.array(img_pil)
        img_num = len(glob.glob(os.path.join(output_dir, "*.png")))
        font_name = os.path.basename(self.font).split(".")[0]
        output_name = "{}_{}".format(font_name, img_num)
        cv.imwrite(os.path.join(output_dir, output_name + ".png"), img)
        with open(os.path.join(output_dir, output_name + ".txt"), "w") as f:
            f.write(text)

    @staticmethod
    def get_args():
        """
        For batch processing
        Usage:
        $ python text2image.py --fonts fonts --text_file text/tsucho.txt --output dataset
        """
        parser = argparse.ArgumentParser(
            description="Making Image from font with TrueTypeFonts(ttf)"
        )
        parser.add_argument(
            "--fonts",
            type=str,
            required=True,
            help="directory path including font files.",
        )

        parser.add_argument(
            "--text_file", type=str, required=True, help="text file path listing texts"
        )
        parser.add_argument(
            "--output", type=str, required=True, help="output directory path"
        )
        args = parser.parse_args()
        return args


class randomResize(object):
    def __init__(self, interpolation=Image.LANCZOS):
        self.interpolation = interpolation

    def __call__(self, img):
        if isinstance(img, np.ndarray):
            shape = img.shape
        else:
            shape = img.size
        img = self.random_expand(img, shape)
        self.random_scaling(img, shape)
        return img

    def _ratio(self):
        return np.random.rand() - 0.5  # {x∈R|x∈[-0.5, 0.5]}

    def random_expand(self, img, shape):
        img = img.resize(
            (int(shape[0] * (1 + self._ratio())), shape[1]), self.interpolation
        )
        return img

    def random_scaling(self, img, shape):
        ratio = self._ratio()
        img.thumbnail((shape[0] * (1 + ratio), shape[1] * (1 + ratio)), Image.LANCZOS)


if __name__ == "__main__":
    # example of batch processing
    args = Text2Image.get_args()
    with open(args.text_file, "r") as f:
        text = f.readlines()
    font_list = os.listdir(args.fonts)
    text2image = Text2Image()
    for t in tqdm(text):
        for f in font_list:
            text2image.set_font(os.path.join(args.fonts, f))
            text2image.convert(t, output_dir=args.output)

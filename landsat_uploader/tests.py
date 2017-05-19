from django.test import TestCase
from django.conf import settings

from .list_files import * # ListLandsatImages
from .uploader import * # LandsatUploader

class LandsatImagesTest(TestCase):
    """docstring for LandsatImagesTest"""
    def setUp(self):
        self.images = ["LC08_L1TP_231064_20170511_20170511_01_RT.tar.gz"]
        self.list = ListLandsatImages.get_files()

    def test_list_images(self):
        self.assertEqual(self.list, self.images)


class LandsatUploaderTest(TestCase):
    """docstring for LandsatUploaderTest"""
    def setUp(self):
        self.arg = arg
        

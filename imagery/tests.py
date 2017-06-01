import os
import shutil

from osgeo import gdal
from datetime import datetime
from django.conf import settings
from django.test import TestCase
from landsat_uploader.uploader import LandsatUploader
from landsat_uploader.utils import get_data_image_name

from .models import Scene, Image, LandsatGrade


class TestCreateRgb(TestCase):
    """ TestCreateRgb TestCase class """

    def setUp(self):
        polygon = "POLYGON \
            (\
                (\
                -60.5143287889999 -6.59136581799993, \
                -60.5275415539999 -6.65361430499993, \
                -60.5303 -6.66661, \
                -60.5303060099999 -6.66660912699993, \
                -62.1856759309999 -6.42615349599993, \
                -62.1857 -6.42615, \
                -61.8745855689999 -4.98025209599993, \
                -61.8584 -4.90503, \
                -60.2073467339999 -5.14487321099993, \
                -60.2073 -5.14488, \
                -60.5143287889999 -6.59136581799993)\
            )"  
        LandsatGrade.objects.create(
            path=231, 
            row=64,
            geom=polygon)

        self.uploader = LandsatUploader() # LandsatUploader initialize
        self.scene_name = "LC08_L1TP_231064_20170511_20170511_01_RT"

    def test_scene_image_creation_composition(self):
        scenes = self.uploader.extract_and_populate_data()
        self.scene = scenes[self.scene_name]["scene"]
        
        self.assertEqual(Scene.objects.count(), 1)
        self.assertEqual(Image.objects.filter(type__in=["B6", "B5", "B4"]).count(), 3)

        ## Testing image exists ##
        for img in Image.objects.all():
            self.assertTrue(os.path.isfile(img.path))

        ## Test image composition creation ##
        imgs = Image.objects.filter(scene=self.scene, type__in=["B6", "B5", "B4"])
        plist = [img.path for img in imgs]
        path = os.path.join(settings.MEDIA_ROOT, "L8", self.scene_name)

        ## Test Image.Model creation ##
        img = self.scene.create_rgb(path, self.scene_name, plist)
        self.assertEqual(img.type, "RGB")

        ## Test image composition creation ##
        datafile = gdal.Open(img.path)
        self.assertEqual(datafile.RasterCount, 3)

    def tearDown(self):
        for scene in Scene.objects.all(): # Delete scenes created after each test 
            scene.delete()
        for image in Image.objects.all(): # Delete image created after each test
            image.delete()

        rm_path = os.path.join( settings.MEDIA_ROOT, "L8", self.scene_name ) 
        if os.path.exists( rm_path ): # Delete created files in tests in MEDIA_ROOT
            shutil.rmtree( rm_path )

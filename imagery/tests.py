from django.test import TestCase
from datetime import datetime
import os
from django.conf import settings

from .models import Scene, Image
from osgeo import gdal
from landsat_uploader.uploader import LandsatUploader

class TestCreateRgb(TestCase):
    def setUp(self):

        polygon = 'POLYGON\
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
                    )'

        self.scene_name = "LC08_L1TP_231064_20170511_20170511_01_RT"
        self.scene = Scene.objects.get_or_create(
            path = "231",
            row = "064",
            sat = "L8",
            date = datetime.now(),
            name = self.scene_name,
            cloud_rate = 0,
            geom = polygon,
            status = "extracted",
        )
        path = os.path.join(settings.MEDIA_ROOT, "L8", self.scene[0].name)

        self.rgb_file_path = os.path.join(path, self.scene_name + "_RGB.TIF")

        for i in range(4,7):
            img = "{}_B{}.TIF".format(self.scene_name, i)
            Image.objects.create(
                name = img,
                type = "B{}".format(i),
                scene = self.scene[0],
                path = os.path.join(path, img)
            )

    def test_scene_image_creation(self):
        self.assertEqual(Scene.objects.count(), 1)
        self.assertEqual(Image.objects.count(), 3)

    def test_if_file_exists(self):
        for img in Image.objects.all():
            self.assertTrue(os.path.isfile(img.path))

    def test_create_rgb(self):
        scene = self.scene[0]

        imgs = Image.objects.filter(scene = scene, type__in=["B6", "B5", "B4"])
        self.assertEqual(imgs.count(), 3)

        plist = [imgs.path for imgs in imgs]
        path = os.path.join(settings.MEDIA_ROOT, "L8", self.scene_name)

        rgb = scene.create_rgb(path, self.scene_name, plist)
        self.assertEqual(rgb['type'], "RGB")
        self.rgb_file_path = rgb

    def test_rgb_composition(self):
        datafile = gdal.Open(self.rgb_file_path)
        self.assertEqual(datafile.RasterCount, 3)



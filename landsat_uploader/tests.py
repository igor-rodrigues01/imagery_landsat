import os
import shutil

from datetime import datetime
from django.test import TestCase
from django.conf import settings

from .models import Scene, Image
from .list_files import * # ListLandsatImages
from .uploader import * # LandsatUploader
from .utils import get_data_from_landsat_image_name


class LandsatImageDataExtractionTest(TestCase):
    """docstring for LandsatImageDataExtractionTest"""
    def setUp(self):
        self.name = "LC08_L1TP_231064_20170511_20170511_01_RT"

    def test_extraction_data_from_image_name(self):
        data = get_data_from_landsat_image_name(self.name)
        self.assertEqual(data["path"], "231")
        self.assertEqual(data["row"], "064")
        self.assertEqual(data["date"], datetime.strptime( "20170511", "%Y%m%d" ))
        self.assertEqual(data["name"], "LC08_L1TP_231064_20170511_20170511_01_RT")

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
        self.uploader = LandsatUploader()
        self.scene_name = "LC08_L1TP_231064_20170511_20170511_01_RT"

    def test_get_scene_name_path(self):
        self.assertEqual(
            self.uploader._get_scene_name_path()[0]["name"],
            self.scene_name
        )
        
        self.assertEqual(
            self.uploader._get_scene_name_path()[0]["path"],
            os.path.join(
                settings.LANDSAT_IMAGES_PATH, "L8",
                self.scene_name + ".tar.gz"
            )
        )

    def test_uploader_scene_creation(self):
        scene = self.uploader._create_scene(self.scene_name)
        self.assertEqual(Scene.objects.count(), 1)

        created_scene = Scene.objects.get(name=self.scene_name)
        self.assertEqual(created_scene.path, "231")
        self.assertEqual(created_scene.row, "064")

    def test_uploader_image_creation(self):
        for file in self.uploader._get_scene_name_path():
            scene = self.uploader._create_scene(file["name"])
            files = self.uploader._extract_file(name=file["name"], path=file["path"])

            self.uploader._upload_files(files, scene[0])

        self.assertEqual(Image.objects.count(), 4)



    def tearDown(self):
        for scene in Scene.objects.all():
            scene.delete()
        for image in Image.objects.all():
            image.delete()

        rm_path = os.path.join( settings.MEDIA_ROOT, "L8", self.scene_name )
        if os.path.exists( rm_path ):
            shutil.rmtree( rm_path )

import os
import shutil
import tarfile

from datetime import datetime
from django.test import TestCase
from django.conf import settings
from imagery.models import Scene, Image, LandsatGrade

 
from .models import Scene, Image, LandsatGrade
from .list_files import ListLandsatImages
from .uploader import LandsatUploader # LandsatUploader
from .utils import get_data_image_name_

from .list_files import * # ListLandsatImages
from .uploader import * # LandsatUploader
from .utils import get_data_image_name

class LandsatImageDataExtractionTest(TestCase):
    """ Tests scene data from scene image name """

    def setUp(self):
        self.name = "LC08_L1TP_231064_20170511_20170511_01_RT"

    def test_extraction_data_from_image_name(self):
        data = get_data_image_name_(self.name)
        self.assertEqual(data["path"], "231")
        self.assertEqual(data["row"], "064")
        self.assertEqual(data["date"], datetime.strptime( "20170511", "%Y%m%d" ))
        self.assertEqual(data["name"], "LC08_L1TP_231064_20170511_20170511_01_RT")


class LandsatImagesTest(TestCase):
    """ Tests tar.gz list files from defined path """
    def setUp(self):
        self.images = ["corrupt.tar.gz","LC08_L1TP_231064_20170511_20170511_01_RT.tar.gz"]
        self.list = ListLandsatImages.get_files()
        self.image_name = "LC08_L1TP_231064_20170511_20170511_01_RT"
   
    def test_list_images(self):
        self.assertEqual(self.list[0], self.images[1])

class LandsatUploaderTest(TestCase):
    """ Tests Upload data after extraction """
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

        self.uploader = LandsatUploader() # LandsatUploader initialize
        self.scene_name = "LC08_L1TP_231064_20170511_20170511_01_RT"
        self.data = get_data_image_name_(self.scene_name)
        self.landsatGrade = LandsatGrade.objects.create(
            path=231, 
            row=64,
            geom=polygon)

        self.l8_path = os.path.join(settings.LANDSAT_IMAGES_PATH, "L8")
        self.tar = os.path.join(self.l8_path,"{}.tar.gz".format(self.scene_name))
        self.file = tarfile.open(self.tar)

    def test_get_scene_name_path(self):
        self.assertEqual(
            self.uploader._LandsatUploader__get_scene_name_path()[0]["name"],
            self.scene_name
        )
        
        self.assertEqual(
            self.uploader._LandsatUploader__get_scene_name_path()[0]["path"],
            os.path.join(
                settings.LANDSAT_IMAGES_PATH, "L8",
                self.scene_name + ".tar.gz"
            )
        )

    def test_uploader_scene_creation(self):
        scene = self.uploader._LandsatUploader__create_scene(self.scene_name)
        self.assertEqual(Scene.objects.count(), 1)

        created_scene = Scene.objects.get(name=self.scene_name)
        self.assertEqual(created_scene.path, "231")
        self.assertEqual(created_scene.row, "064")
        self.assertEqual(created_scene.cloud_rate, 0.0)

    def test_get_scene_geometry(self):
        path = int(self.data["path"])
        row = int(self.data["row"])
        geometry = self.uploader._LandsatUploader__get_scene_geom(path, row)

        self.assertEqual(self.landsatGrade.geom, geometry)

        for file in self.uploader._LandsatUploader__get_scene_name_path():
            scene = self.uploader._LandsatUploader__create_scene(file["name"])
            scene = Scene.objects.get(name=file["name"])
            self.assertEqual(scene.geom, geometry)
            self.assertEqual(scene.path, self.data["path"])
            self.assertEqual(scene.row, self.data["row"])
            self.assertEqual(scene.cloud_rate, 0.0 )

    def test_get_scene_extract_and_metadata(self):

        for file in self.uploader._LandsatUploader__get_scene_name_path():
            files = self.uploader._LandsatUploader__extract_files(name=file["name"], path=file["path"]) # Extract files
            
            mtl_path = [mtl["path"] for mtl in files if mtl["type"].upper() =="MTL"] # Get metadata file with list_comprehension
            
            scene = self.uploader._LandsatUploader__create_scene(file["name"], mtl_path[0]) # Creates a scene with cloud_rate 0
            files_created = self.uploader._LandsatUploader__upload_files(files, scene) # Create images 

            self.assertEqual( Image.objects.count(), 4  )
            self.assertEqual( len(files_created), 4     )
            self.assertEqual( scene.name, file["name"]  )
            self.assertEqual( scene.cloud_rate, 14.19   )
 
    def test_get_data_image_name_(self):
        result = get_data_image_name_(self.scene_name)
        self.assertTrue(result)
    
    def test__get_cloud_cover(self):
        for f in self.uploader._LandsatUploader__get_scene_name_path():
            file_extracted = self.uploader._LandsatUploader__extract_files(name=f["name"], path=f["path"])
            mtl_path = [mtl["path"] for mtl in file_extracted if mtl["type"].upper() =="MTL"]

        result = self.uploader._LandsatUploader__get_cloud_cover(mtl_path[0],'CORNER_UL_PROJECTION_X_PRODUCT')
        verify = isinstance(result,float)
        self.assertTrue(verify)

    def test__get_cloud_cover_exception(self):
        result = self.uploader._LandsatUploader__get_cloud_cover(self.file,'ORIGIN')
        self.assertEqual(result,0.0)
    
    def teste__get_scene_geom_exception(self):
        data = get_data_image_name_('LC08_L1TP_231064_20170511_20170511_01_RT_B1.TIF')
        result = self.uploader._LandsatUploader__get_scene_geom(self.l8_path,data['row'])
        self.assertFalse(result)
    
    def test__extract_files(self):
        result = self.uploader._LandsatUploader__extract_files(self.scene_name,self.tar)
        self.assertTrue(result)

    def test__get_mtl_file_exception(self):
        empty_tar =  os.path.join(self.l8_path,"empty.tar")
        lis = self.uploader._LandsatUploader__extract_files(self.scene_name,empty_tar)
        self.assertRaises(ValueError,self.uploader._LandsatUploader__get_mtl_file,lis)
       
    def test__get_mtl_file(self):
        for f in self.uploader._LandsatUploader__get_scene_name_path():
            file_extracted = self.uploader._LandsatUploader__extract_files(name=f["name"], path=f["path"])

        result = self.uploader._LandsatUploader__get_mtl_file(file_extracted)
        exists_path = os.path.exists(result)

        self.assertTrue(exists_path)

    def test_scene_extract_and_uploder(self):
        extracted_files = self.uploader.extract_and_populate_data()
        self.assertEqual(Image.objects.count(), 4)
        self.assertEqual(Scene.objects.count(), 1)
        self.assertTrue(self.scene_name in extracted_files)
        self.assertTrue(extracted_files[self.scene_name])
        self.assertTrue(extracted_files[self.scene_name]["scene"].name, self.scene_name)
        self.assertTrue( isinstance(extracted_files[self.scene_name]["scene"], Scene) )
        self.assertEqual( len(extracted_files[self.scene_name]["images"]), 4 )

    def tearDown(self):
        # for scene in Scene.objects.all(): # Delete scenes created after each test 
        #     scene.delete() 
        # for image in Image.objects.all(): # Delete image created after each test
        #     image.delete()

        rm_path = os.path.join( settings.MEDIA_ROOT, "L8", self.scene_name ) 
        if os.path.exists( rm_path ): # Delete created files in tests in MEDIA_ROOT
            shutil.rmtree( rm_path )

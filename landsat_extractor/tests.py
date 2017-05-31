import os
import shutil
import tarfile

from django.test import TestCase
from django.conf import settings

from .extractor import LandsatExtractor


def create_list():
    image_list = [] 

    for i in range(1,12):
        img = "LC08_L1TP_231064_20170511_20170511_01_RT_B{}.TIF".format(i)
        image_list.append(img)

    # image_list.append("LC08_L1TP_231064_20170511_20170511_01_RT_BQA.TIF")
    # image_list.append("LC08_L1TP_231064_20170511_20170511_01_RT_ANG.txt")
    image_list.append("LC08_L1TP_231064_20170511_20170511_01_RT_MTL.txt")

    return image_list

def files_to_extract():
    return [
        {
            "name": "LC08_L1TP_231064_20170511_20170511_01_RT_B4.TIF", 
            "path": os.path.join( 
                settings.MEDIA_ROOT, "L8", 
                "LC08_L1TP_231064_20170511_20170511_01_RT", 
                "LC08_L1TP_231064_20170511_20170511_01_RT_B4.TIF"
                ),
            "type": "B4",            
        },
        {
            "name": "LC08_L1TP_231064_20170511_20170511_01_RT_B5.TIF", 
            "path": os.path.join( 
                settings.MEDIA_ROOT, "L8", 
                "LC08_L1TP_231064_20170511_20170511_01_RT", 
                "LC08_L1TP_231064_20170511_20170511_01_RT_B5.TIF"
                ),
            "type": "B5",
        },
        {
            "name": "LC08_L1TP_231064_20170511_20170511_01_RT_B6.TIF", 
            "path": os.path.join( 
                settings.MEDIA_ROOT, "L8", 
                "LC08_L1TP_231064_20170511_20170511_01_RT", 
                "LC08_L1TP_231064_20170511_20170511_01_RT_B6.TIF"
                ),
            "type": "B6",
        },
        {
            "name": "LC08_L1TP_231064_20170511_20170511_01_RT_MTL.txt", 
            "path": os.path.join( 
                settings.MEDIA_ROOT, "L8", 
                "LC08_L1TP_231064_20170511_20170511_01_RT", 
                "LC08_L1TP_231064_20170511_20170511_01_RT_MTL.txt"
                ),
            "type": "MTL",
        },
    ]

class TestExtraction(TestCase):

    def setUp(self):
        self.files_extracted    = []
        self.image_list         = create_list()
        
        self.name               = "LC08_L1TP_231064_20170511_20170511_01_RT"
        self.tar_file           = "{}.tar.gz".format(self.name)
        
        self.L8_path            = os.path.join(settings.LANDSAT_IMAGES_PATH, "L8")
        self.file               = os.path.join(self.L8_path, self.tar_file)
        
        self.extractor          = LandsatExtractor(self.name, self.file, quiet=False)
        
        self.corrupt_name       = "corrupt"
        self.tar_opened         = tarfile.open(self.file)
        self.tar_corrupted      = os.path.join(self.L8_path, self.corrupt_name + '.tar.gz')

    def test_tarfile_isvalid(self):
        self.assertIsInstance( self.extractor, LandsatExtractor )
        self.assertTrue( self.extractor._test_tarfile() )

    def test_interest_bands(self):
        bands = self.extractor._interest_bands(bands=range(1,12))
        for i in bands:
            self.assertTrue(i in self.image_list)

    def test_extraction_files(self):
        self.files_extracted = self.extractor.extract_files()
        
        self.assertEqual(
            self.files_extracted, files_to_extract()
        )

    def test_list_file(self):
        
        list_file = self.extractor._list_files(self.tar_opened)
        self.assertEqual(len(list_file),14)

    def test_open_tar_file(self):
        tar = self.extractor._open_tar_file()
        names_tar_extractor = tar.getnames()[0]
        
        self.assertEqual(names_tar_extractor,self.tar_opened.getnames()[0])

    def test_open_tarfile_with_zip(self):
        zip_name = 'TM_WORLD_BORDERS-0.3'
        zip_name_formatted = '{}.zip'.format(zip_name)
        zip_path = os.path.join(self.L8_path, zip_name_formatted)
        ext_zip = LandsatExtractor(zip_name,zip_path,quiet=False)
        result = ext_zip._open_tar_file()
        self.assertEqual(result,False)

    def test_open_tar_file_quiet_none(self):     
        ext = LandsatExtractor(self.name, self.file, quiet=None)
        result = ext._open_tar_file()
        self.assertEqual(result.getnames()[0], self.tar_opened.getnames()[0])
        self.assertTrue(not ext.quiet)
    
    def test_open_tar_file_corrupted(self):
        ext = LandsatExtractor(self.corrupt_name, self.tar_corrupted, quiet=False)
        result = ext._open_tar_file()
        self.assertEqual(result, False)
    
    def test_validate_file_extracted(self):
        result = self.ext._validate_file_extracted(self.tar_name_formatted,self.path_test)
        self.assertTrue(result)

    def test_extract_interest_bands(self):
        result = self.extractor._extract_interest_bands(self.tar_opened)
        self.assertTrue(result)

    # def test_extract_interest_bands_validate_file_false(self):
    #     tar_extra_name = 'LC08_L1TP_225067_20170517_20170525_01_T1.tar.gz'
    #     self.assertRaises(ValueError,self.extractor._extract_interest_bands,tar_extra_name,self.L8_path)

    def tearDown(self):
        path = os.path.join(settings.LANDSAT_IMAGES_PATH, "L8", self.name)
        if os.path.isdir( path ):
            shutil.rmtree( path )

